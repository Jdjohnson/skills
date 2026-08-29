#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request


API_BASE_URL = "https://api.manus.ai"
DEFAULT_PROFILE = os.environ.get("MANUS_DEFAULT_PROFILE", "manus-1.6")
TERMINAL_STATUSES = {"stopped", "waiting", "error"}
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"(?i)(x-manus-api-key\s*[:=]\s*)\S+"),
    re.compile(r"(?i)(MANUS_API_KEY\s*[:=]\s*)\S+"),
)


@dataclass
class ApiResult:
    ok: bool
    status_code: int | None
    data: dict[str, Any] | None
    failure_kind: str | None
    error_message: str | None


def redact_text(text: str, secret: str | None = None) -> str:
    redacted = text or ""
    if secret and len(secret) >= 4:
        redacted = redacted.replace(secret, "<redacted:MANUS_API_KEY>")
    for pattern in SECRET_PATTERNS:
        if pattern.groups:
            redacted = pattern.sub(r"\1<redacted>", redacted)
        else:
            redacted = pattern.sub("<redacted>", redacted)
    return redacted


def sanitize(value: Any, secret: str | None = None) -> Any:
    if isinstance(value, str):
        return redact_text(value, secret)
    if isinstance(value, list):
        return [sanitize(item, secret) for item in value]
    if isinstance(value, dict):
        return {key: sanitize(item, secret) for key, item in value.items() if key.lower() != "x-manus-api-key"}
    return value


def json_print(payload: dict[str, Any], secret: str | None = None) -> None:
    print(json.dumps(sanitize(payload, secret), indent=2, sort_keys=True))


def validate_cwd(raw_cwd: str | None) -> dict[str, Any]:
    cwd = Path(raw_cwd or os.getcwd()).expanduser()
    issues: list[str] = []
    try:
        resolved = cwd.resolve()
    except OSError as exc:
        return {"ok": False, "path": str(cwd), "issues": [f"cwd_resolve_failed:{exc}"]}
    if not resolved.exists():
        issues.append("cwd_missing")
    elif not resolved.is_dir():
        issues.append("cwd_not_directory")
    home = Path.home().resolve()
    unsafe = {Path(resolved.anchor).resolve(), home, home.parent}
    if Path("/Users").exists():
        unsafe.add(Path("/Users").resolve())
    if resolved in unsafe:
        issues.append("cwd_too_broad")
    return {"ok": not issues, "path": str(resolved), "issues": issues}


def parse_env_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, separator, value = line.partition("=")
        if separator and key.strip() == "MANUS_API_KEY":
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            return value or None
    return None


def credential_candidates(args: argparse.Namespace, cwd: Path) -> list[Path]:
    candidates: list[Path] = []
    if getattr(args, "env_file", None):
        candidates.append(Path(args.env_file).expanduser())
    if os.environ.get("MANUS_ENV_PATH"):
        candidates.append(Path(os.environ["MANUS_ENV_PATH"]).expanduser())
    current = cwd
    home = Path.home().resolve()
    while True:
        candidates.append(current / ".env.local")
        if current == home or current.parent == current:
            break
        current = current.parent
    unique: list[Path] = []
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved not in unique:
            unique.append(resolved)
    return unique


def resolve_credential(args: argparse.Namespace, cwd: Path) -> tuple[str | None, dict[str, Any]]:
    env_value = os.environ.get("MANUS_API_KEY")
    if env_value:
        return env_value, {"present": True, "source": "environment", "name": "MANUS_API_KEY"}
    for candidate in credential_candidates(args, cwd):
        value = parse_env_file(candidate)
        if value:
            return value, {"present": True, "source": "env-file", "path": str(candidate)}
    return None, {"present": False, "source": "missing"}


