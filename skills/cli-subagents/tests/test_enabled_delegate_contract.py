from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from delegate_test_support import import_wrapper


CLAUDE = import_wrapper("claude_delegate")
CODEX = import_wrapper("codex_delegate")
GROK = import_wrapper("grok_delegate")
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

    def test_one_real_timeout_preserves_partial_output_and_all_providers_classify_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = CLAUDE.run_subprocess(
                [
                    sys.executable,
                    "-c",
                    "import sys,time; sys.stdout.write('partial'); sys.stdout.flush(); time.sleep(5)",
                ],
                cwd=Path(tmp),
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
