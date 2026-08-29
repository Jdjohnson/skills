from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "manus_delegate.py"
SECRET = "manus-test-secret-value"


class FakeManusHandler(BaseHTTPRequestHandler):
    requests: list[dict[str, object]] = []
    task_status = "stopped"
    startup_waiting_once = False
    startup_not_found_once = False
    detail_calls = 0
    followup_sent = False
    followup_result_delay_once = False
    followup_message_calls = 0

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send(self, payload: dict[str, object], status: int = 200) -> None:
        raw = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _record(self, body: dict[str, object] | None = None) -> None:
        self.__class__.requests.append({"method": self.command, "path": self.path, "key": self.headers.get("x-manus-api-key"), "body": body})

    def do_GET(self) -> None:
        self._record()
        if self.path.startswith("/v2/usage.availableCredits"):
            self._send({"ok": True, "total_credits": 88813, "addon_credits": 75300})
        elif self.path.startswith("/v2/task.detail"):
            self.__class__.detail_calls += 1
            if self.__class__.startup_not_found_once and self.__class__.detail_calls == 1:
                self._send({"ok": False, "error": {"code": "not_found", "message": "task not found"}}, 404)
                return
            status = "waiting" if self.__class__.startup_waiting_once and self.__class__.detail_calls == 1 else self.__class__.task_status
            self._send({"ok": True, "task": {"id": "task-1", "status": status, "credit_usage": 12}})
        elif self.path.startswith("/v2/task.listMessages"):
            events = [{"id": "message-1", "assistant_message": {"content": "MANUS_READY"}}]
            if self.__class__.followup_sent:
                self.__class__.followup_message_calls += 1
                events.append({"id": "message-user-2", "user_message": {"content": "Move to phase two"}})
                events.append({"id": "message-running-2", "status_update": {"agent_status": "running"}})
                if not self.__class__.followup_result_delay_once or self.__class__.followup_message_calls > 1:
                    events.append({"id": "message-2", "assistant_message": {"content": "PHASE_TWO_OK"}})
            self._send({"ok": True, "task_id": "task-1", "messages": events, "has_more": False})
        else:
            self._send({"ok": False, "error": {"code": "not_found", "message": "missing"}}, 404)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length) or b"{}")
        self._record(body)
        if self.path == "/v2/task.create":
            self._send({"ok": True, "task_id": "task-1", "task_url": "https://manus.im/app/task-1"})
        elif self.path == "/v2/task.sendMessage":
            self.__class__.followup_sent = True
            self._send({"ok": True, "task_id": "task-1"})
        elif self.path == "/v2/task.stop":
            self._send({"ok": True, "request_id": "req-1"})
        else:
            self._send({"ok": False, "error": {"code": "not_found", "message": "missing"}}, 404)


class FakeServer:
    def __enter__(self) -> "FakeServer":
        FakeManusHandler.requests = []
        FakeManusHandler.task_status = "stopped"
        FakeManusHandler.startup_waiting_once = False
        FakeManusHandler.startup_not_found_once = False
        FakeManusHandler.detail_calls = 0
        FakeManusHandler.followup_sent = False
        FakeManusHandler.followup_result_delay_once = False
        FakeManusHandler.followup_message_calls = 0
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeManusHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        return self

    def __exit__(self, *args: object) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()


def run_wrapper(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    merged.pop("MANUS_API_KEY", None)
    merged.pop("MANUS_ENV_PATH", None)
    if env:
        merged.update(env)
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False, env=merged)