def classify_http_failure(status_code: int | None, code: str | None, message: str) -> str:
    text = f"{code or ''} {message}".lower()
    if status_code in {401, 403} or "api key" in text or "unauthor" in text or "permission_denied" in text:
        return "authentication_error"
    if status_code == 429 or "rate limit" in text or "rate_limited" in text:
        return "rate_limit_or_quota"
    if "credit" in text or "quota" in text or "insufficient" in text:
        return "rate_limit_or_quota"
    if status_code and status_code >= 500:
        return "service_unavailable"
    if status_code == 404 or "not_found" in text:
        return "not_found"
    if status_code == 400 or "invalid_argument" in text:
        return "invalid_argument"
    return "api_error"


def api_request(
    method: str,
    endpoint: str,
    secret: str,
    *,
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
    timeout: int = 30,
    base_url: str = API_BASE_URL,
) -> ApiResult:
    url = f"{base_url.rstrip('/')}/v2/{endpoint}"
    if params:
        encoded = parse.urlencode({key: str(value).lower() if isinstance(value, bool) else value for key, value in params.items() if value is not None})
        url = f"{url}?{encoded}"
    payload = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Accept": "application/json", "x-manus-api-key": secret}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=payload, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            parsed = json.loads(raw) if raw else {}
            if not isinstance(parsed, dict):
                return ApiResult(False, response.status, None, "invalid_response", "Manus returned non-object JSON")
            if parsed.get("ok") is False:
                api_error = parsed.get("error") if isinstance(parsed.get("error"), dict) else {}
                message = str(api_error.get("message") or "Manus API returned ok=false")
                kind = classify_http_failure(response.status, str(api_error.get("code") or ""), message)
                return ApiResult(False, response.status, parsed, kind, redact_text(message, secret))
            return ApiResult(True, response.status, parsed, None, None)
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {}
        api_error = parsed.get("error") if isinstance(parsed, dict) and isinstance(parsed.get("error"), dict) else {}
        message = str(api_error.get("message") or raw or exc.reason)
        kind = classify_http_failure(exc.code, str(api_error.get("code") or ""), message)
        return ApiResult(False, exc.code, parsed if isinstance(parsed, dict) else None, kind, redact_text(message, secret))
    except (error.URLError, TimeoutError, socket.timeout, OSError) as exc:
        return ApiResult(False, None, None, "network_or_sandbox", redact_text(str(exc), secret))
    except json.JSONDecodeError as exc:
        return ApiResult(False, None, None, "invalid_response", str(exc))


def extract_credits(data: dict[str, Any] | None) -> dict[str, Any] | None:
    if not data:
        return None
    source = data.get("data") if isinstance(data.get("data"), dict) else data
    fields = (
        "total_credits", "free_credits", "periodic_credits", "addon_credits",
        "pro_monthly_credits", "event_credits", "refresh_credits",
        "max_refresh_credits", "next_refresh_time", "refresh_interval",
    )
    return {field: source.get(field) for field in fields if field in source}


def preflight(args: argparse.Namespace, *, live: bool = True) -> tuple[dict[str, Any], str | None]:
    cwd_result = validate_cwd(getattr(args, "cwd", None))
    issues = list(cwd_result["issues"])
    cwd = Path(cwd_result["path"])
    secret, credential = resolve_credential(args, cwd)
    if not secret:
        issues.append("manus_api_key_missing")
    credits = None
    failure_kind = None
    api = None
    if secret and live:
        result = api_request("GET", "usage.availableCredits", secret, timeout=args.timeout, base_url=args.base_url)
        api = {"ok": result.ok, "status_code": result.status_code}
        if result.ok:
            credits = extract_credits(result.data)
        else:
            failure_kind = result.failure_kind
            issues.append(result.failure_kind or "manus_api_unavailable")
            api["error_message"] = result.error_message
    issues = list(dict.fromkeys(issues))
    return ({
        "ok": not issues,
        "status": "ready" if not issues else "blocked",
        "issues": issues,
        "failure_kind": failure_kind,
        "cwd": cwd_result,
        "credential": credential,
        "api": api,
        "credits": credits,
    }, secret)


