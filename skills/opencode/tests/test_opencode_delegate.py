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


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "opencode_delegate.py"


def make_fake_opencode(directory: Path, body: str) -> Path:
    fake = directory / "opencode"
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


class OpenCodeDelegateTests(unittest.TestCase):
    def test_doctor_blocks_when_auth_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "list"]:
                    print("No auth providers")
                    raise SystemExit(0)
                if sys.argv[1:] == ["models", "ollama-cloud"]:
                    print("ollama-cloud/glm-5.2")
                    raise SystemExit(0)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(["doctor", "--opencode-bin", str(fake), "--cwd", str(root)])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertFalse(payload["ok"])
            self.assertIn("opencode_auth_missing", payload["issues"])
            self.assertEqual(payload["auth"]["method"], "missing")

    def test_doctor_requires_ollama_cloud_model(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "list"]:
                    print("Ollama Cloud api")
                    raise SystemExit(0)
                if sys.argv[1:] == ["models", "ollama-cloud"]:
                    print("ollama-cloud/gpt-oss:20b-cloud")
                    raise SystemExit(0)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(["doctor", "--opencode-bin", str(fake), "--cwd", str(root)])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertFalse(payload["ok"])
            self.assertIn("model_missing", payload["issues"])
            self.assertNotIn("ollama-cloud/glm-5.2", payload["model"]["available"])

    def test_default_discovery_uses_candidate_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            local_bin = root / ".local" / "bin"
            local_bin.mkdir(parents=True)
            fake = make_fake_opencode(
                local_bin,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "list"]:
                    print("Ollama Cloud api")
                    raise SystemExit(0)
                if sys.argv[1:] == ["models", "ollama-cloud"]:
                    print("ollama-cloud/glm-5.2")
                    raise SystemExit(0)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(
                ["doctor", "--cwd", str(project)],
                env={
                    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
                    "OPENCODE_DELEGATE_TEST_CANDIDATES": str(fake),
                },
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["opencode"]["path"], str(fake))

    def test_run_dry_run_builds_safe_argv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "list"]:
                    print("Ollama Cloud api")
                    raise SystemExit(0)
                if sys.argv[1:] == ["models", "ollama-cloud"]:
                    print("ollama-cloud/glm-5.2")
                    raise SystemExit(0)
                raise SystemExit(42)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--opencode-bin",
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
            self.assertEqual(argv[1], "run")
            self.assertIn("--pure", argv)
            self.assertIn("--dir", argv)
            self.assertEqual(argv[argv.index("--dir") + 1], str(root))
            self.assertIn("--model", argv)
            self.assertEqual(argv[argv.index("--model") + 1], "ollama-cloud/glm-5.2")
            self.assertIn("--format", argv)
            self.assertEqual(argv[argv.index("--format") + 1], "json")
            self.assertNotIn("--dangerously-skip-permissions", argv)
            self.assertTrue(any(item.startswith("<prompt:") for item in argv))
            self.assertNotIn("Review this safely", result.stdout)
            prompt_text = Path(payload["artifacts"]["prompt_file"]).read_text(encoding="utf-8")
            self.assertIn("do not write, edit, delete", prompt_text)

    def test_edit_dry_run_builds_explicit_edit_prompt_and_safe_argv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "list"]:
                    print("Ollama Cloud api")
                    raise SystemExit(0)
                if sys.argv[1:] == ["models", "ollama-cloud"]:
                    print("ollama-cloud/glm-5.2")
                    raise SystemExit(0)
                raise SystemExit(42)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--opencode-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--mode",
                    "edit",
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
            self.assertEqual(payload["status"], "dry-run")
            self.assertEqual(argv[1], "run")
            self.assertIn("--pure", argv)
            self.assertIn("--dir", argv)
            self.assertEqual(argv[argv.index("--dir") + 1], str(root))
            self.assertIn("--model", argv)
            self.assertEqual(argv[argv.index("--model") + 1], "ollama-cloud/glm-5.2")
            self.assertIn("--format", argv)
            self.assertEqual(argv[argv.index("--format") + 1], "json")
            self.assertNotIn("--dangerously-skip-permissions", argv)
            self.assertTrue(any(item.startswith("<prompt:") for item in argv))
            self.assertNotIn("Fix the bug in app.py", result.stdout)
            self.assertIn("You are an editing delegate", prompt_text)
            self.assertIn("modify files only under the trusted cwd", prompt_text)
            self.assertIn("Do not write outside the cwd", prompt_text)

    def test_run_blocks_private_source_packet_before_cli_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = root / "called.txt"
            fake = make_fake_opencode(
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
                    "--opencode-bin",
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
            self.assertFalse(marker.exists(), "OpenCode CLI should not be invoked for private external handoff")
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

    def test_probe_requires_exact_ready_from_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import json
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "list"]:
                    print("Ollama Cloud api")
                    raise SystemExit(0)
                if sys.argv[1:] == ["models", "ollama-cloud"]:
                    print("ollama-cloud/glm-5.2")
                    raise SystemExit(0)
                print(json.dumps({"type": "step_start", "part": {"type": "step-start"}}))
                print(json.dumps({"type": "text", "part": {"type": "text", "text": "OPENCODE_READY."}}))
                print(json.dumps({"type": "step_finish", "part": {"type": "step-finish", "reason": "stop"}}))
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(["probe", "--opencode-bin", str(fake), "--cwd", str(root), "--run-id", "probe"])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["probe"]["response_text"], "OPENCODE_READY.")
            self.assertIn("--pure", payload["command"]["argv"])
            self.assertIn("--format", payload["command"]["argv"])

    def test_unsafe_cwd_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(["doctor", "--opencode-bin", str(fake), "--cwd", str(Path.home())])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertIn("cwd_too_broad", payload["issues"])

    def test_run_writes_artifacts_and_captures_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import json
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "list"]:
                    print("Ollama Cloud api")
                    raise SystemExit(0)
                if sys.argv[1:] == ["models", "ollama-cloud"]:
                    print("ollama-cloud/glm-5.2")
                    raise SystemExit(0)
                print(json.dumps({"text": "done"}))
                print("stderr note", file=sys.stderr)
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--opencode-bin",
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
            self.assertIn('"done"', stdout_path.read_text(encoding="utf-8"))
            self.assertEqual(stderr_path.read_text(encoding="utf-8").strip(), "stderr note")
            self.assertTrue(meta_path.exists())

    def test_edit_mode_can_modify_project_file_and_captures_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "app.py"
            target.write_text("VALUE = 'broken'\n", encoding="utf-8")
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import json
                import sys
                from pathlib import Path
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "list"]:
                    print("Ollama Cloud api")
                    raise SystemExit(0)
                if sys.argv[1:] == ["models", "ollama-cloud"]:
                    print("ollama-cloud/glm-5.2")
                    raise SystemExit(0)
                Path("app.py").write_text("VALUE = 'fixed'\\n", encoding="utf-8")
                print(json.dumps({"text": "Changed app.py and validation passed."}))
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--opencode-bin",
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

    def test_json_cancelled_result_is_not_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import json
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "list"]:
                    print("Ollama Cloud api")
                    raise SystemExit(0)
                if sys.argv[1:] == ["models", "ollama-cloud"]:
                    print("ollama-cloud/glm-5.2")
                    raise SystemExit(0)
                print(json.dumps({"text": "", "stopReason": "Cancelled"}))
                raise SystemExit(0)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--opencode-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Plan the thing",
                    "--run-id",
                    "cancelled-json",
                ]
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 1)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["failure_kind"], "cancelled")
            self.assertEqual(payload["status"], "blocked")

    def test_state_schema_failure_classification_and_redaction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secret = "ollama-secret-value"
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import os
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] == ["auth", "list"]:
                    print("Ollama Cloud api")
                    raise SystemExit(0)
                if sys.argv[1:] == ["models", "ollama-cloud"]:
                    print("ollama-cloud/glm-5.2")
                    raise SystemExit(0)
                print(f"SqliteError: no such column: name {os.environ['OLLAMA_API_KEY']}", file=sys.stderr)
                raise SystemExit(1)
                """,
            )
            result = run_wrapper(
                [
                    "run",
                    "--opencode-bin",
                    str(fake),
                    "--cwd",
                    str(root),
                    "--prompt",
                    "Do the thing",
                ],
                env={"OLLAMA_API_KEY": secret},
            )
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["failure_kind"], "state_schema_incompatible")
            self.assertNotIn(secret, result.stdout)
            self.assertIn("<redacted:OLLAMA_API_KEY>", payload["result"]["stderr"])

    def test_opencode_global_log_sandbox_error_is_classified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = make_fake_opencode(
                root,
                """\
                #!/usr/bin/env python3
                import sys
                if sys.argv[1:] == ["--version"]:
                    print("1.17.5")
                    raise SystemExit(0)
                if sys.argv[1:] in (["auth", "list"], ["models", "ollama-cloud"]):
                    print("Unknown: FileSystem.open (/home/example/.local/share/opencode/log/opencode.log)", file=sys.stderr)
                    raise SystemExit(1)
                raise SystemExit(9)
                """,
            )
            result = run_wrapper(["doctor", "--opencode-bin", str(fake), "--cwd", str(root)])
            payload = json.loads(result.stdout)

            self.assertEqual(result.returncode, 2)
            self.assertFalse(payload["ok"])
            self.assertIn("network_or_sandbox", payload["issues"])
            self.assertNotIn("opencode_auth_missing", payload["issues"])


if __name__ == "__main__":
    unittest.main()
