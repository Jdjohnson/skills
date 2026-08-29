from __future__ import annotations

import io
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from delegate_test_support import import_wrapper


CLAUDE = import_wrapper("claude_delegate")
CODEX = import_wrapper("codex_delegate")
GROK = import_wrapper("grok_delegate")
OPENCODE = import_wrapper("opencode_delegate")
COMMON = import_wrapper("_delegate_common")

PROVIDERS = (
    {
        "name": "claude",
        "module": CLAUDE,
        "secret": "ANTHROPIC_API_KEY",
    },
    {
        "name": "codex",
        "module": CODEX,
        "secret": "OPENAI_API_KEY",
    },
    {
        "name": "grok",
        "module": GROK,
        "secret": "XAI_API_KEY",
    },
)


class DelegateContractTests(unittest.TestCase):
    def test_run_directories_and_artifacts_are_private(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            common_artifacts = COMMON.prepare_artifacts(root, "cursor", "private", "prompt")
            COMMON.write_artifacts(
                common_artifacts,
                COMMON.CommandResult(["agent"], 0, "result", ""),
                {"cwd": str(root)},
            )
            artifact_sets = [common_artifacts]

            for module in (CODEX, GROK, OPENCODE):
                with self.subTest(provider=module.__name__), patch.object(
                    module, "git_status", return_value=""
                ):
                    artifacts = module.prepare_artifacts(root, "private", "prompt")
                    for key in ("stdout", "stderr", "meta", "git_status_after"):
                        module.write_text(Path(artifacts[key]), key)
                    artifact_sets.append(artifacts)

            for artifacts in artifact_sets:
                self.assertEqual(os.stat(artifacts["run_dir"]).st_mode & 0o777, 0o700)
                for path in map(Path, artifacts.values()):
                    if path.is_file():
                        self.assertEqual(os.stat(path).st_mode & 0o777, 0o600, str(path))

    def test_cursor_free_tier_named_model_error_is_classified(self) -> None:
        message = "Named models unavailable. Free plans can only use Auto."
        self.assertEqual(COMMON.classify_failure(1, "", message), "unsupported_account_tier")

    def test_wrappers_reject_broad_working_directories(self) -> None:
        for spec in PROVIDERS:
            with self.subTest(provider=spec["name"]):
                result = spec["module"].validate_cwd(str(Path.home()))
                self.assertFalse(result["ok"])
                self.assertIn("cwd_too_broad", result["issues"])

    def test_wrappers_redact_rate_limit_credentials(self) -> None:
        for spec in PROVIDERS:
            with self.subTest(provider=spec["name"]):
                secret = f"fake-{spec['name']}-secret-value"
                message = f"rate limit 429 {secret}"
                self.assertEqual(spec["module"].classify_failure(1, "", message), "rate_limit_or_quota")
                redacted = spec["module"].redact(message, {spec["secret"]: secret})
                self.assertNotIn(secret, redacted)
                self.assertIn(f"<redacted:{spec['secret']}>", redacted)

    def test_timeout_preserves_partial_output_and_all_providers_classify_it(self) -> None:
        timeout = subprocess.TimeoutExpired(
            cmd=["agent"], timeout=0.5, output=b"partial", stderr=b""
        )
        with patch.object(CLAUDE.subprocess, "run", side_effect=timeout):
            result = CLAUDE.run_subprocess(
                ["agent"],
                cwd=None,
                timeout=0.5,
            )

        self.assertEqual(result.returncode, 124)
        self.assertIn("partial", result.stdout)
        for spec in PROVIDERS:
            with self.subTest(provider=spec["name"]):
                failure = spec["module"].classify_failure(result.returncode, result.stdout, result.stderr)
                self.assertEqual(failure, "timeout")

    def test_wrappers_defer_prompt_policy_to_the_workspace(self) -> None:
        for spec in PROVIDERS:
            with self.subTest(provider=spec["name"]):
                output = io.StringIO()
                with redirect_stdout(output):
                    returncode = spec["module"].main(
                        [
                            "audit-prompt",
                            "--data-classification",
                            "client-private",
                            "--prompt",
                            "Review the supplied internal context.",
                        ]
                    )
                data = __import__("json").loads(output.getvalue())
                self.assertEqual(returncode, 0)
                self.assertTrue(data["ok"])
                self.assertEqual(data["status"], "safe")


if __name__ == "__main__":
    unittest.main()
