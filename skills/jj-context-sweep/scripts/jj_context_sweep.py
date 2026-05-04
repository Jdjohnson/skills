#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo


SOURCES = ("superhuman", "slack", "notion", "crm", "codex")
SOURCE_LABELS = {
    "superhuman": "Superhuman",
    "slack": "Slack",
    "notion": "Notion",
    "crm": "CRM",
    "codex": "Codex",
}
LOG_MARKER_PREFIX = "ctx"
TIMESTAMP_RE = re.compile(r"^\* \*\*(?P<label>[^*]+)\*\* — ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reusable helpers for jj-context-sweep state, Codex parsing, and daily-note writes."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    state = subparsers.add_parser("state", help="Show or initialize jj-context-sweep state.")
    state.add_argument("--root", default=".", help="Workspace root")
    state.add_argument("--state-path", help="Override state.json path")
    state.add_argument("--init", action="store_true", help="Create the state file if missing")

    codex = subparsers.add_parser("codex", help="Summarize local Codex sessions since a timestamp.")
    codex.add_argument("--since", required=True, help="Inclusive ISO-8601 lower bound")
    codex.add_argument(
        "--codex-home",
        default=str(Path.home() / ".codex"),
        help="Codex home containing sessions/",
    )
    codex.add_argument(
        "--timezone",
        default=os.environ.get("TZ") or "America/Chicago",
        help="IANA timezone name for output timestamps",
    )

    write = subparsers.add_parser(
        "write",
        help="Write/update jj-context-sweep log items and advance checkpoints when allowed.",
    )
    write.add_argument("--root", default=".", help="Workspace root")
    write.add_argument("--date", help="Target local date in YYYY-MM-DD")
    write.add_argument(
        "--journal-file",
        default=os.environ.get("CONTEXT_SWEEP_JOURNAL_FILE"),
        help="Target markdown journal file. Defaults to .context-sweep/journal/YYYY-MM-DD.md",
    )
    write.add_argument(
        "--journal-dir",
        default=os.environ.get("CONTEXT_SWEEP_JOURNAL_DIR"),
        help="Directory for default daily notes. Defaults to .context-sweep/journal under --root",
    )
    write.add_argument("--payload-file", required=True, help="Normalized JSON payload")
    write.add_argument("--state-path", help="Override state.json path")
    write.add_argument(
        "--timezone",
        default=os.environ.get("TZ") or "America/Chicago",
        help="IANA timezone name for parsing/rendering",
    )
    write.add_argument("--dry-run", action="store_true", help="Do not mutate files or checkpoints")

    return parser.parse_args()


def collapse_whitespace(text: str | None) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def trim_text(text: str | None, limit: int = 160) -> str:
    collapsed = collapse_whitespace(text)
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 3].rstrip() + "..."


def parse_iso_datetime(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=ZoneInfo("UTC"))
    return parsed


def isoformat_local(value: datetime, timezone: ZoneInfo) -> str:
    return value.astimezone(timezone).isoformat()


def normalize_addresses(value: str | None) -> str:
    addresses = getaddresses([value or ""])
    cleaned: list[str] = []
    for name, email_address in addresses:
        if name:
            cleaned.append(collapse_whitespace(name))
            continue
        if email_address:
            cleaned.append(email_address.split("@", 1)[0])
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    return f"{cleaned[0]} +{len(cleaned) - 1}"


def normalize_address_field(value: object) -> str:
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, dict):
                parts.append(str(item.get("email") or item.get("address") or item.get("name") or ""))
            else:
                parts.append(str(item))
        return normalize_addresses(", ".join(part for part in parts if part))
    if isinstance(value, dict):
        return normalize_addresses(str(value.get("email") or value.get("address") or value.get("name") or ""))
    return normalize_addresses(str(value or ""))


def parse_message_datetime(value: str, timezone: ZoneInfo) -> datetime:
    if not value:
        raise ValueError("message missing timestamp")
    try:
        parsed = parse_iso_datetime(value)
    except ValueError:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=ZoneInfo("UTC"))
    return parsed.astimezone(timezone)


