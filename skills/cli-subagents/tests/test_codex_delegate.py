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


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "codex_delegate.py"

FAKE_PREAMBLE = """\
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

FAKE_PREAMBLE_NO_AUTH = """\
#!/usr/bin/env python3
import json
import sys
if sys.argv[1:] == ["--version"]:
    print("codex-cli 0.142.3")
    raise SystemExit(0)
if sys.argv[1:] == ["login", "status"]:
    print("Not logged in", file=sys.stderr)
    raise SystemExit(1)
"""

FAKE_EXEC_HELPER = """\
def last_message_path():
    args = sys.argv[1:]
    return args[args.index("--output-last-message") + 1]
"""


def make_fake_codex(directory: Path, body: str) -> Path:
    fake = directory / "codex"
    fake.write_text(textwrap.dedent(body), encoding="utf-8")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    return fake


def run_wrapper(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    merged_env.pop("OPENAI_API_KEY", None)
    merged_env.pop("CODEX_API_KEY", None)
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
        env=merged_env,
    )


class CodexDelegateTests(unittest.TestCase):
    def test_doctor_blocks_when_auth_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_codex(root, FAKE_PREAMBLE_NO_AUTH + "raise SystemExit(9)\n")
            result = run_wrapper(["doctor", "--codex-bin", str(fake), "--cwd", str(root)])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertFalse(payload["ok"])
            self.assertIn("missing_auth", payload["issues"])
            self.assertEqual(payload["auth"]["method"], "missing")

    def test_doctor_ready_when_logged_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_codex(root, FAKE_PREAMBLE + "raise SystemExit(9)\n")
            result = run_wrapper(["doctor", "--codex-bin", str(fake), "--cwd", str(root)])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["auth"]["method"], "codex-login-status")
            self.assertEqual(payload["model"]["model"], "gpt-5.6-sol")
            self.assertEqual(payload["model"]["effort"], "medium")

    def test_default_discovery_uses_candidate_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            local_bin = root / ".local" / "bin"
            local_bin.mkdir(parents=True)
            fake = make_fake_codex(local_bin, FAKE_PREAMBLE + "raise SystemExit(9)\n")
            result = run_wrapper(
                ["doctor", "--cwd", str(project)],
                env={
                    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
                    "CODEX_DELEGATE_TEST_CANDIDATES": str(fake),
                },
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["codex"]["path"], str(fake))

    def test_run_dry_run_builds_safe_argv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_codex(root, FAKE_PREAMBLE + "raise SystemExit(42)\n")
            result = run_wrapper(
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Review this safely",
                    "--run-id",
                    "dry-run",
                    "--dry-run",
                ]
            )
            payload = json.loads(result.stdout)
            argv = payload["command"]["argv"]

            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "dry-run")
            self.assertEqual(argv[1], "exec")
            self.assertIn("--cd", argv)
            self.assertEqual(argv[argv.index("--cd") + 1], str(root))
            self.assertIn("--ephemeral", argv)
            self.assertIn("--ignore-user-config", argv)
            self.assertIn("--ignore-rules", argv)
            self.assertIn("--sandbox", argv)
            self.assertEqual(argv[argv.index("--sandbox") + 1], "read-only")
            self.assertIn("--model", argv)
            self.assertEqual(argv[argv.index("--model") + 1], "gpt-5.6-sol")
            self.assertIn('model_reasoning_effort="medium"', argv)
            self.assertIn('approval_policy="never"', argv)
            self.assertIn("--json", argv)
            self.assertIn("--output-last-message", argv)
            self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", argv)
            self.assertTrue(any(item.startswith("<prompt:") for item in argv))
            self.assertNotIn("Review this safely", result.stdout)
            prompt_text = Path(payload["artifacts"]["prompt_file"]).read_text(encoding="utf-8")
            self.assertIn("do not write, edit, delete", prompt_text)

    def test_edit_dry_run_uses_workspace_write_and_edit_preface(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_codex(root, FAKE_PREAMBLE + "raise SystemExit(42)\n")
            result = run_wrapper(
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--mode",
                    "edit",
                    "--effort",
                    "xhigh",
                    "--prompt",
                    "Fix the bug in app.py and run tests",
                    "--run-id",
                    "edit-dry-run",
                    "--dry-run",
                ]
            )
            payload = json.loads(result.stdout)
            argv = payload["command"]["argv"]
            prompt_text = Path(payload["artifacts"]["prompt_file"]).read_text(encoding="utf-8")

            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["mode"], "edit")
            self.assertEqual(payload["effort"], "xhigh")
            self.assertEqual(payload["status"], "dry-run")
            self.assertEqual(argv[argv.index("--sandbox") + 1], "workspace-write")
            self.assertIn('model_reasoning_effort="xhigh"', argv)
            self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", argv)
            self.assertNotIn("Fix the bug in app.py", result.stdout)
            self.assertIn("You are an editing delegate", prompt_text)
            self.assertIn("modify files only under the trusted cwd", prompt_text)
            self.assertIn("Do not write outside the cwd", prompt_text)

    def test_run_accepts_context_allowed_by_workspace_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = root / "called.txt"
            fake = make_fake_codex(
                root,
                FAKE_PREAMBLE
                + FAKE_EXEC_HELPER
                + textwrap.dedent(f"""\
                from pathlib import Path
                Path({str(marker)!r}).write_text("called")
                Path(last_message_path()).write_text("reviewed", encoding="utf-8")
                print('{{"type":"agent_message","message":"reviewed"}}')
                raise SystemExit(0)
                """),
            )
            private_prompt = (
                "Review internal project material at "
                "/projects/example/source-material/2026-06/users-export.csv"
            )
            result = run_wrapper(
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    private_prompt,
                    "--run-id",
                    "private-context",
                ]
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertTrue(marker.exists())
            self.assertNotIn(private_prompt, result.stdout)

    def test_audit_prompt_defers_to_workspace_policy(self) -> None:
        result = run_wrapper(
            [
                "audit-prompt",
                "--data-classification",
                "client-private",
                "--prompt",
                "Review the supplied internal context.",
            ]
        )
        payload = json.loads(result.stdout)

        self.assertEqual(result.returncode, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["status"], "safe")

    def test_explicit_full_access_uses_native_unrestricted_sandbox(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_codex(root, FAKE_PREAMBLE + "raise SystemExit(42)\n")
            result = run_wrapper(
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--full-access",
                    "--prompt",
                    "Inspect the isolated environment.",
                    "--dry-run",
                ]
            )
            payload = json.loads(result.stdout)
            argv = payload["command"]["argv"]

            self.assertEqual(result.returncode, 0)
            self.assertEqual(argv[argv.index("--sandbox") + 1], "danger-full-access")
            self.assertIn('approval_policy="never"', argv)

    def test_probe_requires_exact_ready_from_last_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_codex(
                root,
                FAKE_PREAMBLE
                + FAKE_EXEC_HELPER
                + textwrap.dedent("""\
                from pathlib import Path
                Path(last_message_path()).write_text("CODEX_READY.", encoding="utf-8")
                print(json.dumps({"type": "agent_message", "message": "CODEX_READY."}))
                raise SystemExit(0)
                """),
            )
            result = run_wrapper(["probe", "--codex-bin", str(fake), "--cwd", str(root), "--run-id", "probe"])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["probe"]["response_text"], "CODEX_READY.")
            self.assertIn("--json", payload["command"]["argv"])
            self.assertIn("--output-last-message", payload["command"]["argv"])

    def test_unsafe_cwd_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_codex(root, FAKE_PREAMBLE + "raise SystemExit(0)\n")
            result = run_wrapper(["doctor", "--codex-bin", str(fake), "--cwd", str(Path.home())])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertIn("cwd_too_broad", payload["issues"])

    def test_run_writes_artifacts_and_captures_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_codex(
                root,
                FAKE_PREAMBLE
                + FAKE_EXEC_HELPER
                + textwrap.dedent("""\
                from pathlib import Path
                Path(last_message_path()).write_text("done", encoding="utf-8")
                print(json.dumps({"type": "agent_message", "message": "done"}))
                print("stderr note", file=sys.stderr)
                raise SystemExit(0)
                """),
            )
            result = run_wrapper(
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Do the thing",
                    "--run-id",
                    "artifact-test",
                ]
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["result"]["response_text"], "done")
            stdout_path = Path(payload["artifacts"]["stdout"])
            stderr_path = Path(payload["artifacts"]["stderr"])
            meta_path = Path(payload["artifacts"]["meta"])
            last_message_path = Path(payload["artifacts"]["last_message"])
            self.assertIn('"done"', stdout_path.read_text(encoding="utf-8"))
            self.assertEqual(stderr_path.read_text(encoding="utf-8").strip(), "stderr note")
            self.assertEqual(last_message_path.read_text(encoding="utf-8"), "done")
            self.assertTrue(meta_path.exists())

    def test_reused_run_id_cannot_reuse_stale_last_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_codex(
                root,
                FAKE_PREAMBLE
                + FAKE_EXEC_HELPER
                + textwrap.dedent("""\
                from pathlib import Path
                Path(last_message_path()).write_text("first answer", encoding="utf-8")
                raise SystemExit(0)
                """),
            )
            first = run_wrapper(
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "First run",
                    "--run-id",
                    "reused",
                ]
            )
            self.assertEqual(first.returncode, 0)

            make_fake_codex(
                root,
                FAKE_PREAMBLE
                + textwrap.dedent("""\
                print(json.dumps({"type": "turn.completed", "usage": {}}))
                raise SystemExit(0)
                """),
            )
            second = run_wrapper(
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Second run",
                    "--run-id",
                    "reused",
                ]
            )
            payload = json.loads(second.stdout)

            self.assertEqual(second.returncode, 1)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["result"]["response_text"], "")

    def test_edit_mode_can_modify_project_file_and_captures_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "app.py"
            target.write_text("VALUE = 'broken'\n", encoding="utf-8")
            fake = make_fake_codex(
                root,
                FAKE_PREAMBLE
                + FAKE_EXEC_HELPER
                + textwrap.dedent("""\
                from pathlib import Path
                Path("app.py").write_text("VALUE = 'fixed'\\n", encoding="utf-8")
                Path(last_message_path()).write_text("Changed app.py and validation passed.", encoding="utf-8")
                raise SystemExit(0)
                """),
            )
            result = run_wrapper(
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--mode",
                    "edit",
                    "--prompt",
                    "Change VALUE to fixed in app.py",
                    "--run-id",
                    "edit-artifact-test",
                ]
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["mode"], "edit")
            self.assertEqual(target.read_text(encoding="utf-8"), "VALUE = 'fixed'\n")
            self.assertEqual(payload["result"]["response_text"], "Changed app.py and validation passed.")
            self.assertTrue(Path(payload["artifacts"]["stdout"]).exists())
            self.assertTrue(Path(payload["artifacts"]["stderr"]).exists())
            self.assertTrue(Path(payload["artifacts"]["meta"]).exists())

    def test_usage_limit_failure_classification_and_redaction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secret = "fake-codex-secret-value"
            fake = make_fake_codex(
                root,
                FAKE_PREAMBLE
                + textwrap.dedent("""\
                import os
                print(f"Error: usage limit reached {os.environ['OPENAI_API_KEY']}", file=sys.stderr)
                raise SystemExit(1)
                """),
            )
            result = run_wrapper(
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Do the thing",
                ],
                env={"OPENAI_API_KEY": secret},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["failure_kind"], "rate_limit_or_quota")
            self.assertNotIn(secret, result.stdout)
            self.assertIn("<redacted:OPENAI_API_KEY>", payload["result"]["stderr"])

    def test_timeout_is_classified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_codex(
                root,
                FAKE_PREAMBLE
                + textwrap.dedent("""\
                import time
                time.sleep(10)
                raise SystemExit(0)
                """),
            )
            result = run_wrapper(
                [
                    "run",
                    "--codex-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--timeout",
                    "2",
                    "--prompt",
                    "Do the thing",
                    "--run-id",
                    "timeout-test",
                ]
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 1)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["failure_kind"], "timeout")


if __name__ == "__main__":
    unittest.main()
