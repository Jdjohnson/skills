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


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "claude_delegate.py"


def make_fake_claude(directory: Path, body: str) -> Path:
    fake = directory / "claude"
    fake.write_text(textwrap.dedent(body), encoding="utf-8")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    return fake


def run_wrapper(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
        env=merged_env,
    )


class ClaudeDelegateTests(unittest.TestCase):
    def test_doctor_blocks_when_auth_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_claude(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("2.1.177 (Claude Code)")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "status", "--text"]:
                    print("Not logged in. Run claude auth login to authenticate.")
                    raise SystemExit(1)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(["doctor", "--claude-bin", str(fake), "--cwd", str(root)])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertFalse(payload["ok"])
            self.assertIn("claude_auth_missing", payload["issues"])
            self.assertEqual(payload["auth"]["method"], "missing")
            self.assertIn("require_escalated", payload["auth"]["codex_escalation_hint"])

    def test_doctor_accepts_environment_credential_without_printing_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_claude(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("2.1.177 (Claude Code)")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "status", "--text"]:
                    print("Not logged in. Run claude auth login to authenticate.")
                    raise SystemExit(1)
                raise SystemExit(9)
                """,
            )
            secret = "sk-ant-test-secret-value"
            result = run_wrapper(
                ["doctor", "--claude-bin", str(fake), "--cwd", str(root)],
                env={"ANTHROPIC_API_KEY": secret},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["auth"]["method"], "environment")
            self.assertIn("ANTHROPIC_API_KEY", payload["auth"]["env_credentials"])
            self.assertNotIn(secret, result.stdout)

    def test_default_discovery_checks_home_local_bin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            local_bin = root / ".local" / "bin"
            local_bin.mkdir(parents=True)
            fake = make_fake_claude(
                local_bin,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("2.1.177 (Claude Code)")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "status", "--text"]:
                    print("Logged in")
                    raise SystemExit(0)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(
                ["doctor", "--cwd", str(project)],
                env={"HOME": str(root), "PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["claude"]["path"], str(fake))

    def test_run_builds_safe_argv_and_parses_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            argv_file = root / "argv.json"
            fake = make_fake_claude(
                root,
                f"""\
                #!/usr/bin/env python3
                import json
                import sys
                from pathlib import Path
                if sys.argv[1:] == ["--version"]:
                    print("2.1.177 (Claude Code)")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "status", "--text"]:
                    print("Logged in")
                    raise SystemExit(0)
                Path({str(argv_file)!r}).write_text(json.dumps(sys.argv[1:]))
                print(json.dumps({{"type": "result", "session_id": "abc", "result": "done"}}))
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--claude-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--mode",
                    "plan",
                    "--prompt",
                    "Review this safely",
                    "--output-format",
                    "json",
                    "--max-turns",
                    "3",
                    "--allowed-tool",
                    "Bash(npm test)",
                ]
            )
            payload = json.loads(result.stdout)
            invoked = json.loads(argv_file.read_text(encoding="utf-8"))

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["result"]["json"]["result"], "done")
            self.assertIn("--permission-mode", invoked)
            self.assertEqual(invoked[invoked.index("--permission-mode") + 1], "dontAsk")
            self.assertIn("--safe-mode", invoked)
            self.assertIn("--model", invoked)
            self.assertEqual(invoked[invoked.index("--model") + 1], "opus")
            self.assertIn("--allowedTools", invoked)
            self.assertIn("Bash(npm test)", invoked[invoked.index("--allowedTools") + 1])
            self.assertTrue(any(item.startswith("<prompt:") for item in payload["command"]["argv"]))
            self.assertNotIn("Review this safely", result.stdout)

    def test_run_blocks_private_source_packet_before_cli_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = root / "called.txt"
            fake = make_fake_claude(
                root,
                f"""\
                #!/usr/bin/env python3
                import sys
                from pathlib import Path
                Path({str(marker)!r}).write_text("called")
                raise SystemExit(9)
                """,
            )
            private_prompt = (
                "Review PSB Bank ChatGPT Enterprise usage from raw CSV exports at "
                "/Users/jaradjohnson/Developer/ai-hub/Dot/projects/psb/source-material/2026-06/"
                "PSB Bank users export (2026-05-01 - 2026-05-31).csv"
            )
            result = run_wrapper(
                [
                    "run",
                    "--claude-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    private_prompt,
                ]
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["failure_kind"], "external_private_data_not_allowed")
            self.assertIn("external_private_data_not_allowed", payload["issues"])
            self.assertIn("source_material_path", payload["data_safety"]["findings"])
            self.assertFalse(marker.exists(), "Claude CLI should not be invoked for private external handoff")
            self.assertNotIn(private_prompt, result.stdout)

    def test_audit_prompt_allows_sanitized_aggregate_packet(self) -> None:
        result = run_wrapper(
            [
                "audit-prompt",
                "--data-classification",
                "sanitized",
                "--prompt",
                "Review anonymized aggregate metrics: active users 41 of 43 and total messages 4282.",
            ]
        )
        payload = json.loads(result.stdout)

        self.assertEqual(result.returncode, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["status"], "safe")

    def test_probe_requires_exact_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_claude(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("2.1.177 (Claude Code)")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "status", "--text"]:
                    print("Logged in")
                    raise SystemExit(0)
                print("READY")
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(["probe", "--claude-bin", str(fake), "--cwd", str(root)])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["probe"]["stdout"].strip(), "READY")
            self.assertIn("--no-session-persistence", payload["command"]["argv"])

    def test_unsafe_cwd_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_claude(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("2.1.177 (Claude Code)")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "status", "--text"]:
                    print("Logged in")
                    raise SystemExit(0)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(["doctor", "--claude-bin", str(fake), "--cwd", str(Path.home())])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertIn("cwd_too_broad", payload["issues"])

    def test_failure_classification_and_redaction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secret = "sk-ant-test-secret-value"
            fake = make_fake_claude(
                root,
                """\
                #!/usr/bin/env python3
                import os
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("2.1.177 (Claude Code)")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "status", "--text"]:
                    print("Logged in")
                    raise SystemExit(0)
                print(f"API Error: Request rejected (429) {os.environ['ANTHROPIC_API_KEY']}", file=sys.stderr)
                raise SystemExit(1)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--claude-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Do the thing",
                ],
                env={"ANTHROPIC_API_KEY": secret},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["failure_kind"], "rate_limit_or_quota")
            self.assertNotIn(secret, result.stdout)
            self.assertIn("<redacted:ANTHROPIC_API_KEY>", payload["result"]["stderr"])


if __name__ == "__main__":
    unittest.main()