def month_day_prefix(value: datetime) -> str:
    return f"{value.strftime('%b')} {value.day}"


def format_clock(value: datetime) -> str:
    return value.strftime("%I:%M%p").lstrip("0").lower()


def format_log_timestamp(value: datetime, note_date: date) -> str:
    clock = format_clock(value)
    if value.date() != note_date:
        return f"{month_day_prefix(value)} {clock}"
    return clock


def format_log_label(start: datetime, end: datetime | None, note_date: date) -> str:
    start_label = format_log_timestamp(start, note_date)
    if end and end != start:
        return f"{start_label}-{format_log_timestamp(end, note_date)}"
    return start_label


def encode_marker_id(source_id: str) -> str:
    return quote(str(source_id), safe="._-")


def build_marker(source: str, source_id: str) -> str:
    return f"<!-- {LOG_MARKER_PREFIX}:{source}:{encode_marker_id(source_id)} -->"


def default_state() -> dict:
    return {
        "version": 1,
        "sources": {
            source: {
                "high_water": None,
                "last_success_at": None,
                "last_run_at": None,
                "last_status": None,
                "last_note": None,
            }
            for source in SOURCES
        },
    }


def get_state_path(root: Path, override: str | None = None) -> Path:
    if override:
        return Path(override).expanduser().resolve()
    return root / ".context-sweep" / "jj-context-sweep" / "state.json"


def ensure_state_parent(state_path: Path) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)


def load_state(state_path: Path) -> dict:
    state = default_state()
    if not state_path.exists():
        return state
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    state["version"] = payload.get("version", 1)
    loaded_sources = payload.get("sources", {})
    for source in SOURCES:
        state["sources"][source].update(loaded_sources.get(source, {}))
    return state


def save_state(state_path: Path, state: dict) -> None:
    ensure_state_parent(state_path)
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def run_json_command(command: list[str]) -> dict:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def resolve_day_payload(
    root: Path,
    target_date: str | None,
    timezone: ZoneInfo,
    journal_file: str | None = None,
    journal_dir: str | None = None,
) -> dict:
    note_date = date.fromisoformat(target_date) if target_date else datetime.now(timezone).date()
    display_title = note_date.strftime("%A, %B ") + str(note_date.day) + note_date.strftime(", %Y")

    if journal_file:
        daily_file = Path(journal_file).expanduser()
        if not daily_file.is_absolute():
            daily_file = root / daily_file
    else:
        base_dir = Path(journal_dir).expanduser() if journal_dir else root / ".context-sweep" / "journal"
        if not base_dir.is_absolute():
            base_dir = root / base_dir
        daily_file = base_dir / f"{note_date.isoformat()}.md"

    return {
        "date": note_date.isoformat(),
        "daily_file": str(daily_file.resolve()),
        "display_title": display_title,
    }


def ensure_log_section(content: str) -> tuple[str, str, str]:
    if "## Log" not in content:
        content = content.rstrip() + "\n\n## Log\n\n"

    prefix, remainder = content.split("## Log", 1)
    after_log = remainder.lstrip("\n")
    parts = after_log.split("\n## ", 1)
    log_body = parts[0].rstrip("\n")
    tail = ""
    if len(parts) == 2:
        tail = "\n## " + parts[1]
    return prefix, log_body, tail


def parse_log_label_start(label: str, note_date: date, timezone: ZoneInfo) -> datetime | None:
    start_label = label.split("-", 1)[0].strip()
    if start_label.startswith("~"):
        start_label = start_label[1:].strip()
    if re.fullmatch(r"\d{1,2}:\d{2}(?:am|pm)", start_label):
        parsed = datetime.strptime(start_label, "%I:%M%p")
        return datetime.combine(
            note_date,
            parsed.time(),
            tzinfo=timezone,
        )
    if re.fullmatch(r"[A-Z][a-z]{2} \d{1,2} \d{1,2}:\d{2}(?:am|pm)", start_label):
        parsed = datetime.strptime(f"{note_date.year} {start_label}", "%Y %b %d %I:%M%p")
        return parsed.replace(tzinfo=timezone)
    return None


