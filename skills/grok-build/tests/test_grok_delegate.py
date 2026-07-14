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


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "grok_delegate.py"


def make_fake_grok(directory: Path, body: str) -> Path:
    fake = directory / "grok"
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


class GrokDelegateTests(unittest.TestCase):
    def test_doctor_blocks_when_auth_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_grok(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                if sys.argv[1:] == ["inspect", "--json"]:
                    print("Not logged in. Run grok login.", file=sys.stderr)
                    raise SystemExit(1)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(["doctor", "--grok-bin", str(fake), "--cwd", str(root)])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertFalse(payload["ok"])
            self.assertIn("grok_auth_missing", payload["issues"])
            self.assertEqual(payload["auth"]["method"], "missing")

    def test_doctor_accepts_environment_credential_without_printing_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_grok(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                if sys.argv[1:] == ["inspect", "--json"]:
                    print("Not logged in. Run grok login.", file=sys.stderr)
                    raise SystemExit(1)
                raise SystemExit(9)
                """,
            )
            secret = "fake-grok-secret-value"
            result = run_wrapper(
                ["doctor", "--grok-bin", str(fake), "--cwd", str(root)],
                env={"XAI_API_KEY": secret},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["auth"]["method"], "environment")
            self.assertIn("XAI_API_KEY", payload["auth"]["env_credentials"])
            self.assertNotIn(secret, result.stdout)

    def test_default_discovery_uses_candidate_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            local_bin = root / ".grok" / "bin"
            local_bin.mkdir(parents=True)
            fake = make_fake_grok(
                local_bin,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                if sys.argv[1:] == ["inspect", "--json"]:
                    print('{"config": "ok"}')
                    raise SystemExit(0)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(
                ["doctor", "--cwd", str(project)],
                env={
                    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
                    "GROK_BUILD_TEST_CANDIDATES": str(fake),
                },
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["grok"]["path"], str(fake))

    def test_run_dry_run_builds_safe_argv_and_env_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_grok(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                if sys.argv[1:] == ["inspect", "--json"]:
                    print('{"config": "ok"}')
                    raise SystemExit(0)
                raise SystemExit(42)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--grok-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Review this safely",
                    "--run-id",
                    "dry-run",
                    "--dry-run",
                ],
                env={"XAI_API_KEY": "xai-secret-value"},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "dry-run")
            self.assertIn("--prompt-file", payload["command"]["argv"])
            self.assertNotIn("Review this safely", result.stdout)
            self.assertEqual(payload["env_policy"]["GROK_CLAUDE_SKILLS_ENABLED"], "false")
            self.assertIn("--deny", payload["command"]["argv"])
            self.assertIn("--model", payload["command"]["argv"])
            self.assertEqual(
                payload["command"]["argv"][payload["command"]["argv"].index("--permission-mode") + 1],
                "dontAsk",
            )
            self.assertEqual(
                payload["command"]["argv"][payload["command"]["argv"].index("--model") + 1],
                "grok-4.5",
            )

    def test_run_blocks_private_source_packet_before_cli_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = root / "called.txt"
            fake = make_fake_grok(
                root,
                f"""\
                #!/usr/bin/env python3
                from pathlib import Path
                Path({str(marker)!r}).write_text("called")
                raise SystemExit(9)
                """,
            )
            private_prompt = (
                "Review a client usage export from raw CSV files at "
                "/projects/example/source-material/2026-06/users-export.csv"
            )
            result = run_wrapper(
                [
                    "run",
                    "--grok-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    private_prompt,
                    "--run-id",
                    "private-block",
                    "--dry-run",
                ]
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["failure_kind"], "external_private_data_not_allowed")
            self.assertIn("external_private_data_not_allowed", payload["issues"])
            self.assertIn("source_material_path", payload["data_safety"]["findings"])
            self.assertFalse(marker.exists(), "Grok CLI should not be invoked for private external handoff")
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

    def test_edit_mode_uses_headless_write_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_grok(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                if sys.argv[1:] == ["inspect", "--json"]:
                    print('{"config": "ok"}')
                    raise SystemExit(0)
                raise SystemExit(42)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--grok-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--mode",
                    "edit",
                    "--prompt",
                    "Patch the file",
                    "--run-id",
                    "edit-permissions",
                    "--dry-run",
                ]
            )
            payload = json.loads(result.stdout)
            argv = payload["command"]["argv"]

            self.assertEqual(result.returncode, 0)
            self.assertIn("--permission-mode", argv)
            self.assertEqual(argv[argv.index("--permission-mode") + 1], "bypassPermissions")
            self.assertIn("--always-approve", argv)

    def test_run_writes_artifacts_and_captures_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_grok(
                root,
                """\
                #!/usr/bin/env python3
                import os
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                if sys.argv[1:] == ["inspect", "--json"]:
                    print('{"config": "ok"}')
                    raise SystemExit(0)
                print("done")
                print("stderr note", file=sys.stderr)
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--grok-bin",
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
            self.assertEqual(payload["result"]["stdout"].strip(), "done")
            stdout_path = Path(payload["artifacts"]["stdout"])
            stderr_path = Path(payload["artifacts"]["stderr"])
            meta_path = Path(payload["artifacts"]["meta"])
            self.assertEqual(stdout_path.read_text(encoding="utf-8").strip(), "done")
            self.assertEqual(stderr_path.read_text(encoding="utf-8").strip(), "stderr note")
            self.assertTrue(meta_path.exists())

    def test_json_cancelled_result_is_not_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_grok(
                root,
                """\
                #!/usr/bin/env python3
                import json
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                if sys.argv[1:] == ["inspect", "--json"]:
                    print('{"config": "ok"}')
                    raise SystemExit(0)
                print(json.dumps({"text": "", "stopReason": "Cancelled"}))
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--grok-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Plan the thing",
                    "--output-format",
                    "json",
                    "--run-id",
                    "cancelled-json",
                ]
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 1)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["failure_kind"], "cancelled")
            self.assertEqual(payload["status"], "blocked")

    def test_probe_requires_exact_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_grok(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                if sys.argv[1:] == ["inspect", "--json"]:
                    print('{"config": "ok"}')
                    raise SystemExit(0)
                print("GROK_READY")
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(["probe", "--grok-bin", str(fake), "--cwd", str(root), "--run-id", "probe"])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["probe"]["stdout"].strip(), "GROK_READY")
            self.assertIn("--disable-web-search", payload["command"]["argv"])
            self.assertIn("--no-subagents", payload["command"]["argv"])

    def test_unsafe_cwd_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_grok(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(["doctor", "--grok-bin", str(fake), "--cwd", str(Path.home())])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertIn("cwd_too_broad", payload["issues"])

    def test_allow_mcp_and_subagents_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_grok(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                if sys.argv[1:] == ["inspect", "--json"]:
                    print('{"config": "ok"}')
                    raise SystemExit(0)
                raise SystemExit(42)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--grok-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Use optional tools",
                    "--run-id",
                    "opts",
                    "--dry-run",
                    "--allow-mcp",
                    "--allow-subagents",
                    "--allow-web",
                    "--compat",
                    "all",
                ],
                env={"XAI_API_KEY": "xai-secret-value"},
            )
            payload = json.loads(result.stdout)
            argv = payload["command"]["argv"]

            self.assertEqual(result.returncode, 0)
            self.assertNotIn("MCPTool(*)", argv)
            self.assertNotIn("--no-subagents", argv)
            self.assertNotIn("--disable-web-search", argv)
            self.assertEqual(payload["env_policy"], {})

    def test_failure_classification_and_redaction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secret = "fake-grok-secret-value"
            fake = make_fake_grok(
                root,
                """\
                #!/usr/bin/env python3
                import os
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("grok 0.2.51")
                    raise SystemExit(0)
                if sys.argv[1:] == ["inspect", "--json"]:
                    print('{"config": "ok"}')
                    raise SystemExit(0)
                print(f"rate limit 429 {os.environ['XAI_API_KEY']}", file=sys.stderr)
                raise SystemExit(1)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--grok-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Do the thing",
                ],
                env={"XAI_API_KEY": secret},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["failure_kind"], "rate_limit_or_quota")
            self.assertNotIn(secret, result.stdout)
            self.assertIn("<redacted:XAI_API_KEY>", payload["result"]["stderr"])


if __name__ == "__main__":
    unittest.main()