def read_prompt(args: argparse.Namespace) -> str:
    sources = [bool(getattr(args, "prompt", None)), bool(getattr(args, "prompt_file", None)), bool(getattr(args, "stdin", False))]
    if sum(sources) != 1:
        raise ValueError("Provide exactly one of --prompt, --prompt-file, or --stdin.")
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).expanduser().read_text(encoding="utf-8")
    return sys.stdin.read()


def prompt_metadata(prompt: str) -> dict[str, Any]:
    return {"characters": len(prompt), "sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest()}


def safe_run_id(raw: str | None) -> str:
    if raw:
        cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", raw).strip(".-")
        if cleaned:
            return cleaned[:80]
    return time.strftime("%Y%m%dT%H%M%S")


def prepare_artifacts(cwd: Path, run_id: str, prompt: str) -> dict[str, str]:
    run_dir = cwd / ".tmp" / "manus" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    prompt_meta = run_dir / "prompt-meta.json"
    prompt_meta.write_text(json.dumps(prompt_metadata(prompt), indent=2, sort_keys=True), encoding="utf-8")
    return {
        "run_dir": str(run_dir),
        "prompt_meta": str(prompt_meta),
        "receipt": str(run_dir / "receipt.json"),
        "messages": str(run_dir / "messages.json"),
    }


def prepare_action_artifacts(cwd: Path, run_id: str) -> dict[str, str]:
    run_dir = cwd / ".tmp" / "manus" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return {
        "run_dir": str(run_dir),
        "receipt": str(run_dir / "receipt.json"),
    }


def write_receipt(artifacts: dict[str, str], payload: dict[str, Any], secret: str | None) -> None:
    Path(artifacts["receipt"]).write_text(json.dumps(sanitize(payload, secret), indent=2, sort_keys=True), encoding="utf-8")


def build_message(args: argparse.Namespace, prompt: str) -> dict[str, Any]:
    message: dict[str, Any] = {"content": [{"type": "text", "text": prompt}]}
    for attr, field in (("connector", "connectors"), ("enable_skill", "enable_skills"), ("force_skill", "force_skills")):
        values = getattr(args, attr, None)
        if values:
            message[field] = values
    return message


def load_schema(path_value: str | None) -> dict[str, Any] | None:
    if not path_value:
        return None
    value = json.loads(Path(path_value).expanduser().read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Structured output schema must be a JSON object.")
    return value


def task_status(result: ApiResult) -> str | None:
    if not result.data:
        return None
    task = result.data.get("task") if isinstance(result.data.get("task"), dict) else result.data
    value = task.get("status")
    return str(value) if value else None


def has_explicit_waiting_event(messages: ApiResult | None) -> bool:
    if not messages or not messages.ok or not messages.data:
        return False
    for event in messages.data.get("messages", []):
        if not isinstance(event, dict):
            continue
        update = event.get("status_update")
        if not isinstance(update, dict):
            continue
        status = str(update.get("agent_status") or "").lower()
        detail = update.get("status_detail")
        waiting_type = detail.get("waiting_for_event_type") if isinstance(detail, dict) else None
        if status == "waiting" or waiting_type:
            return True
    return False


def get_messages(secret: str, task_id: str, args: argparse.Namespace, *, order: str = "asc", limit: int = 200, verbose: bool = False) -> ApiResult:
    return api_request(
        "GET", "task.listMessages", secret,
        params={"task_id": task_id, "order": order, "limit": limit, "verbose": verbose, "slides_format": getattr(args, "slides_format", "pptx")},
        timeout=args.timeout, base_url=args.base_url,
    )


def message_ids(messages: ApiResult | None) -> set[str]:
    if not messages or not messages.ok or not messages.data:
        return set()
    return {
        str(event["id"])
        for event in messages.data.get("messages", [])
        if isinstance(event, dict) and event.get("id")
    }


def has_new_result_event(messages: ApiResult | None, baseline_message_ids: set[str]) -> bool:
    if not messages or not messages.ok or not messages.data:
        return False
    for event in messages.data.get("messages", []):
        if not isinstance(event, dict) or str(event.get("id") or "") in baseline_message_ids:
            continue
        if isinstance(event.get("assistant_message"), dict) or isinstance(event.get("structured_output_result"), dict):
            return True
    return False


def wait_for_task(
    secret: str,
    task_id: str,
    args: argparse.Namespace,
    *,
    baseline_message_ids: set[str] | None = None,
) -> tuple[ApiResult, ApiResult | None, bool]:
    deadline = time.monotonic() + args.wait_timeout
    last = ApiResult(False, None, None, "timeout", "No status received")
    while time.monotonic() < deadline:
        last = api_request("GET", "task.detail", secret, params={"task_id": task_id}, timeout=args.timeout, base_url=args.base_url)
        if not last.ok:
            # A newly-created task can be accepted before it has propagated to
            # the detail endpoint. Treat that narrow startup 404 as transient;
            # other failures should still stop immediately.
            if last.failure_kind == "not_found":
                time.sleep(args.poll_interval)
                continue
            return last, None, False
        status = task_status(last)
        if status in {"stopped", "error"}:
            messages = get_messages(secret, task_id, args)
            # Follow-ups can briefly retain the task's previous stopped state
            # while only the new user/running events are visible. Do not report
            # completion until the continuation has produced a new result.
            if baseline_message_ids is None or has_new_result_event(messages, baseline_message_ids):
                return last, messages, True
        if status == "waiting":
            messages = get_messages(secret, task_id, args)
            # Newly-created tasks can briefly report waiting before their first
            # message and running event become visible. Only treat waiting as a
            # user/approval boundary when the event stream says so explicitly.
            has_new_event = baseline_message_ids is None or bool(message_ids(messages) - baseline_message_ids)
            if has_new_event and has_explicit_waiting_event(messages):
                return last, messages, True
        time.sleep(args.poll_interval)
    return last, None, False


def assistant_texts(messages: ApiResult | None) -> list[str]:
    if not messages or not messages.data:
        return []
    values: list[str] = []
    for event in messages.data.get("messages", []):
        if not isinstance(event, dict):
            continue
        assistant = event.get("assistant_message")
        if isinstance(assistant, dict) and isinstance(assistant.get("content"), str):
            values.append(assistant["content"].strip())
    return values


def receipt_safe_messages(data: dict[str, Any] | None) -> dict[str, Any] | None:
    if data is None:
        return None
    safe = json.loads(json.dumps(data))
    for event in safe.get("messages", []):
        if not isinstance(event, dict):
            continue
        user_message = event.get("user_message")
        if isinstance(user_message, dict) and "content" in user_message:
            user_message["content"] = "<redacted:submitted-prompt>"
    return safe


def require_prompt(args: argparse.Namespace) -> tuple[str | None, dict[str, Any] | None, int | None]:
    try:
        prompt = read_prompt(args)
    except (OSError, ValueError) as exc:
        return None, {"ok": False, "status": "blocked", "issues": [str(exc)]}, 2
    return prompt, None, None


def do_doctor(args: argparse.Namespace) -> int:
    payload, secret = preflight(args)
    json_print(payload, secret)
    return 0 if payload["ok"] else 2


def do_credits(args: argparse.Namespace) -> int:
    payload, secret = preflight(args)
    json_print(payload, secret)
    return 0 if payload["ok"] else 2


def do_probe(args: argparse.Namespace) -> int:
    prompt = "Reply exactly MANUS_READY."
    payload, secret = preflight(args, live=not args.dry_run)
    if not payload["ok"] or not secret:
        payload["probe"] = None
        json_print(payload, secret)
        return 2
    cwd = Path(payload["cwd"]["path"])
    artifacts = prepare_artifacts(cwd, safe_run_id(args.run_id or "probe"), prompt)
    body = {
        "message": {"content": [{"type": "text", "text": prompt}]},
        "interactive_mode": False,
        "hide_in_task_list": True,
        "share_visibility": "private",
        "agent_profile": "manus-1.6-lite",
        "title": "Manus wrapper probe",
    }
    payload.update({"artifacts": artifacts, "prompt": prompt_metadata(prompt)})
    if args.dry_run:
        payload.update({"ok": True, "status": "dry-run", "probe": None})
        write_receipt(artifacts, payload, secret)
        json_print(payload, secret)
        return 0
    created = api_request("POST", "task.create", secret, body=body, timeout=args.timeout, base_url=args.base_url)
    task_id = created.data.get("task_id") if created.ok and created.data else None
    if not created.ok or not task_id:
        payload.update({
            "ok": False, "status": "blocked", "failure_kind": created.failure_kind or "task_create_failed",
            "issues": [created.failure_kind or "task_create_failed"], "task": created.data, "probe": None,
        })
        write_receipt(artifacts, payload, secret)
        json_print(payload, secret)
        return 1
    detail, messages, terminal = wait_for_task(secret, str(task_id), args)
    texts = assistant_texts(messages)
    exact = terminal and task_status(detail) == "stopped" and any(text == "MANUS_READY" for text in texts)
    payload.update({
        "ok": exact,
        "status": "ready" if exact else task_status(detail) or "blocked",
        "failure_kind": None if exact else "unexpected_probe_response" if terminal else "wait_timeout",
        "issues": [] if exact else ["unexpected_probe_response" if terminal else "wait_timeout"],
        "task": created.data,
        "task_detail": detail.data,
        "probe": {"ok": exact, "assistant_texts": texts},
        "messages": receipt_safe_messages(messages.data if messages else None),
    })
    if messages and messages.data:
        Path(artifacts["messages"]).write_text(json.dumps(sanitize(receipt_safe_messages(messages.data), secret), indent=2, sort_keys=True), encoding="utf-8")
    write_receipt(artifacts, payload, secret)
    json_print(payload, secret)
    return 0 if exact else 1


def do_run(args: argparse.Namespace) -> int:
    prompt, error, code = require_prompt(args)
    if code is not None:
        json_print(error or {})
        return code
    preflight_payload, secret = preflight(args, live=not args.dry_run)
    if not preflight_payload["ok"] or not secret:
        preflight_payload.update({"prompt": prompt_metadata(prompt or ""), "task": None})
        json_print(preflight_payload, secret)
        return 2
    cwd = Path(preflight_payload["cwd"]["path"])
    artifacts = prepare_artifacts(cwd, safe_run_id(args.run_id), prompt or "")
    try:
        schema = load_schema(args.structured_output_schema)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        payload = {"ok": False, "status": "blocked", "issues": [str(exc)], "artifacts": artifacts}
        write_receipt(artifacts, payload, secret)
        json_print(payload, secret)
        return 2
    body: dict[str, Any] = {
        "message": build_message(args, prompt or ""),
        "interactive_mode": args.interactive,
        "hide_in_task_list": args.hide_in_task_list,
        "share_visibility": args.share_visibility,
        "agent_profile": args.profile,
    }
    for attr in ("project_id", "title"):
        value = getattr(args, attr)
        if value:
            body[attr] = value
    if schema:
        body["structured_output_schema"] = schema
    preview = sanitize(body)
    preview["message"]["content"] = [f"<prompt:{len(prompt or '')} chars sha256:{prompt_metadata(prompt or '')['sha256']}>"]
    payload = preflight_payload | {
        "prompt": prompt_metadata(prompt or ""), "artifacts": artifacts,
        "request": {"endpoint": "task.create", "body": preview},
    }
    if args.dry_run:
        payload.update({"ok": True, "status": "dry-run", "task": None})
        write_receipt(artifacts, payload, secret)
        json_print(payload, secret)
        return 0
    result = api_request("POST", "task.create", secret, body=body, timeout=args.timeout, base_url=args.base_url)
    payload["ok"] = result.ok
    payload["status"] = "submitted" if result.ok else "blocked"
    payload["failure_kind"] = result.failure_kind
    payload["issues"] = [] if result.ok else [result.failure_kind or "task_create_failed"]
    payload["task"] = result.data
    if result.error_message:
        payload["error_message"] = result.error_message
    task_id = result.data.get("task_id") if result.ok and result.data else None
    if result.ok and args.wait and task_id:
        detail, messages, terminal = wait_for_task(secret, str(task_id), args)
        payload["status"] = task_status(detail) or ("timeout" if not terminal else "unknown")
        payload["task_detail"] = detail.data
        payload["messages"] = receipt_safe_messages(messages.data if messages else None)
        payload["ok"] = detail.ok and terminal and task_status(detail) != "error" and bool(messages and messages.ok)
        if not terminal:
            payload["failure_kind"] = "wait_timeout"
            payload["issues"] = ["wait_timeout"]
        elif not payload["ok"]:
            payload["failure_kind"] = detail.failure_kind or (messages.failure_kind if messages else None) or "task_error"
            payload["issues"] = [payload["failure_kind"]]
        if messages and messages.data:
            Path(artifacts["messages"]).write_text(json.dumps(sanitize(receipt_safe_messages(messages.data), secret), indent=2, sort_keys=True), encoding="utf-8")
    write_receipt(artifacts, payload, secret)
    json_print(payload, secret)
    return 0 if payload["ok"] else 1


def do_status(args: argparse.Namespace) -> int:
    payload, secret = preflight(args)
    if not payload["ok"] or not secret:
        json_print(payload, secret)
        return 2
    result = api_request("GET", "task.detail", secret, params={"task_id": args.task_id}, timeout=args.timeout, base_url=args.base_url)
    payload.update({"ok": result.ok, "status": task_status(result) or ("blocked" if not result.ok else "unknown"), "failure_kind": result.failure_kind, "task": result.data})
    if result.error_message:
        payload["error_message"] = result.error_message
    json_print(payload, secret)
    return 0 if result.ok else 1


def do_messages(args: argparse.Namespace) -> int:
    payload, secret = preflight(args)
    if not payload["ok"] or not secret:
        json_print(payload, secret)
        return 2
    result = get_messages(secret, args.task_id, args, order=args.order, limit=args.limit, verbose=args.verbose)
    payload.update({"ok": result.ok, "status": "read" if result.ok else "blocked", "failure_kind": result.failure_kind, "messages": result.data})
    if result.error_message:
        payload["error_message"] = result.error_message
    json_print(payload, secret)
    return 0 if result.ok else 1


def do_follow_up(args: argparse.Namespace) -> int:
    prompt, error, code = require_prompt(args)
    if code is not None:
        json_print(error or {})
        return code
    payload, secret = preflight(args)
    if not payload["ok"] or not secret:
        json_print(payload, secret)
        return 2
    cwd = Path(payload["cwd"]["path"])
    artifacts = prepare_artifacts(cwd, safe_run_id(args.run_id), prompt or "")
    payload["artifacts"] = artifacts
    baseline = get_messages(secret, args.task_id, args, order="asc", limit=200)
    if not baseline.ok:
        payload.update({
            "ok": False,
            "status": "blocked",
            "failure_kind": baseline.failure_kind or "baseline_messages_failed",
            "issues": [baseline.failure_kind or "baseline_messages_failed"],
            "error_message": baseline.error_message,
        })
        write_receipt(artifacts, payload, secret)
        json_print(payload, secret)
        return 1
    baseline_ids = message_ids(baseline)
    body: dict[str, Any] = {"task_id": args.task_id, "message": build_message(args, prompt or "")}
    if args.profile:
        body["agent_profile"] = args.profile
    preview = sanitize(body)
    preview["message"]["content"] = [f"<prompt:{len(prompt or '')} chars sha256:{prompt_metadata(prompt or '')['sha256']}>"]
    payload.update({"prompt": prompt_metadata(prompt or ""), "request": {"endpoint": "task.sendMessage", "body": preview}})
    result = api_request("POST", "task.sendMessage", secret, body=body, timeout=args.timeout, base_url=args.base_url)
    payload.update({"ok": result.ok, "status": "submitted" if result.ok else "blocked", "failure_kind": result.failure_kind, "task": result.data})
    if result.ok and args.wait:
        detail, messages, terminal = wait_for_task(secret, args.task_id, args, baseline_message_ids=baseline_ids)
        payload.update({"status": task_status(detail) or ("timeout" if not terminal else "unknown"), "task_detail": detail.data, "messages": receipt_safe_messages(messages.data if messages else None)})
        payload["ok"] = detail.ok and terminal and task_status(detail) != "error" and bool(messages and messages.ok)
        if not payload["ok"]:
            payload["failure_kind"] = "wait_timeout" if not terminal else detail.failure_kind or (messages.failure_kind if messages else None) or "task_error"
        if messages and messages.data:
            Path(artifacts["messages"]).write_text(json.dumps(sanitize(receipt_safe_messages(messages.data), secret), indent=2, sort_keys=True), encoding="utf-8")
    if result.error_message:
        payload["error_message"] = result.error_message
    if not result.ok:
        payload["issues"] = [result.failure_kind or "task_send_message_failed"]
    write_receipt(artifacts, payload, secret)
    json_print(payload, secret)
    return 0 if payload["ok"] else 1


def do_stop(args: argparse.Namespace) -> int:
    payload, secret = preflight(args)
    if not payload["ok"] or not secret:
        json_print(payload, secret)
        return 2
    cwd = Path(payload["cwd"]["path"])
    artifacts = prepare_action_artifacts(cwd, safe_run_id(args.run_id or f"stop-{args.task_id[:12]}"))
    payload["artifacts"] = artifacts
    result = api_request("POST", "task.stop", secret, body={"task_id": args.task_id}, timeout=args.timeout, base_url=args.base_url)
    deadline = time.monotonic() + args.verify_timeout
    detail = ApiResult(False, None, None, "stop_unconfirmed", "Stop state was not checked")
    while time.monotonic() < deadline:
        detail = api_request("GET", "task.detail", secret, params={"task_id": args.task_id}, timeout=min(args.timeout, 30), base_url=args.base_url)
        if detail.ok and task_status(detail) == "stopped":
            break
        time.sleep(args.poll_interval)
    confirmed = detail.ok and task_status(detail) == "stopped"
    payload.update({
        "ok": confirmed,
        "status": "stopped" if confirmed else "blocked",
        "failure_kind": None if confirmed else result.failure_kind or detail.failure_kind or "stop_unconfirmed",
        "issues": [] if confirmed else [result.failure_kind or detail.failure_kind or "stop_unconfirmed"],
        "stop_request": {
            "ok": result.ok,
            "status_code": result.status_code,
            "failure_kind": result.failure_kind,
            "error_message": result.error_message,
            "response": result.data,
            "reconciled_after_request_failure": confirmed and not result.ok,
        },
        "task": detail.data,
    })
    write_receipt(artifacts, payload, secret)
    json_print(payload, secret)
    return 0 if confirmed else 1


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--cwd", default=os.getcwd(), help="Trusted project directory used for credential lookup and artifacts.")
    parser.add_argument("--env-file", help="Explicit local env file containing MANUS_API_KEY.")
    parser.add_argument("--timeout", type=int, default=30, help="Per-request timeout in seconds.")
    parser.add_argument("--base-url", default=os.environ.get("MANUS_API_BASE_URL", API_BASE_URL), help=argparse.SUPPRESS)


def add_prompt_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--stdin", action="store_true")


def add_wait_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--wait", action="store_true", help="Poll until stopped, waiting, error, or timeout.")
    parser.add_argument("--wait-timeout", type=int, default=900)
    parser.add_argument("--poll-interval", type=float, default=5.0)
    parser.add_argument("--slides-format", choices=("html", "pptx"), default="pptx")


def add_capability_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--connector", action="append", default=[])
    parser.add_argument("--enable-skill", action="append", default=[])
    parser.add_argument("--force-skill", action="append", default=[])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe wrapper for Manus API delegation.")
    commands = parser.add_subparsers(dest="command", required=True)

    doctor = commands.add_parser("doctor", help="Check credential, API readiness, and spendable credits.")
    add_common(doctor)
    doctor.set_defaults(func=do_doctor)

    credits = commands.add_parser("credits", help="Read the authoritative spendable credit balance.")
    add_common(credits)
    credits.set_defaults(func=do_credits)

    probe = commands.add_parser("probe", help="Run a minimal MANUS_READY end-to-end smoke test.")
    add_common(probe)
    add_wait_args(probe)
    probe.set_defaults(wait=True)
    probe.add_argument("--run-id")
    probe.add_argument("--dry-run", action="store_true")
    probe.set_defaults(func=do_probe)

    run = commands.add_parser("run", help="Submit a bounded Manus task.")
    add_common(run)
    add_prompt_args(run)
    add_wait_args(run)
    add_capability_args(run)
    run.add_argument("--profile", default=DEFAULT_PROFILE)
    run.add_argument("--title")
    run.add_argument("--project-id")
    run.add_argument("--interactive", action="store_true")
    run.add_argument("--hide-in-task-list", action="store_true")
    run.add_argument("--share-visibility", choices=("private", "team", "public"), default="private")
    run.add_argument("--structured-output-schema", help="Path to a JSON Schema file.")
    run.add_argument("--run-id")
    run.add_argument("--dry-run", action="store_true")
    run.set_defaults(func=do_run)

    status = commands.add_parser("status", help="Read task status and metadata.")
    add_common(status)
    status.add_argument("task_id")
    status.set_defaults(func=do_status)

    messages = commands.add_parser("messages", help="Read task conversation and output events.")
    add_common(messages)
    messages.add_argument("task_id")
    messages.add_argument("--order", choices=("asc", "desc"), default="asc")
    messages.add_argument("--limit", type=int, choices=range(1, 201), default=200)
    messages.add_argument("--verbose", action="store_true")
    messages.add_argument("--slides-format", choices=("html", "pptx"), default="pptx")
    messages.set_defaults(func=do_messages)

    follow = commands.add_parser("follow-up", help="Send a follow-up message to an existing task.")
    add_common(follow)
    add_prompt_args(follow)
    add_wait_args(follow)
    add_capability_args(follow)
    follow.add_argument("task_id")
    follow.add_argument("--profile")
    follow.add_argument("--run-id")
    follow.set_defaults(func=do_follow_up)

    stop = commands.add_parser("stop", help="Stop a running task; it remains resumable.")
    add_common(stop)
    stop.add_argument("task_id")
    stop.add_argument("--run-id")
    stop.add_argument("--verify-timeout", type=int, default=90)
    stop.add_argument("--poll-interval", type=float, default=5.0)
    stop.set_defaults(timeout=90)
    stop.set_defaults(func=do_stop)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if hasattr(args, "poll_interval") and args.poll_interval < 1:
        json_print({"ok": False, "status": "blocked", "issues": ["poll_interval_must_be_at_least_1"]})
        return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