def parse_log_line_timestamp(line: str, note_date: date, timezone: ZoneInfo) -> datetime | None:
    match = TIMESTAMP_RE.match(line)
    if not match:
        return None
    return parse_log_label_start(match.group("label"), note_date=note_date, timezone=timezone)


def build_log_entry(item: dict, note_date: date, timezone: ZoneInfo) -> str:
    start = parse_iso_datetime(item["timestamp"]).astimezone(timezone)
    end_value = item.get("end_timestamp")
    end = parse_iso_datetime(end_value).astimezone(timezone) if end_value else None
    label = format_log_label(start=start, end=end, note_date=note_date)
    summary = collapse_whitespace(item["summary"])
    source_label = SOURCE_LABELS.get(item["source"], item["source"].title())
    marker = build_marker(item["source"], item["source_id"])
    return f"* **{label}** — [{source_label}] {summary} {marker}"


def normalize_write_item(item: dict, timezone: ZoneInfo) -> dict | None:
    if item.get("include", True) is False:
        return None
    source = item.get("source")
    source_id = item.get("source_id")
    timestamp = item.get("timestamp")
    summary = collapse_whitespace(item.get("summary"))
    if source not in SOURCES:
        raise ValueError(f"unknown source: {source!r}")
    if not source_id:
        raise ValueError("item missing source_id")
    if not timestamp:
        raise ValueError("item missing timestamp")
    if not summary:
        raise ValueError("item summary is empty")

    parsed_start = parse_iso_datetime(timestamp).astimezone(timezone)
    normalized = dict(item)
    normalized["source"] = source
    normalized["source_id"] = str(source_id)
    normalized["summary"] = summary
    normalized["timestamp"] = parsed_start.isoformat()

    end_value = item.get("end_timestamp")
    if end_value:
        normalized["end_timestamp"] = parse_iso_datetime(end_value).astimezone(timezone).isoformat()

    return normalized


def upsert_log_items(
    content: str,
    items: list[dict],
    note_date: date,
    timezone: ZoneInfo,
) -> tuple[str, list[dict]]:
    prefix, log_body, tail = ensure_log_section(content)
    lines = [line for line in log_body.splitlines() if line.strip()]
    actions: list[dict] = []

    deduped_items: dict[tuple[str, str], dict] = {}
    for item in items:
        deduped_items[(item["source"], item["source_id"])] = item

    ordered_items = sorted(
        deduped_items.values(),
        key=lambda item: parse_iso_datetime(item["timestamp"]).astimezone(timezone),
    )

    for item in ordered_items:
        marker = build_marker(item["source"], item["source_id"])
        rendered = build_log_entry(item=item, note_date=note_date, timezone=timezone)
        matches = [index for index, line in enumerate(lines) if marker in line]
        prior_line = lines[matches[0]] if len(matches) == 1 else None
        for index in reversed(matches):
            lines.pop(index)

        insert_at: int | None = None
        item_time = parse_iso_datetime(item["timestamp"]).astimezone(timezone)
        for index, line in enumerate(lines):
            existing_time = parse_log_line_timestamp(line, note_date=note_date, timezone=timezone)
            if existing_time and existing_time > item_time:
                insert_at = index
                break

        if insert_at is None:
            lines.append(rendered)
        else:
            lines.insert(insert_at, rendered)

        if not matches:
            action = "created"
        elif prior_line == rendered:
            action = "unchanged"
        else:
            action = "updated"

        actions.append(
            {
                "source": item["source"],
                "source_id": item["source_id"],
                "action": action,
                "entry": rendered,
            }
        )

    updated = prefix + "## Log\n\n"
    if lines:
        updated += "\n".join(lines) + "\n"
    if tail:
        updated += tail.lstrip("\n")
    return updated.rstrip() + "\n", actions


