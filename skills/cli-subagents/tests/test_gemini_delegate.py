from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "gemini_delegate.py"


def make_fake(directory: Path, body: str) -> Path:
    fake = directory / "gemini"
    fake.write_text(textwrap.dedent(body), encoding="utf-8")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    return fake


def run_wrapper(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    merged.pop("GEMINI_API_KEY", None)
    merged.pop("GOOGLE_API_KEY", None)
    merged["HOME"] = tempfile.gettempdir()
    if env:
        merged.update(env)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
        env=merged,
    )


class GeminiDelegateTests(unittest.TestCase):
    def test_doctor_marks_gemini_inactive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("0.52.0")
                    raise SystemExit(0)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(
                ["doctor", "--gemini-bin", str(fake), "--cwd", str(root)],
                env={"GEMINI_API_KEY": "fake-google-credential"},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertFalse(payload["active"])
            self.assertEqual(payload["status"], "inactive-ready")
            self.assertEqual(payload["model"], "gemini-3.6-flash")
            self.assertEqual(payload["auth"]["method"], "environment")

    def test_run_requires_explicit_inactive_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("0.52.0")
                    raise SystemExit(0)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(
                ["run", "--gemini-bin", str(fake), "--cwd", str(root), "--prompt", "Review this."],
                env={"GEMINI_API_KEY": "fake-google-credential"},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertEqual(payload["status"], "inactive")
            self.assertIn("gemini_inactive_requires_explicit_opt_in", payload["issues"])

    def test_run_dry_run_uses_plan_mode_and_concrete_model(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("0.52.0")
                    raise SystemExit(0)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--gemini-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--allow-inactive",
                    "--prompt",
                    "Inspect the screenshots.",
                    "--run-id",
                    "dry",
                    "--dry-run",
                ],
                env={"GEMINI_API_KEY": "fake-google-credential"},
            )
            payload = json.loads(result.stdout)
            argv = payload["command"]["argv"]

            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "dry-run")
            self.assertEqual(argv[argv.index("--model") + 1], "gemini-3.6-flash")
            self.assertEqual(argv[argv.index("--approval-mode") + 1], "plan")
            self.assertTrue(any(item.startswith("<prompt:") for item in argv))
            self.assertNotIn("Inspect the screenshots.", result.stdout)

    def test_probe_requires_exact_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake(
                root,
                """\
                #!/usr/bin/env python3
                import json
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("0.52.0")
                    raise SystemExit(0)
                print(json.dumps({"response": "GEMINI_READY"}))
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(
                ["probe", "--allow-inactive", "--gemini-bin", str(fake), "--cwd", str(root)],
                env={"GOOGLE_API_KEY": "fake-google-credential"},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["result"]["response_text"], "GEMINI_READY")

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
                    print("0.52.0")
                    raise SystemExit(0)
                sys.stdout.write("partial")
                sys.stdout.flush()
                time.sleep(5)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--gemini-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--allow-inactive",
                    "--timeout",
                    "1",
                    "--prompt",
                    "Review this.",
                ],
                env={"GEMINI_API_KEY": "fake-google-credential"},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["failure_kind"], "timeout")
            self.assertIn("partial", payload["result"]["stdout"])


if __name__ == "__main__":
    unittest.main()
