from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import google_oauth  # noqa: E402


class GoogleOAuthTests(unittest.TestCase):
    def setUp(self) -> None:
        google_oauth.clear_access_token_cache()

    def tearDown(self) -> None:
        google_oauth.clear_access_token_cache()

    @patch.object(google_oauth, "refresh_token_payload")
    def test_build_gws_env_reuses_access_token_in_process(self, refresh: MagicMock) -> None:
        refresh.return_value = {
            "access_token": "test-access-token",
            "expires_in": 3600,
            "scopes": ["scope-a"],
        }

        first_env, first_payload = google_oauth.build_gws_env(["scope-a"])
        second_env, second_payload = google_oauth.build_gws_env(["scope-a"])

        self.assertEqual(first_env[google_oauth.DEFAULT_TOKEN_VAR], "test-access-token")
        self.assertEqual(second_env[google_oauth.DEFAULT_TOKEN_VAR], "test-access-token")
        self.assertIs(first_payload, second_payload)
        refresh.assert_called_once_with({"scope-a"})

    @patch.object(google_oauth, "refresh_token_payload")
    def test_cache_refreshes_when_new_scope_is_required(self, refresh: MagicMock) -> None:
        refresh.side_effect = [
            {"access_token": "token-a", "expires_in": 3600, "scopes": ["scope-a"]},
            {
                "access_token": "token-ab",
                "expires_in": 3600,
                "scopes": ["scope-a", "scope-b"],
            },
        ]

        google_oauth.build_gws_env(["scope-a"])
        env, _ = google_oauth.build_gws_env(["scope-a", "scope-b"])

        self.assertEqual(env[google_oauth.DEFAULT_TOKEN_VAR], "token-ab")
        self.assertEqual(refresh.call_count, 2)

    @patch.object(google_oauth.time, "sleep")
    @patch.object(google_oauth.urllib.request, "urlopen")
    def test_refresh_retries_one_transient_timeout(
        self, urlopen: MagicMock, sleep: MagicMock
    ) -> None:
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            {"access_token": "fresh-token", "expires_in": 3600}
        ).encode()
        urlopen.side_effect = [TimeoutError("temporary timeout"), response]
        bundle = google_oauth.TokenBundle(
            source=google_oauth.TokenSource("test", Path("/tmp/test-token.json")),
            refresh_token="refresh",
            client_id="client",
            client_secret="secret",
            token_uri="https://oauth2.example.test/token",
            scopes={"scope-a"},
        )

        payload = google_oauth.refresh_access_token(bundle, timeout=1)

        self.assertEqual(payload["access_token"], "fresh-token")
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(google_oauth.TOKEN_REFRESH_RETRY_DELAY_SECONDS)

    def test_token_bundle_rejects_group_readable_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            token_path = Path(directory) / "token.json"
            token_path.write_text(
                json.dumps(
                    {
                        "refresh_token": "refresh",
                        "client_id": "client",
                        "client_secret": "secret",
                        "scopes": ["scope-a"],
                    }
                )
            )
            os.chmod(token_path, 0o644)

            with patch.object(google_oauth, "CANONICAL_TOKEN_PATH", token_path):
                with self.assertRaisesRegex(RuntimeError, "insecure permissions 0644"):
                    google_oauth.load_token_bundle()

    @patch.object(google_oauth, "refresh_access_token")
    def test_access_token_is_persisted_and_reused_across_process_caches(
        self, refresh: MagicMock
    ) -> None:
        refresh.return_value = {
            "source": "gws-full",
            "token_path": "/tmp/token.json",
            "access_token": "fresh-token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scopes": ["scope-a"],
        }
        with tempfile.TemporaryDirectory() as directory:
            token_path = Path(directory) / "token.json"
            token_path.write_text(
                json.dumps(
                    {
                        "refresh_token": "refresh",
                        "client_id": "client",
                        "client_secret": "secret",
                        "scopes": ["scope-a"],
                    }
                )
            )
            os.chmod(token_path, 0o600)

            with patch.object(google_oauth, "CANONICAL_TOKEN_PATH", token_path):
                first = google_oauth.access_token_payload(["scope-a"])
                google_oauth.clear_access_token_cache()
                second = google_oauth.access_token_payload(["scope-a"])

            self.assertEqual(first["access_token"], "fresh-token")
            self.assertEqual(second["access_token"], "fresh-token")
            refresh.assert_called_once()
            persisted = json.loads(token_path.read_text())
            self.assertEqual(persisted["token"], "fresh-token")
            self.assertIn("expiry", persisted)
            self.assertEqual(os.stat(token_path).st_mode & 0o777, 0o600)

    @patch.object(google_oauth.time, "sleep")
    @patch.object(google_oauth.subprocess, "run")
    @patch.object(google_oauth, "build_gws_env")
    def test_read_command_retries_transient_gws_failures(
        self, build_env: MagicMock, run: MagicMock, sleep: MagicMock
    ) -> None:
        build_env.return_value = ({}, {"access_token": "hidden"})
        run.side_effect = [
            subprocess.CompletedProcess([], 1, "", "error: HTTP request failed"),
            subprocess.CompletedProcess([], 1, "", "error: HTTP request failed"),
            subprocess.CompletedProcess([], 0, "{}", ""),
        ]

        result = google_oauth.run_gws(["gmail", "users", "threads", "list"])

        self.assertEqual(result, "{}")
        self.assertEqual(run.call_count, 3)
        self.assertEqual(
            sleep.call_args_list,
            [
                unittest.mock.call(google_oauth.GWS_RETRY_DELAY_SECONDS),
                unittest.mock.call(google_oauth.GWS_RETRY_DELAY_SECONDS * 2),
            ],
        )

    @patch.object(google_oauth.time, "sleep")
    @patch.object(google_oauth.subprocess, "run")
    @patch.object(google_oauth, "build_gws_env")
    def test_mutation_command_does_not_retry_ambiguous_transport_failure(
        self, build_env: MagicMock, run: MagicMock, sleep: MagicMock
    ) -> None:
        build_env.return_value = ({}, {"access_token": "hidden"})
        run.return_value = subprocess.CompletedProcess(
            [], 1, "", "error: HTTP request failed"
        )

        with self.assertRaisesRegex(RuntimeError, "HTTP request failed"):
            google_oauth.run_gws(["gmail", "users", "threads", "modify"])

        run.assert_called_once()
        sleep.assert_not_called()

    @patch.object(google_oauth.time, "sleep")
    @patch.object(google_oauth.subprocess, "run")
    @patch.object(google_oauth, "build_gws_env")
    def test_idempotent_mutation_can_opt_into_transient_retries(
        self, build_env: MagicMock, run: MagicMock, sleep: MagicMock
    ) -> None:
        build_env.return_value = ({}, {"access_token": "hidden"})
        run.side_effect = [
            subprocess.CompletedProcess([], 1, "", "error: HTTP request failed"),
            subprocess.CompletedProcess([], 0, "{}", ""),
        ]

        result = google_oauth.run_gws(
            ["gmail", "users", "threads", "modify"], retry_transient=True
        )

        self.assertEqual(result, "{}")
        self.assertEqual(run.call_count, 2)
        sleep.assert_called_once_with(google_oauth.GWS_RETRY_DELAY_SECONDS)


if __name__ == "__main__":
    unittest.main()