def apply_checkpoint_updates(state: dict, source_results: dict, run_finished_at: str) -> dict:
    updated = json.loads(json.dumps(state))
    for source, payload in source_results.items():
        if source not in updated["sources"]:
            continue
        source_state = updated["sources"][source]
        source_state["last_run_at"] = run_finished_at
        source_state["last_status"] = payload.get("status")
        source_state["last_note"] = payload.get("note")
        if payload.get("status") == "success":
            source_state["last_success_at"] = run_finished_at
            if payload.get("high_water"):
                existing_high_water = source_state.get("high_water")
                next_high_water = payload["high_water"]
                if (
                    not existing_high_water
                    or parse_iso_datetime(next_high_water) > parse_iso_datetime(existing_high_water)
                ):
                    source_state["high_water"] = next_high_water
    return updated


def write_payload(
    *,
    root: Path,
    payload: dict,
    target_date: str | None,
    timezone: ZoneInfo,
    state_path: Path,
    journal_file: str | None,
    journal_dir: str | None,
    dry_run: bool,
) -> dict:
    day_payload = resolve_day_payload(
        root=root,
        target_date=target_date,
        timezone=timezone,
        journal_file=journal_file,
        journal_dir=journal_dir,
    )
    note_date = date.fromisoformat(day_payload["date"])
    daily_file = Path(day_payload["daily_file"])
    state_before = load_state(state_path)

    normalized_items: list[dict] = []
    for raw_item in payload.get("items", []):
        normalized = normalize_write_item(raw_item, timezone=timezone)
        if normalized:
            normalized_items.append(normalized)

    content = (
        daily_file.read_text(encoding="utf-8")
        if daily_file.exists()
        else f"# {day_payload['display_title']}\n\n## Log\n\n"
    )
    updated_content, actions = upsert_log_items(
        content=content,
        items=normalized_items,
        note_date=note_date,
        timezone=timezone,
    )

    run_finished_at = datetime.now(tz=timezone).isoformat()
    source_results = {}
    for source in SOURCES:
        source_results[source] = dict(payload.get("sources", {}).get(source, {}))
        source_results[source].setdefault("status", None)
        source_results[source].setdefault("high_water", None)
        source_results[source].setdefault("note", None)

    state_after = apply_checkpoint_updates(
        state=state_before,
        source_results=source_results,
        run_finished_at=run_finished_at,
    )

    if not dry_run:
        daily_file.parent.mkdir(parents=True, exist_ok=True)
        daily_file.write_text(updated_content, encoding="utf-8")
        save_state(state_path, state_after)

    return {
        "daily_file": str(daily_file),
        "state_path": str(state_path),
        "dry_run": dry_run,
        "entry_count": len(actions),
        "created": sum(1 for action in actions if action["action"] == "created"),
        "updated": sum(1 for action in actions if action["action"] == "updated"),
        "unchanged": sum(1 for action in actions if action["action"] == "unchanged"),
        "actions": actions,
        "sources": source_results,
        "state_before": state_before,
        "state_after": state_after,
    }


def extract_message_text(content: list[dict] | None) -> str:
    parts: list[str] = []
    for item in content or []:
        item_type = item.get("type")
        if item_type in {"input_text", "output_text"}:
            parts.append(item.get("text", ""))
    return collapse_whitespace(" ".join(parts))


def summarize_codex_user_messages(messages: list[str], cwd: str | None) -> str:
    cwd_label = Path(cwd).name if cwd else "unknown workspace"
    if not messages:
        return f"Worked in Codex from {cwd_label}."
    lead = trim_text(messages[0], limit=100)
    if len(messages) == 1:
        return f"Worked in Codex from {cwd_label}: {lead}"
    tail = trim_text(messages[-1], limit=80)
    if tail == lead:
        return f"Worked in Codex from {cwd_label}: {lead}"
    return f"Worked in Codex from {cwd_label}: {lead}; later {tail}"


