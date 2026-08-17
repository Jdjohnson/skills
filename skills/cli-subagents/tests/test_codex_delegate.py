from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from delegate_test_support import import_wrapper, make_executable, payload, run_wrapper


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "codex_delegate.py"
CODEX = import_wrapper("codex_delegate")

PREFLIGHT = """\
#!/usr/bin/env python3
import json
import sys
if sys.argv[1:] == ["--version"]:
    print("codex-cli 0.142.3")
    raise SystemExit(0)
if sys.argv[1:] == ["login", "status"]:
    print("Logged in using ChatGPT")
    raise SystemExit(0)
"""

LAST_MESSAGE_HELPER = """\
def last_message_path():
    args = sys.argv[1:]
    return args[args.index("--output-last-message") + 1]
"""


class CodexDelegateTests(unittest.TestCase):
    def test_doctor_distinguishes_missing_and_ready_auth(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = CODEX.build_parser().parse_args(
                ["doctor", "--codex-bin", "/usr/bin/true", "--cwd", str(root)]
            )
            version = CODEX.CommandResult(["true", "--version"], 0, "codex-cli 0.142.3", "")
            missing_auth = CODEX.CommandResult(["true", "login", "status"], 1, "", "Not logged in")
            ready_auth = CODEX.CommandResult(["true", "login", "status"], 0, "Logged in using ChatGPT", "")
            empty_credentials = {name: "" for name in CODEX.CREDENTIAL_ENV_NAMES}

            with patch.dict(os.environ, empty_credentials), patch.object(
                CODEX, "run_subprocess", side_effect=[version, missing_auth]
            ):
                missing_data = CODEX.collect_preflight(args)
            self.assertIn("missing_auth", missing_data["issues"])

            with patch.dict(os.environ, empty_credentials), patch.object(
                CODEX, "run_subprocess", side_effect=[version, ready_auth]
            ):
                ready_data = CODEX.collect_preflight(args)
            self.assertTrue(ready_data["ok"])
            self.assertEqual(ready_data["auth"]["method"], "codex-login-status")
            self.assertEqual(ready_data["model"]["model"], "gpt-5.6-sol")
            self.assertEqual(ready_data["model"]["effort"], "medium")

    def test_dry_runs_apply_the_expected_sandbox_and_prompt_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scenarios = (
                ("plan", [], "read-only", "medium"),
                ("edit", ["--mode", "edit", "--effort", "xhigh"], "workspace-write", "xhigh"),
                ("full", ["--full-access"], "danger-full-access", "medium"),
            )
            for name, extra, sandbox, effort in scenarios:
                with self.subTest(mode=name):
                    prompt = f"{name} private prompt"
                    args = CODEX.build_parser().parse_args(
                        [
                            "run",
                            "--codex-bin",
                            "/usr/bin/true",
                            "--cwd",
                            str(root),
                            "--prompt",
                            prompt,
                            "--dry-run",
                            *extra,
                        ]
                    )
                    delegated = CODEX.build_delegation_prompt(args.mode, prompt)
                    argv = CODEX.build_codex_argv(args, delegated, str(root / "last-message.txt"), mode=args.mode)
                    preview = CODEX.command_preview(argv, delegated)
                    self.assertEqual(argv[argv.index("--sandbox") + 1], sandbox)
                    self.assertIn(f'model_reasoning_effort="{effort}"', argv)
                    self.assertIn('approval_policy="never"', argv)
                    self.assertNotIn(prompt, preview)
                    if name == "edit":
                        self.assertIn("You are an editing delegate", delegated)
                        self.assertIn("Do not write outside the cwd", delegated)
                    elif name == "plan":
                        self.assertIn("do not write, edit, delete", delegated)

    def test_probe_requires_exact_ready_from_the_last_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            last_message = root / "last-message.txt"
            last_message.write_text("CODEX_READY.", encoding="utf-8")
            response = CODEX.extract_response_text(last_message, [], "")
            args = CODEX.build_parser().parse_args(
                ["probe", "--codex-bin", "/usr/bin/true", "--cwd", str(root)]
            )
            argv = CODEX.build_codex_argv(args, "Reply exactly CODEX_READY.", str(last_message), mode="read")

            self.assertTrue(CODEX.is_ready_response(response))
            self.assertFalse(CODEX.is_ready_response("READY"))
            self.assertIn("--output-last-message", argv)

    def test_edit_run_changes_only_the_project_and_writes_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "app.py"
            target.write_text("VALUE = 'broken'\n", encoding="utf-8")
            fake = make_executable(
                root,
                "codex",
                PREFLIGHT
                + LAST_MESSAGE_HELPER
                + """\
from pathlib import Path
Path("app.py").write_text("VALUE = 'fixed'\\n", encoding="utf-8")
Path(last_message_path()).write_text("Changed app.py and validation passed.", encoding="utf-8")
raise SystemExit(0)
""",
            )
            result = run_wrapper(
                SCRIPT,
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--mode",
                    "edit",
                    "--prompt",
                    "Change VALUE in app.py",
                    "--run-id",
                    "edit-artifacts",
                ],
            )
            data = payload(result)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(target.read_text(encoding="utf-8"), "VALUE = 'fixed'\n")
            self.assertEqual(data["result"]["response_text"], "Changed app.py and validation passed.")
            for name in ("stdout", "stderr", "meta", "last_message", "prompt_file"):
                self.assertTrue(Path(data["artifacts"][name]).exists())

    def test_reused_run_id_cannot_reuse_a_stale_last_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(CODEX, "git_status", return_value=""):
                first = CODEX.prepare_artifacts(root, "reused", "First")
                last_message = Path(first["last_message"])
                last_message.write_text("first answer", encoding="utf-8")
                second = CODEX.prepare_artifacts(root, "reused", "Second")

            reused_last_message = Path(second["last_message"])
            self.assertFalse(reused_last_message.exists())
            self.assertEqual(CODEX.extract_response_text(reused_last_message, [], ""), "")

if __name__ == "__main__":
    unittest.main()
