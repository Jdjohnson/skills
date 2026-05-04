from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[3]


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


CONTEXT_SWEEP = load_module(
    "context_sweep",
    ROOT / "skills" / "context-sweep" / "scripts" / "context_sweep.py",
)


class LogWriterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.timezone = ZoneInfo("America/Chicago")
        self.note_date = date(2026, 4, 22)

    def test_upsert_log_items_inserts_chronologically(self) -> None:
        base = (
            "# Wednesday, April 22, 2026\n\n"
            "## Log\n\n"
            "* **2:15pm** — Existing checkpoint.\n"
            "\n## Evening\n"
        )
        items = [
            {
                "source": "superhuman",
                "source_id": "msg-1",
                "timestamp": "2026-04-22T13:05:00-05:00",
                "summary": "Sent email to JD re AECI follow-up.",
            },
            {
                "source": "slack",
                "source_id": "1713819600.000200",
                "timestamp": "2026-04-22T15:00:00-05:00",
                "summary": "Sent Slack message in deals: Shared proposal timing update.",
            },
        ]

        updated, actions = CONTEXT_SWEEP.upsert_log_items(
            content=base,
            items=items,
            note_date=self.note_date,
            timezone=self.timezone,
        )

        self.assertEqual([action["action"] for action in actions], ["created", "created"])
        self.assertLess(updated.index("msg-1"), updated.index("Existing checkpoint"))
        self.assertLess(updated.index("Existing checkpoint"), updated.index("1713819600.000200"))
        self.assertIn("## Evening", updated)

    def test_upsert_log_items_updates_same_marker_without_duplicates(self) -> None:
        original_item = {
            "source": "superhuman",
            "source_id": "msg-2",
            "timestamp": "2026-04-22T13:05:00-05:00",
            "summary": "Sent first note.",
        }
        updated_item = {
            "source": "superhuman",
            "source_id": "msg-2",
            "timestamp": "2026-04-22T13:07:00-05:00",
            "summary": "Sent revised note.",
        }
        once, _ = CONTEXT_SWEEP.upsert_log_items(
            content="# Wednesday, April 22, 2026\n\n## Log\n\n",
            items=[original_item],
            note_date=self.note_date,
            timezone=self.timezone,
        )
        twice, actions = CONTEXT_SWEEP.upsert_log_items(
            content=once,
            items=[updated_item],
            note_date=self.note_date,
            timezone=self.timezone,
        )

        marker = CONTEXT_SWEEP.build_marker("superhuman", "msg-2")
        self.assertEqual(twice.count(marker), 1)
        self.assertEqual(actions[0]["action"], "updated")
        self.assertIn("Sent revised note.", twice)

    def test_upsert_log_items_marks_no_op_rerun_unchanged(self) -> None:
        item = {
            "source": "codex",
            "source_id": "thread-123",
            "timestamp": "2026-04-22T10:00:00-05:00",
            "end_timestamp": "2026-04-22T10:15:00-05:00",
            "summary": "Worked in Codex from workspace: build a helper.",
        }
        once, _ = CONTEXT_SWEEP.upsert_log_items(
            content="# Wednesday, April 22, 2026\n\n## Log\n\n",
            items=[item],
            note_date=self.note_date,
            timezone=self.timezone,
        )
        twice, actions = CONTEXT_SWEEP.upsert_log_items(
            content=once,
            items=[item],
            note_date=self.note_date,
            timezone=self.timezone,
        )

        self.assertEqual(once, twice)
        self.assertEqual(actions[0]["action"], "unchanged")


class StateAndWriteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.timezone = ZoneInfo("America/Chicago")

    def test_apply_checkpoint_updates_advances_only_success_sources(self) -> None:
        state = CONTEXT_SWEEP.default_state()
        state["sources"]["superhuman"]["high_water"] = "2026-04-22T14:00:00-05:00"
        state["sources"]["crm"]["high_water"] = "2026-04-22T09:00:00-05:00"

        updated = CONTEXT_SWEEP.apply_checkpoint_updates(
            state=state,
            source_results={
                "superhuman": {
                    "status": "success",
                    "high_water": "2026-04-22T13:00:00-05:00",
                    "note": "2 messages",
                },
                "crm": {
                    "status": "skipped",
                    "high_water": "2026-04-22T14:00:00-05:00",
                    "note": "supabase unavailable",
                },
            },
            run_finished_at="2026-04-22T15:30:00-05:00",
        )

        self.assertEqual(updated["sources"]["superhuman"]["high_water"], "2026-04-22T14:00:00-05:00")
        self.assertEqual(updated["sources"]["crm"]["high_water"], "2026-04-22T09:00:00-05:00")
        self.assertEqual(updated["sources"]["crm"]["last_status"], "skipped")

    def test_write_payload_direct_write_advances_success_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            daily_file = root / "2026" / "week-17_2026-04-20_to_2026-04-26" / "2026-04-22-wed" / "2026-04-22-wed.md"
            state_path = root / ".context-sweep" / "context-sweep" / "state.json"

            payload = {
                "sources": {
                    "superhuman": {
                        "status": "success",
                        "high_water": "2026-04-22T11:00:00-05:00",
                        "note": "1 kept",
                    },
                    "crm": {
                        "status": "skipped",
                        "high_water": "2026-04-22T11:00:00-05:00",
                        "note": "supabase unavailable",
                    },
                },
                "items": [
                    {
                        "source": "superhuman",
                        "source_id": "msg-3",
                        "timestamp": "2026-04-22T10:30:00-05:00",
                        "summary": "Sent email to Andy re component wizard next steps.",
                    }
                ],
            }

            result = CONTEXT_SWEEP.write_payload(
                root=root,
                payload=payload,
                target_date="2026-04-22",
                timezone=self.timezone,
                state_path=state_path,
                journal_file=str(daily_file),
                journal_dir=None,
                dry_run=False,
            )

            self.assertEqual(result["created"], 1)
            written = daily_file.read_text(encoding="utf-8")
            self.assertIn("msg-3", written)

            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["sources"]["superhuman"]["high_water"], "2026-04-22T11:00:00-05:00")
            self.assertIsNone(state["sources"]["crm"]["high_water"])
            self.assertEqual(state["sources"]["crm"]["last_status"], "skipped")

    def test_write_payload_dry_run_does_not_mutate_files_or_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            daily_file = root / "2026" / "week-17_2026-04-20_to_2026-04-26" / "2026-04-22-wed" / "2026-04-22-wed.md"
            state_path = root / ".context-sweep" / "context-sweep" / "state.json"

            payload = {
                "sources": {
                    "slack": {
                        "status": "success",
                        "high_water": "2026-04-22T12:00:00-05:00",
                    }
                },
                "items": [
                    {
                        "source": "slack",
                        "source_id": "1713800000.000100",
                        "timestamp": "2026-04-22T11:50:00-05:00",
                        "summary": "Sent Slack message in deals: Shared timing note.",
                    }
                ],
            }

            result = CONTEXT_SWEEP.write_payload(
                root=root,
                payload=payload,
                target_date="2026-04-22",
                timezone=self.timezone,
                state_path=state_path,
                journal_file=str(daily_file),
                journal_dir=None,
                dry_run=True,
            )

            self.assertTrue(result["dry_run"])
            self.assertFalse(daily_file.exists())
            self.assertFalse(state_path.exists())


class CodexParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.timezone = ZoneInfo("America/Chicago")

    def test_collect_codex_candidates_summarizes_local_sessions_since_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            codex_home = Path(tmp_dir) / ".codex"
            rollout_dir = codex_home / "sessions" / "2026" / "04" / "22"
            rollout_dir.mkdir(parents=True)

            active_thread = "019db8ca-f63b-7063-9eae-40e40a0def34"
            active_path = rollout_dir / f"rollout-2026-04-22T14-00-00-{active_thread}.jsonl"
            active_lines = [
                {
                    "timestamp": "2026-04-22T19:00:00.000Z",
                    "type": "session_meta",
                    "payload": {
                        "id": active_thread,
                        "cwd": "/home/example/projects/workspace",
                    },
                },
                {
                    "timestamp": "2026-04-22T19:01:00.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": "Implement context-sweep."}],
                    },
                },
                {
                    "timestamp": "2026-04-22T19:15:00.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": "Run the validation bundle too."}],
                    },
                },
            ]
            active_path.write_text(
                "\n".join(json.dumps(line) for line in active_lines) + "\n",
                encoding="utf-8",
            )

            stale_thread = "019db8ca-f63b-7063-9eae-40e40a0def35"
            stale_path = rollout_dir / f"rollout-2026-04-22T10-00-00-{stale_thread}.jsonl"
            stale_lines = [
                {
                    "timestamp": "2026-04-22T15:00:00.000Z",
                    "type": "session_meta",
                    "payload": {"id": stale_thread, "cwd": "/tmp/other"},
                },
                {
                    "timestamp": "2026-04-22T15:05:00.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": "Older session."}],
                    },
                },
            ]
            stale_path.write_text(
                "\n".join(json.dumps(line) for line in stale_lines) + "\n",
                encoding="utf-8",
            )

            candidates = CONTEXT_SWEEP.collect_codex_candidates(
                codex_home=codex_home,
                since=datetime.fromisoformat("2026-04-22T18:30:00+00:00"),
                timezone=self.timezone,
            )

            self.assertEqual(len(candidates), 1)
            candidate = candidates[0]
            self.assertEqual(candidate["source_id"], active_thread)
            self.assertEqual(candidate["cwd"], "/home/example/projects/workspace")
            self.assertIn("workspace", candidate["summary"])
            self.assertIn("Implement context-sweep.", candidate["summary"])
            self.assertEqual(candidate["end_timestamp"], "2026-04-22T14:15:00-05:00")


class NormalizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.timezone = ZoneInfo("America/Chicago")

    def test_normalize_superhuman_item(self) -> None:
        candidate = CONTEXT_SWEEP.normalize_superhuman_item(
            {
                "id": "18fabc",
                "thread_id": "thread-9",
                "to": "Andy <andy@example.com>",
                "subject": "Component wizard",
                "snippet": "Can you review the next cut today?",
                "sent_at": "2026-04-22T15:30:00Z",
            },
            timezone=self.timezone,
        )

        self.assertEqual(candidate["source"], "superhuman")
        self.assertEqual(candidate["timestamp"], "2026-04-22T10:30:00-05:00")
        self.assertIn("andy", candidate["summary"].lower())
        self.assertIn("Component wizard", candidate["summary"])

    def test_normalize_slack_message(self) -> None:
        candidate = CONTEXT_SWEEP.normalize_slack_message(
            {
                "ts": "1713812400.000200",
                "channel_name": "deals",
                "text": "Shared the latest Ochsner timing update.",
            },
            timezone=self.timezone,
        )

        self.assertEqual(candidate["source"], "slack")
        self.assertIn("deals", candidate["summary"])
        self.assertIn("Ochsner", candidate["summary"])

    def test_normalize_notion_candidate(self) -> None:
        candidate = CONTEXT_SWEEP.normalize_notion_candidate(
            {
                "id": "page-1",
                "title": "AI workflow notes",
                "database_title": "Meeting Notes",
                "last_edited_time": "2026-04-22T16:45:00.000Z",
            },
            timezone=self.timezone,
        )

        self.assertEqual(candidate["source"], "notion")
        self.assertEqual(candidate["timestamp"], "2026-04-22T11:45:00-05:00")
        self.assertIn("Updated", candidate["summary"])
        self.assertIn("Meeting Notes", candidate["summary"])

    def test_normalize_crm_row(self) -> None:
        candidate = CONTEXT_SWEEP.normalize_crm_row(
            {
                "audit_id": "audit-7",
                "deal_id": "deal-3",
                "deal_name": "AECI",
                "company_name": "Associated Electric",
                "stage": "proposal_writing",
                "updated_at": "2026-04-22T17:10:00.000Z",
                "change_summary": "Advanced after revised scope note.",
            },
            timezone=self.timezone,
        )

        self.assertEqual(candidate["source"], "crm")
        self.assertEqual(candidate["source_id"], "audit-7")
        self.assertIn("proposal_writing", candidate["summary"])
        self.assertIn("Associated Electric", candidate["summary"])


if __name__ == "__main__":
    unittest.main()