def normalize_superhuman_item(item: dict, timezone: ZoneInfo) -> dict:
    timestamp_value = (
        item.get("sent_at")
        or item.get("date")
        or item.get("last_message_at")
        or item.get("updated_at")
        or item.get("created_at")
    )
    sent_at = parse_message_datetime(str(timestamp_value or ""), timezone)
    source_id = item.get("message_id") or item.get("id") or item.get("thread_id")
    if not source_id:
        raise ValueError("superhuman item missing id")
    recipient = normalize_address_field(item.get("to") or item.get("recipients"))
    subject = trim_text(item.get("subject"), limit=90)
    snippet = trim_text(item.get("snippet") or item.get("summary") or item.get("body_text"), limit=120)
    summary = "Sent work email"
    if recipient:
        summary += f" to {recipient}"
    if subject:
        summary += f" re {subject}"
    if snippet:
        summary += f": {snippet}"
    return {
        "source": "superhuman",
        "source_id": str(source_id),
        "thread_id": item.get("thread_id") or item.get("threadId"),
        "timestamp": sent_at.isoformat(),
        "summary": summary,
        "kind": "sent_email",
        "subject": subject,
        "recipient": recipient,
    }


def slack_timestamp_to_datetime(value: str | int | float, timezone: ZoneInfo) -> datetime:
    return datetime.fromtimestamp(float(value), tz=ZoneInfo("UTC")).astimezone(timezone)


def normalize_slack_message(message: dict, timezone: ZoneInfo) -> dict:
    ts_value = message.get("ts") or message.get("timestamp")
    if ts_value is None:
        raise ValueError("slack message missing ts")
    channel_name = (
        message.get("channel_name")
        or (message.get("channel") or {}).get("name")
        or message.get("channel_id")
        or "DM"
    )
    text = trim_text(message.get("text") or message.get("snippet"), limit=160)
    summary = f"Sent Slack message in {channel_name}: {text}" if text else f"Sent Slack message in {channel_name}."
    return {
        "source": "slack",
        "source_id": str(ts_value),
        "timestamp": slack_timestamp_to_datetime(ts_value, timezone).isoformat(),
        "summary": summary,
        "kind": "sent_message",
        "channel_name": channel_name,
        "permalink": message.get("permalink"),
    }


def notion_title(candidate: dict) -> str:
    raw_title = (
        candidate.get("title")
        or candidate.get("page_title")
        or candidate.get("name")
        or candidate.get("plain_text")
    )
    return trim_text(raw_title, limit=100) or "Untitled page"


def normalize_notion_candidate(candidate: dict, timezone: ZoneInfo) -> dict:
    last_edited = candidate.get("last_edited_time")
    created = candidate.get("created_time")
    timestamp_value = last_edited or created
    if not timestamp_value:
        raise ValueError("notion candidate missing created/edited time")
    event_time = parse_iso_datetime(timestamp_value).astimezone(timezone)
    action = "Updated" if last_edited else "Created"
    title = notion_title(candidate)
    summary = f"{action} Notion page {title}"
    parent = trim_text(candidate.get("parent_title") or candidate.get("database_title"), limit=80)
    if parent:
        summary += f" in {parent}"
    return {
        "source": "notion",
        "source_id": str(candidate.get("id")),
        "timestamp": event_time.isoformat(),
        "summary": summary,
        "kind": "page_activity",
        "url": candidate.get("url"),
        "title": title,
    }


def normalize_crm_row(row: dict, timezone: ZoneInfo) -> dict:
    timestamp_value = row.get("updated_at") or row.get("created_at")
    if not timestamp_value:
        raise ValueError("crm row missing updated_at/created_at")
    event_time = parse_iso_datetime(timestamp_value).astimezone(timezone)
    stage = collapse_whitespace(row.get("stage"))
    deal_name = trim_text(row.get("deal_name") or row.get("name"), limit=90) or "Untitled deal"
    company = trim_text(row.get("company_name"), limit=60)
    summary = f"CRM update for {deal_name}"
    if company:
        summary += f" ({company})"
    if stage:
        summary += f": now in {stage}"
    note_excerpt = trim_text(row.get("note_excerpt") or row.get("change_summary"), limit=110)
    if note_excerpt:
        summary += f" — {note_excerpt}"
    source_id = row.get("audit_id") or row.get("id") or row.get("deal_id")
    if not source_id:
        raise ValueError("crm row missing id/audit_id/deal_id")
    return {
        "source": "crm",
        "source_id": str(source_id),
        "timestamp": event_time.isoformat(),
        "summary": summary,
        "kind": "deal_update",
        "deal_id": row.get("deal_id") or row.get("id"),
        "deal_name": deal_name,
    }


