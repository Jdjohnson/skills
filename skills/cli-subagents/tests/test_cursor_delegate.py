from __future__ import annotations

import json
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "cursor_delegate.py"


def make_fake(directory: Path, body: str) -> Path:
    fake = directory / "cursor-agent"
    fake.write_text(textwrap.dedent(body), encoding="utf-8")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    return fake


def run_wrapper(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


FAKE = """\
#!/usr/bin/env python3
import sys
if sys.argv[1:] == ["--version"]:
    print("2026.07.23-test")
    raise SystemExit(0)
if sys.argv[1:] == ["status"]:
    print("Logged in")
    raise SystemExit(0)
raise SystemExit(9)
"""


class CursorDelegateTests(unittest.TestCase):
    def test_doctor_marks_cursor_inactive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake(root, FAKE)
            result = run_wrapper(["doctor", "--cursor-bin", str(fake), "--cwd", str(root)])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertFalse(payload["active"])
            self.assertEqual(payload["status"], "inactive-ready")

    def test_run_requires_explicit_inactive_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake(root, FAKE)
            result = run_wrapper(
                ["run", "--cursor-bin", str(fake), "--cwd", str(root), "--prompt", "Review this."]
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertEqual(payload["status"], "inactive")
            self.assertIn("cursor_inactive_requires_explicit_opt_in", payload["issues"])

    def test_dry_run_calls_cursor_agent_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake(root, FAKE)
            result = run_wrapper(
                [
                    "run",
                    "--cursor-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--allow-inactive",
                    "--mode",
                    "plan",
                    "--model",
                    "gpt-5.6-sol-medium",
                    "--prompt",
                    "Plan the change.",
                    "--run-id",
                    "dry",
                    "--dry-run",
                ]
            )
            payload = json.loads(result.stdout)
            argv = payload["command"]["argv"]

            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "dry-run")
            self.assertEqual(Path(argv[0]).name, "cursor-agent")
            self.assertIn("--trust", argv)
            self.assertEqual(argv[argv.index("--mode") + 1], "plan")
            self.assertEqual(argv[argv.index("--model") + 1], "gpt-5.6-sol-medium")
            self.assertNotIn("--force", argv)
            self.assertNotIn("--yolo", argv)

    def test_partial_output_timeout_returns_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                import time
                if sys.argv[1:] == ["--version"]:
                    print("2026.07.23-test")
                    raise SystemExit(0)
                if sys.argv[1:] == ["status"]:
                    print("Logged in")
                    raise SystemExit(0)
                sys.stdout.write("partial")
                sys.stdout.flush()
                time.sleep(5)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--allow-inactive",
                    "--cursor-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--timeout",
                    "1",
                    "--prompt",
                    "Review this.",
                ]
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["failure_kind"], "timeout")
            self.assertIn("partial", payload["result"]["stdout"])


if __name__ == "__main__":
    unittest.main()