class ManusDelegateTests(unittest.TestCase):
    def test_doctor_loads_env_file_and_reports_credits_without_secret(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            root = Path(tmp)
            env_file = root / ".env.local"
            env_file.write_text(f"MANUS_API_KEY={SECRET}\n")
            result = run_wrapper(["doctor", "--cwd", str(root), "--base-url", server.url])
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["credits"]["total_credits"], 88813)
            self.assertNotIn(SECRET, result.stdout)
            self.assertEqual(FakeManusHandler.requests[0]["key"], SECRET)

    def test_doctor_blocks_when_key_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_wrapper(["doctor", "--cwd", tmp], env={"HOME": tmp})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 2)
            self.assertIn("manus_api_key_missing", payload["issues"])

    def test_run_submits_private_task_and_redacts_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            prompt = "Review the checkpoint plan in the supplied project context."
            result = run_wrapper([
                "run", "--cwd", tmp, "--base-url", server.url, "--prompt", prompt,
                "--title", "Bounded test", "--profile", "manus-1.6-lite",
            ], env={"MANUS_API_KEY": SECRET})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "submitted")
            self.assertEqual(payload["task"]["task_id"], "task-1")
            self.assertNotIn(prompt, result.stdout)
            create = [item for item in FakeManusHandler.requests if item["path"] == "/v2/task.create"][0]
            self.assertEqual(create["body"]["share_visibility"], "private")
            self.assertEqual(create["body"]["agent_profile"], "manus-1.6-lite")
            self.assertEqual(create["body"]["message"]["content"][0]["text"], prompt)

    def test_run_wait_reads_terminal_messages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            result = run_wrapper([
                "run", "--cwd", tmp, "--base-url", server.url, "--prompt", "Reply briefly",
                "--wait", "--poll-interval", "1", "--wait-timeout", "3",
            ], env={"MANUS_API_KEY": SECRET})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "stopped")
            self.assertEqual(payload["messages"]["messages"][0]["assistant_message"]["content"], "MANUS_READY")
            self.assertNotIn("Reply briefly", result.stdout)

    def test_status_reads_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            result = run_wrapper(["status", "task-1", "--cwd", tmp, "--base-url", server.url], env={"MANUS_API_KEY": SECRET})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "stopped")

    def test_probe_verifies_exact_ready_response(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            result = run_wrapper([
                "probe", "--cwd", tmp, "--base-url", server.url,
                "--poll-interval", "1", "--wait-timeout", "3",
            ], env={"MANUS_API_KEY": SECRET})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["probe"]["ok"])
            self.assertNotIn("Reply exactly MANUS_READY", result.stdout)
            create = [item for item in FakeManusHandler.requests if item["path"] == "/v2/task.create"][0]
            self.assertEqual(create["body"]["agent_profile"], "manus-1.6-lite")
            self.assertTrue(create["body"]["hide_in_task_list"])

    def test_probe_survives_transient_startup_waiting_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            FakeManusHandler.startup_waiting_once = True
            result = run_wrapper([
                "probe", "--cwd", tmp, "--base-url", server.url,
                "--poll-interval", "1", "--wait-timeout", "4",
            ], env={"MANUS_API_KEY": SECRET})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["probe"]["ok"])
            self.assertGreaterEqual(FakeManusHandler.detail_calls, 2)

    def test_run_wait_survives_transient_startup_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            FakeManusHandler.startup_not_found_once = True
            result = run_wrapper([
                "run", "--cwd", tmp, "--base-url", server.url, "--prompt", "Reply briefly",
                "--wait", "--poll-interval", "1", "--wait-timeout", "4",
            ], env={"MANUS_API_KEY": SECRET})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "stopped")
            self.assertGreaterEqual(FakeManusHandler.detail_calls, 2)

    def test_follow_up_sends_message_without_echoing_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            prompt = "Use the revised constraint"
            result = run_wrapper(["follow-up", "task-1", "--cwd", tmp, "--base-url", server.url, "--prompt", prompt], env={"MANUS_API_KEY": SECRET})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "submitted")
            self.assertNotIn(prompt, result.stdout)
            self.assertTrue(Path(payload["artifacts"]["receipt"]).is_file())

    def test_follow_up_wait_requires_a_new_event_and_writes_redacted_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            prompt = "Move to phase two"
            result = run_wrapper([
                "follow-up", "task-1", "--cwd", tmp, "--base-url", server.url,
                "--prompt", prompt, "--wait", "--poll-interval", "1", "--wait-timeout", "3",
                "--run-id", "follow-up-test",
            ], env={"MANUS_API_KEY": SECRET})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            assistant_events = [event for event in payload["messages"]["messages"] if "assistant_message" in event]
            self.assertEqual(assistant_events[-1]["assistant_message"]["content"], "PHASE_TWO_OK")
            receipt = Path(payload["artifacts"]["receipt"]).read_text()
            self.assertNotIn(prompt, receipt)
            self.assertNotIn(SECRET, receipt)

    def test_follow_up_wait_ignores_new_user_and_running_events_until_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            FakeManusHandler.followup_result_delay_once = True
            result = run_wrapper([
                "follow-up", "task-1", "--cwd", tmp, "--base-url", server.url,
                "--prompt", "Move to phase two", "--wait", "--poll-interval", "1", "--wait-timeout", "4",
            ], env={"MANUS_API_KEY": SECRET})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            assistant_events = [event for event in payload["messages"]["messages"] if "assistant_message" in event]
            self.assertEqual(assistant_events[-1]["assistant_message"]["content"], "PHASE_TWO_OK")
            self.assertGreaterEqual(FakeManusHandler.followup_message_calls, 2)

    def test_stop_posts_task_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, FakeServer() as server:
            result = run_wrapper(["stop", "task-1", "--cwd", tmp, "--base-url", server.url], env={"MANUS_API_KEY": SECRET})
            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "stopped")
            self.assertTrue(Path(payload["artifacts"]["receipt"]).is_file())
            stop = [item for item in FakeManusHandler.requests if item["path"] == "/v2/task.stop"][0]
            self.assertEqual(stop["body"], {"task_id": "task-1"})

    def test_dry_run_creates_receipt_without_network_or_raw_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            prompt = "Dry run prompt body"
            result = run_wrapper(["run", "--cwd", tmp, "--prompt", prompt, "--dry-run", "--run-id", "dry-test"], env={"MANUS_API_KEY": SECRET})
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "dry-run")
            receipt = Path(payload["artifacts"]["receipt"]).read_text()
            self.assertNotIn(prompt, receipt)
            self.assertNotIn(SECRET, receipt)

    def test_rejects_broad_cwd(self) -> None:
        result = run_wrapper(["run", "--cwd", str(Path.home()), "--prompt", "Safe prompt", "--dry-run"], env={"MANUS_API_KEY": SECRET})
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertIn("cwd_too_broad", payload["issues"])

    def test_rejects_multiple_prompt_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_wrapper(["run", "--cwd", tmp, "--prompt", "one", "--stdin", "--dry-run"])
        self.assertEqual(result.returncode, 2)
        self.assertIn("Provide exactly one", result.stdout)


if __name__ == "__main__":
    unittest.main()
