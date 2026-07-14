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


def load_module():
    path = ROOT / "skills" / "context-sweep" / "scripts" / "context_sweep.py"
    spec = importlib.util.spec_from_file_location("context_sweep", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["context_sweep"] = module
    spec.loader.exec_module(module)
    return module


SWEEP = load_module()


class ContextSweepTests(unittest.TestCase):
    def setUp(self) -> None:
        self.timezone = ZoneInfo("America/Chicago")
        self.note_date = date(2026, 4, 22)

    def test_generic_sources_insert_chronologically(self) -> None:
        base = "# Day\n\n## Log\n\n* **2:15pm** — Existing checkpoint.\n"
        items = [
            {"source": "email", "source_id": "m-1", "timestamp": "2026-04-22T13:05:00-05:00", "summary": "Sent the revised scope."},
            {"source": "team-chat", "source_id": "c-1", "timestamp": "2026-04-22T15:00:00-05:00", "summary": "Confirmed the delivery date."},
        ]
        updated, actions = SWEEP.upsert_log_items(base, items, self.note_date, self.timezone)
        self.assertEqual([item["action"] for item in actions], ["created", "created"])
        self.assertLess(updated.index("m-1"), updated.index("Existing checkpoint"))
        self.assertLess(updated.index("Existing checkpoint"), updated.index("c-1"))

    def test_same_marker_updates_without_duplicate(self) -> None:
        original = {"source": "notes", "source_id": "n-1", "timestamp": "2026-04-22T13:05:00-05:00", "summary": "Captured an initial decision."}
        revised = dict(original, summary="Captured the final decision.")
        once, _ = SWEEP.upsert_log_items("# Day\n\n## Log\n\n", [original], self.note_date, self.timezone)
        twice, actions = SWEEP.upsert_log_items(once, [revised], self.note_date, self.timezone)
        self.assertEqual(twice.count(SWEEP.build_marker("notes", "n-1")), 1)
        self.assertEqual(actions[0]["action"], "updated")

    def test_dynamic_checkpoints_advance_success_only_and_forward_only(self) -> None:
        state = {"version": 1, "sources": {"email": {"high_water": "2026-04-22T14:00:00-05:00"}}}
        updated = SWEEP.apply_checkpoint_updates(
            state,
            {
                "email": {"status": "success", "high_water": "2026-04-22T13:00:00-05:00"},
                "tasks": {"status": "skipped", "high_water": "2026-04-22T15:00:00-05:00"},
            },
            "2026-04-22T15:30:00-05:00",
        )
        self.assertEqual(updated["sources"]["email"]["high_water"], "2026-04-22T14:00:00-05:00")
        self.assertIsNone(updated["sources"]["tasks"]["high_water"])
        self.assertEqual(updated["sources"]["tasks"]["last_status"], "skipped")

    def test_write_and_dry_run_boundaries(self) -> None:
        payload = {
            "sources": {"email": {"status": "success", "high_water": "2026-04-22T11:00:00-05:00"}},
            "items": [{"source": "email", "source_id": "m-2", "timestamp": "2026-04-22T10:30:00-05:00", "summary": "Sent a decision note."}],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / "day.md"
            state = root / "state.json"
            dry = SWEEP.write_payload(root=root, payload=payload, target_date="2026-04-22", timezone=self.timezone, state_path=state, journal_file=str(note), journal_dir=None, dry_run=True)
            self.assertTrue(dry["dry_run"])
            self.assertFalse(note.exists())
            written = SWEEP.write_payload(root=root, payload=payload, target_date="2026-04-22", timezone=self.timezone, state_path=state, journal_file=str(note), journal_dir=None, dry_run=False)
            self.assertEqual(written["created"], 1)
            self.assertIn("m-2", note.read_text())
            self.assertEqual(json.loads(state.read_text())["sources"]["email"]["high_water"], "2026-04-22T11:00:00-05:00")

    def test_codex_parser_uses_stable_thread_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".codex"
            folder = home / "sessions" / "2026" / "04" / "22"
            folder.mkdir(parents=True)
            thread = "019db8ca-f63b-7063-9eae-40e40a0def34"
            path = folder / f"rollout-2026-04-22T14-00-00-{thread}.jsonl"
            rows = [
                {"timestamp": "2026-04-22T19:00:00Z", "type": "session_meta", "payload": {"id": thread, "cwd": "/home/example/workspace"}},
                {"timestamp": "2026-04-22T19:01:00Z", "type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "Implement the helper."}]}},
            ]
            path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
            candidates = SWEEP.collect_codex_candidates(home, datetime.fromisoformat("2026-04-22T18:30:00+00:00"), self.timezone)
            self.assertEqual(candidates[0]["source_id"], thread)
            self.assertIn("Implement the helper.", candidates[0]["summary"])


if __name__ == "__main__":
    unittest.main()
