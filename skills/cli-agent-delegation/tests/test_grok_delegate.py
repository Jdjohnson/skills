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


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "grok_delegate.py"
GROK = import_wrapper("grok_delegate")

PREFLIGHT = """\
#!/usr/bin/env python3
import json
import sys
if sys.argv[1:] == ["--version"]:
    print("grok 0.2.51")
    raise SystemExit(0)
if sys.argv[1:] == ["inspect", "--json"]:
    print('{"config":"ok"}')
    raise SystemExit(0)
if sys.argv[1:] == ["models"]:
    print("grok-build-0.1")
    raise SystemExit(0)
"""

class GrokDelegateTests(unittest.TestCase):
    def test_doctor_requires_proven_auth_or_a_redacted_environment_credential(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = GROK.build_parser().parse_args(
                ["doctor", "--grok-bin", "/usr/bin/true", "--cwd", str(root)]
            )
            version = GROK.CommandResult(["true", "--version"], 0, "grok 0.2.51", "")
            inspect_missing = GROK.CommandResult(["true", "inspect", "--json"], 1, "", "Not logged in")
            inspect_ready = GROK.CommandResult(["true", "inspect", "--json"], 0, '{"config":"ok"}', "")
            unknown_models = GROK.CommandResult(["true", "models"], 9, "", "")
            unauthenticated_models = GROK.CommandResult(
                ["true", "models"], 1, "", "Not logged in. Run grok login."
            )
            misleading_zero_models = GROK.CommandResult(
                ["true", "models"], 0, "You are not authenticated.\ngrok-build-0.1", ""
            )
            empty_credentials = {name: "" for name in GROK.CREDENTIAL_ENV_NAMES}

            with patch.dict(os.environ, empty_credentials), patch.object(
                GROK, "run_subprocess", side_effect=[version, inspect_missing, unknown_models]
            ):
                missing = GROK.collect_preflight(args)
            self.assertIn("grok_auth_missing", missing["issues"])

            with patch.dict(os.environ, empty_credentials), patch.object(
                GROK, "run_subprocess", side_effect=[version, inspect_ready, unauthenticated_models]
            ):
                inspect = GROK.collect_preflight(args)
            self.assertIn("not_authenticated", inspect["issues"])

            with patch.dict(os.environ, empty_credentials), patch.object(
                GROK, "run_subprocess", side_effect=[version, inspect_ready, misleading_zero_models]
            ):
                misleading = GROK.collect_preflight(args)
            self.assertIn("not_authenticated", misleading["issues"])

            secret = "fake-grok-secret-value"
            with patch.dict(os.environ, empty_credentials | {"XAI_API_KEY": secret}), patch.object(
                GROK, "run_subprocess", side_effect=[version, inspect_missing, unknown_models]
            ):
                ready_data = GROK.collect_preflight(args)
            self.assertTrue(ready_data["ok"])
            self.assertEqual(ready_data["auth"]["method"], "environment")
            self.assertNotIn(secret, json.dumps(ready_data))

    def test_dry_runs_apply_safe_defaults_and_explicit_tool_opt_ins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            default_args = GROK.build_parser().parse_args(
                [
                    "run",
                    "--grok-bin",
                    "/usr/bin/true",
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Review this safely",
                    "--dry-run",
                ]
            )
            _, default_policy = GROK.grok_env(default_args)
            default_argv = GROK.build_grok_argv(default_args, "<prompt-file>")
            self.assertEqual(default_argv[default_argv.index("--permission-mode") + 1], "auto")
            self.assertEqual(default_argv[default_argv.index("--sandbox") + 1], "read-only")
            self.assertIn("--deny", default_argv)
            self.assertIn("--no-subagents", default_argv)
            self.assertIn("--disable-web-search", default_argv)
            self.assertEqual(default_policy["GROK_CLAUDE_SKILLS_ENABLED"], "false")

            opted_args = GROK.build_parser().parse_args(
                [
                    "run",
                    "--grok-bin",
                    "/usr/bin/true",
                    "--cwd",
                    str(root),
                    "--mode",
                    "edit",
                    "--prompt",
                    "Use optional tools",
                    "--dry-run",
                    "--allow-mcp",
                    "--allow-subagents",
                    "--allow-web",
                    "--compat",
                    "all",
                ]
            )
            _, opted_policy = GROK.grok_env(opted_args)
            opted_argv = GROK.build_grok_argv(opted_args, "<prompt-file>")
            self.assertEqual(opted_argv[opted_argv.index("--sandbox") + 1], "workspace")
            self.assertNotIn("MCPTool(*)", opted_argv)
            self.assertNotIn("--no-subagents", opted_argv)
            self.assertNotIn("--disable-web-search", opted_argv)
            self.assertEqual(opted_policy, {})

    def test_successful_run_writes_output_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_executable(
                root,
                "grok",
                PREFLIGHT
                + """\
print("done")
print("stderr note", file=sys.stderr)
raise SystemExit(0)
""",
            )
            result = run_wrapper(
                SCRIPT,
                ["run", "--grok-bin", str(fake), "--cwd", str(root), "--prompt", "Do the thing", "--run-id", "artifacts"],
            )
            data = payload(result)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(data["result"]["stdout"].strip(), "done")
            self.assertEqual(Path(data["artifacts"]["stdout"]).read_text(encoding="utf-8").strip(), "done")
            self.assertEqual(Path(data["artifacts"]["stderr"]).read_text(encoding="utf-8").strip(), "stderr note")
            self.assertTrue(Path(data["artifacts"]["meta"]).exists())

    def test_probe_requires_the_exact_ready_response(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = GROK.build_parser().parse_args(
                ["probe", "--grok-bin", "/usr/bin/true", "--cwd", str(root), "--run-id", "probe"]
            )
            preflight = {"ok": True, "cwd": {"path": str(root)}}
            artifacts = {
                "prompt_file": str(root / "prompt.md"),
                "stdout": str(root / "stdout.log"),
                "stderr": str(root / "stderr.log"),
                "meta": str(root / "meta.json"),
                "git_status_after": str(root / "git-status-after.txt"),
            }

            results = []
            for response in ("GROK_READY", "READY"):
                output = io.StringIO()
                completed = GROK.CommandResult(["true"], 0, response, "")
                with patch.object(GROK, "collect_preflight", return_value=preflight.copy()), patch.object(
                    GROK, "prepare_artifacts", return_value=artifacts
                ), patch.object(
                    GROK, "run_subprocess", return_value=completed
                ), patch.object(GROK, "write_result_artifacts"), redirect_stdout(output):
                    returncode = GROK.do_probe(args)
                results.append((returncode, json.loads(output.getvalue())))

            ready_code, ready_data = results[0]
            wrong_code, wrong_data = results[1]
            self.assertEqual(ready_code, 0)
            self.assertEqual(ready_data["probe"]["stdout"], "GROK_READY")
            self.assertIn("--disable-web-search", ready_data["command"]["argv"])
            self.assertIn("--no-subagents", ready_data["command"]["argv"])
            self.assertEqual(wrong_code, 1)
            self.assertEqual(wrong_data["status"], "blocked")

    def test_cancelled_json_is_not_success(self) -> None:
        parsed = GROK.parse_json_output(json.dumps({"text": "", "stopReason": "Cancelled"}))
        self.assertEqual(GROK.semantic_json_failure(parsed), "cancelled")
        self.assertIsNone(GROK.classify_failure(0, json.dumps(parsed), ""))

if __name__ == "__main__":
    unittest.main()