def parse_rollout_events(rollout_path: Path) -> tuple[str | None, str | None, list[tuple[datetime, str]]]:
    thread_id: str | None = None
    cwd: str | None = None
    user_messages: list[tuple[datetime, str]] = []

    with rollout_path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            payload = json.loads(line)
            entry_type = payload.get("type")
            timestamp = parse_iso_datetime(payload["timestamp"])

            if entry_type == "session_meta":
                meta = payload.get("payload", {})
                thread_id = meta.get("id", thread_id)
                cwd = meta.get("cwd", cwd)
                continue

            if entry_type != "response_item":
                continue

            item = payload.get("payload", {})
            if item.get("type") != "message" or item.get("role") != "user":
                continue
            text = extract_message_text(item.get("content"))
            user_messages.append((timestamp, text))

    return thread_id, cwd, user_messages


def iter_rollout_paths(codex_home: Path) -> list[Path]:
    sessions_dir = codex_home / "sessions"
    if not sessions_dir.exists():
        return []
    return sorted(sessions_dir.rglob("rollout-*.jsonl"))


def collect_codex_candidates(codex_home: Path, since: datetime, timezone: ZoneInfo) -> list[dict]:
    candidates: list[dict] = []
    for rollout_path in iter_rollout_paths(codex_home):
        thread_id, cwd, user_messages = parse_rollout_events(rollout_path)
        relevant_messages = [(stamp, text) for stamp, text in user_messages if stamp >= since]
        if not relevant_messages:
            continue
        candidate_id = thread_id or rollout_path.stem.replace("rollout-", "")
        summary = summarize_codex_user_messages(
            messages=[text for _, text in relevant_messages if text],
            cwd=cwd,
        )
        start_time = relevant_messages[0][0].astimezone(timezone)
        end_time = relevant_messages[-1][0].astimezone(timezone)
        candidates.append(
            {
                "source": "codex",
                "source_id": candidate_id,
                "rollout_id": rollout_path.stem.replace("rollout-", ""),
                "timestamp": start_time.isoformat(),
                "end_timestamp": end_time.isoformat() if end_time != start_time else None,
                "summary": summary,
                "kind": "local_session",
                "cwd": cwd,
                "path": str(rollout_path),
                "user_messages": [text for _, text in relevant_messages if text][:3],
            }
        )
    return sorted(candidates, key=lambda item: item["timestamp"])


def main() -> int:
    args = parse_args()

    if args.command == "state":
        root = Path(args.root).expanduser().resolve()
        state_path = get_state_path(root=root, override=args.state_path)
        state = load_state(state_path)
        if args.init and not state_path.exists():
            save_state(state_path, state)
        print(
            json.dumps(
                {
                    "state_path": str(state_path),
                    "exists": state_path.exists(),
                    "state": state,
                }
            )
        )
        return 0

    if args.command == "codex":
        timezone = ZoneInfo(args.timezone)
        since = parse_iso_datetime(args.since)
        codex_home = Path(args.codex_home).expanduser().resolve()
        candidates = collect_codex_candidates(codex_home=codex_home, since=since, timezone=timezone)
        print(
            json.dumps(
                {
                    "since": since.astimezone(timezone).isoformat(),
                    "codex_home": str(codex_home),
                    "count": len(candidates),
                    "items": candidates,
                }
            )
        )
        return 0

    root = Path(args.root).expanduser().resolve()
    timezone = ZoneInfo(args.timezone)
    state_path = get_state_path(root=root, override=args.state_path)
    payload_path = Path(args.payload_file).expanduser().resolve()
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    result = write_payload(
        root=root,
        payload=payload,
        target_date=args.date,
        timezone=timezone,
        state_path=state_path,
        journal_file=args.journal_file,
        journal_dir=args.journal_dir,
        dry_run=args.dry_run,
    )
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:  # pragma: no cover - CLI guardrail
        detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        print(f"ERROR: {detail}", file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:  # pragma: no cover - CLI guardrail
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
