from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from delegate_test_support import import_wrapper, make_executable, payload, run_wrapper


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "claude_delegate.py"
CLAUDE = import_wrapper("claude_delegate")

PREFLIGHT = """\
#!/usr/bin/env python3
import sys
if sys.argv[1:] == ["--version"]:
    print("2.1.177 (Claude Code)")
    raise SystemExit(0)
if sys.argv[1:] == ["auth", "status", "--text"]:
    print("Logged in")
    raise SystemExit(0)
"""

class ClaudeDelegateTests(unittest.TestCase):
    def test_doctor_requires_auth_without_exposing_environment_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = CLAUDE.build_parser().parse_args(
                ["doctor", "--claude-bin", "/usr/bin/true", "--cwd", str(root)]
            )
            version = CLAUDE.CommandResult(["true", "--version"], 0, "2.1.177 (Claude Code)", "")
            auth = CLAUDE.CommandResult(
                ["true", "auth", "status", "--text"],
                1,
                "Not logged in. Run claude auth login to authenticate.",
                "",
            )
            empty_credentials = {name: "" for name in CLAUDE.CREDENTIAL_ENV_NAMES}

            with patch.dict(os.environ, empty_credentials), patch.object(
                CLAUDE, "run_subprocess", side_effect=[version, auth]
            ):
                missing_data = CLAUDE.collect_preflight(args)
            self.assertIn("claude_auth_missing", missing_data["issues"])
            self.assertEqual(missing_data["auth"]["method"], "missing")

            secret = "fake-claude-secret-value"
            with patch.dict(os.environ, empty_credentials | {"ANTHROPIC_API_KEY": secret}), patch.object(
                CLAUDE, "run_subprocess", side_effect=[version, auth]
            ):
                ready_data = CLAUDE.collect_preflight(args)
            self.assertTrue(ready_data["ok"])
            self.assertEqual(ready_data["auth"]["method"], "environment")
            self.assertIn("ANTHROPIC_API_KEY", ready_data["auth"]["env_credentials"])
            self.assertNotIn(secret, json.dumps(ready_data))

    def test_plan_run_builds_safe_private_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private_prompt = "Review internal source-material/users-export.csv safely."
            args = CLAUDE.build_parser().parse_args(
                [
                    "run",
                    "--claude-bin",
                    "/usr/bin/true",
                    "--cwd",
                    str(root),
                    "--mode",
                    "plan",
                    "--prompt",
                    private_prompt,
                    "--output-format",
                    "json",
                    "--allowed-tool",
                    "Bash(npm test)",
                ]
            )
            argv = CLAUDE.build_claude_run_argv(args, private_prompt)
            preview = CLAUDE.command_preview(argv, private_prompt)
            self.assertEqual(argv[argv.index("--permission-mode") + 1], "auto")
            self.assertNotIn("--model", argv)
            self.assertEqual(argv[argv.index("--effort") + 1], "high")
            self.assertIn("Bash(npm test)", argv[argv.index("--allowedTools") + 1])
            self.assertNotIn("--safe-mode", argv)
            self.assertNotIn(private_prompt, preview)
            self.assertTrue(any(item.startswith("<prompt:") for item in preview))

    def test_probe_requires_the_exact_ready_response(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_executable(
                root,
                "claude",
                PREFLIGHT
                + """\
print("READY")
raise SystemExit(0)
""",
            )
            result = run_wrapper(SCRIPT, ["probe", "--claude-bin", str(fake), "--cwd", str(root)])
            data = payload(result)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(data["ok"])
            self.assertEqual(data["probe"]["stdout"].strip(), "READY")
            self.assertIn("--no-session-persistence", data["command"]["argv"])

    def test_zero_exit_without_output_is_not_complete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = CLAUDE.build_parser().parse_args(
                ["run", "--claude-bin", "/usr/bin/true", "--cwd", str(root), "--prompt", "Review this."]
            )
            preflight = {"ok": True, "cwd": {"path": str(root)}}
            completed = CLAUDE.CommandResult(["true"], 0, "", "")
            output = io.StringIO()
            with patch.object(CLAUDE, "collect_preflight", return_value=preflight), patch.object(
                CLAUDE, "run_subprocess", return_value=completed
            ), redirect_stdout(output):
                returncode = CLAUDE.do_run(args)
            data = json.loads(output.getvalue())

            self.assertEqual(returncode, 1)
            self.assertEqual(data["failure_kind"], "empty_result")

if __name__ == "__main__":
    unittest.main()
