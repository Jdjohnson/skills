from __future__ import annotations

import base64
import sys
import unittest
from email import policy
from email.parser import BytesParser
from pathlib import Path
from unittest.mock import MagicMock, call, patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import google_gmail  # noqa: E402


def encoded(value: str) -> str:
    return base64.urlsafe_b64encode(value.encode()).decode().rstrip("=")


class GoogleGmailTests(unittest.TestCase):
    @patch.object(google_gmail, "run_gws_json")
    def test_count_uses_id_only_pagination(self, run_gws: MagicMock) -> None:
        run_gws.side_effect = [
            {
                "threads": [{"id": "thread-1"}, {"id": "thread-2"}],
                "nextPageToken": "page-2",
            },
            {"threads": [{"id": "thread-3"}]},
        ]

        payload = google_gmail.count_threads("in:inbox")

        self.assertEqual(payload["threadCount"], 3)
        self.assertEqual(payload["pagesRead"], 2)
        self.assertTrue(payload["complete"])
        self.assertEqual(run_gws.call_count, 2)
        self.assertEqual(run_gws.call_args_list[0].kwargs["params"]["maxResults"], 500)
        self.assertNotIn("pageToken", run_gws.call_args_list[0].kwargs["params"])
        self.assertEqual(
            run_gws.call_args_list[1].kwargs["params"]["pageToken"], "page-2"
        )

    @patch.object(google_gmail, "run_gws_json")
    def test_search_is_thread_oriented_metadata_only(self, run_gws: MagicMock) -> None:
        run_gws.side_effect = [
            {
                "threads": [{"id": "thread-1"}],
                "resultSizeEstimate": 12,
                "nextPageToken": "next-page",
            },
            {
                "id": "thread-1",
                "historyId": "history-1",
                "snippet": "latest snippet",
                "messages": [
                    {
                        "id": "message-1",
                        "threadId": "thread-1",
                        "internalDate": "100",
                        "labelIds": ["INBOX"],
                        "payload": {
                            "headers": [
                                {"name": "Subject", "value": "Earlier"},
                                {"name": "From", "value": "one@localhost"},
                            ]
                        },
                    },
                    {
                        "id": "message-2",
                        "threadId": "thread-1",
                        "internalDate": "200",
                        "labelIds": ["INBOX", "UNREAD"],
                        "payload": {
                            "headers": [
                                {"name": "Subject", "value": "Latest"},
                                {"name": "From", "value": "two@localhost"},
                                {"name": "Delivered-To", "value": "work@localhost"},
                            ],
                            "body": {"data": encoded("must not be decoded")},
                        },
                    },
                ],
            },
        ]

        payload = google_gmail.search_threads(
            "in:inbox", max_results=25, page_token="current-page"
        )

        self.assertEqual(payload["resultSizeEstimate"], 12)
        self.assertEqual(payload["nextPageToken"], "next-page")
        self.assertEqual(len(payload["threads"]), 1)
        thread = payload["threads"][0]
        self.assertEqual(thread["messageCount"], 2)
        self.assertEqual(thread["labelIds"], ["INBOX", "UNREAD"])
        self.assertEqual(thread["latestMessage"]["subject"], "Latest")
        self.assertNotIn("body_text", thread["latestMessage"])
        self.assertNotIn("body_html", thread["latestMessage"])

        list_call = run_gws.call_args_list[0]
        self.assertEqual(list_call.args[0], ["gmail", "users", "threads", "list"])
        self.assertEqual(list_call.kwargs["params"]["pageToken"], "current-page")
        get_call = run_gws.call_args_list[1]
        self.assertEqual(get_call.args[0], ["gmail", "users", "threads", "get"])
        self.assertEqual(get_call.kwargs["params"]["format"], "metadata")
        self.assertIn(
            "List-Unsubscribe", get_call.kwargs["params"]["metadataHeaders"]
        )

    @patch.object(google_gmail, "run_gws_json")
    def test_archive_targets_threads_by_default(self, run_gws: MagicMock) -> None:
        run_gws.return_value = {
            "id": "thread-1",
            "messages": [
                {"id": "message-1", "labelIds": ["IMPORTANT"]},
                {"id": "message-2", "labelIds": ["UNREAD"]},
            ],
        }

        payload = google_gmail.archive_ids(["thread-1"])

        self.assertEqual(payload["target"], "thread")
        self.assertFalse(payload["archived"][0]["inInbox"])
        run_gws.assert_called_once_with(
            ["gmail", "users", "threads", "modify"],
            required_scopes=[google_gmail.GMAIL_SCOPE],
            params={"userId": "me", "id": "thread-1"},
            json_body={"removeLabelIds": ["INBOX"]},
            retry_transient=True,
        )

    @patch.object(google_gmail, "run_gws_json")
    def test_archive_can_explicitly_target_messages(self, run_gws: MagicMock) -> None:
        run_gws.return_value = {
            "id": "message-1",
            "threadId": "thread-1",
            "labelIds": ["IMPORTANT"],
        }

        payload = google_gmail.archive_ids(["message-1"], target="message")

        self.assertEqual(payload["target"], "message")
        self.assertFalse(payload["archived"][0]["inInbox"])
        self.assertEqual(
            run_gws.call_args,
            call(
                ["gmail", "users", "messages", "modify"],
                required_scopes=[google_gmail.GMAIL_SCOPE],
                params={"userId": "me", "id": "message-1"},
                json_body={"removeLabelIds": ["INBOX"]},
                retry_transient=True,
            ),
        )

    def test_message_body_omits_html_unless_requested(self) -> None:
        message = {
            "id": "message-1",
            "payload": {
                "mimeType": "multipart/alternative",
                "headers": [{"name": "Subject", "value": "Hello"}],
                "parts": [
                    {"mimeType": "text/plain", "body": {"data": encoded("Plain")}},
                    {"mimeType": "text/html", "body": {"data": encoded("<b>HTML</b>")}},
                ],
            },
        }

        plain = google_gmail.summarize_message(message)
        with_html = google_gmail.summarize_message(message, include_html=True)

        self.assertEqual(plain["body_text"], "Plain")
        self.assertNotIn("body_html", plain)
        self.assertEqual(with_html["body_html"], "<b>HTML</b>")

    @patch.object(google_gmail, "print_output")
    @patch.object(google_gmail, "run_gws_json")
    def test_table_output_does_not_repeat_draft_creation(
        self, run_gws: MagicMock, print_output: MagicMock
    ) -> None:
        run_gws.return_value = {"id": "draft-1"}

        with patch.object(
            sys,
            "argv",
            [
                "google_gmail.py",
                "draft",
                "--to",
                "person@localhost",
                "--subject",
                "Hello",
                "--body",
                "Draft body",
                "--format",
                "table",
            ],
        ):
            google_gmail.main()

        self.assertEqual(run_gws.call_count, 1)
        print_output.assert_called_once_with({"id": "draft-1"}, "table")

    @patch.object(google_gmail, "print_output")
    @patch.object(google_gmail, "run_gws_json")
    def test_threaded_draft_sets_gmail_and_rfc_threading_fields(
        self, run_gws: MagicMock, _print_output: MagicMock
    ) -> None:
        run_gws.return_value = {"id": "draft-1"}

        with patch.object(
            sys,
            "argv",
            [
                "google_gmail.py",
                "draft",
                "--to",
                "person@localhost",
                "--subject",
                "Re: Hello",
                "--body",
                "Draft body",
                "--thread-id",
                "thread-1",
                "--in-reply-to",
                "<message-1@localhost>",
                "--references",
                "<message-0@localhost> <message-1@localhost>",
            ],
        ):
            google_gmail.main()

        message_resource = run_gws.call_args.kwargs["json_body"]["message"]
        raw = base64.urlsafe_b64decode(message_resource["raw"])
        parsed = BytesParser(policy=policy.default).parsebytes(raw)
        self.assertEqual(message_resource["threadId"], "thread-1")
        self.assertEqual(parsed["In-Reply-To"], "<message-1@localhost>")
        self.assertEqual(
            parsed["References"],
            "<message-0@localhost> <message-1@localhost>",
        )

    @patch.object(google_gmail, "print_output")
    @patch.object(google_gmail, "run_gws_json")
    def test_draft_read_verifies_draft_without_mutating(
        self, run_gws: MagicMock, print_output: MagicMock
    ) -> None:
        run_gws.return_value = {
            "id": "draft-1",
            "message": {
                "id": "message-1",
                "threadId": "thread-1",
                "labelIds": ["DRAFT"],
                "payload": {
                    "headers": [{"name": "Subject", "value": "Re: Hello"}],
                    "mimeType": "text/plain",
                    "body": {"data": encoded("Draft body")},
                },
            },
        }

        with patch.object(
            sys,
            "argv",
            ["google_gmail.py", "draft-read", "draft-1"],
        ):
            google_gmail.main()

        run_gws.assert_called_once_with(
            ["gmail", "users", "drafts", "get"],
            required_scopes=[google_gmail.GMAIL_SCOPE],
            params={"userId": "me", "id": "draft-1", "format": "full"},
        )
        output = print_output.call_args.args[0]
        self.assertEqual(output["id"], "draft-1")
        self.assertEqual(output["message"]["body_text"], "Draft body")

    @patch.object(google_gmail, "run_gws_json")
    def test_draft_list_fetches_full_message_details(self, run_gws: MagicMock) -> None:
        run_gws.side_effect = [
            {
                "drafts": [{"id": "draft-1", "message": {"id": "message-1"}}],
                "resultSizeEstimate": 1,
                "nextPageToken": "page-2",
            },
            {
                "id": "draft-1",
                "message": {
                    "id": "message-1",
                    "threadId": "thread-1",
                    "labelIds": ["DRAFT"],
                    "payload": {
                        "headers": [{"name": "Subject", "value": "Re: Hello"}],
                        "mimeType": "text/html",
                        "body": {"data": encoded("<p>Draft body</p>")},
                    },
                },
            },
        ]

        payload = google_gmail.list_drafts(
            "subject:Hello",
            max_results=25,
            page_token="current-page",
            include_html=True,
        )

        self.assertEqual(payload["resultSizeEstimate"], 1)
        self.assertEqual(payload["nextPageToken"], "page-2")
        self.assertEqual(payload["drafts"][0]["id"], "draft-1")
        self.assertEqual(payload["drafts"][0]["message"]["body_html"], "<p>Draft body</p>")
        self.assertEqual(
            run_gws.call_args_list[0],
            call(
                ["gmail", "users", "drafts", "list"],
                required_scopes=[google_gmail.GMAIL_SCOPE],
                params={
                    "userId": "me",
                    "maxResults": 25,
                    "q": "subject:Hello",
                    "pageToken": "current-page",
                },
            ),
        )

    @patch.object(google_gmail, "print_output")
    @patch.object(google_gmail, "run_gws_json")
    def test_draft_send_is_single_attempt(
        self, run_gws: MagicMock, print_output: MagicMock
    ) -> None:
        run_gws.return_value = {
            "id": "sent-message-1",
            "threadId": "thread-1",
            "labelIds": ["SENT"],
        }

        with patch.object(sys, "argv", ["google_gmail.py", "draft-send", "draft-1"]):
            google_gmail.main()

        run_gws.assert_called_once_with(
            ["gmail", "users", "drafts", "send"],
            required_scopes=[google_gmail.GMAIL_SCOPE],
            params={"userId": "me"},
            json_body={"id": "draft-1"},
            retry_transient=False,
        )
        self.assertTrue(print_output.call_args.args[0]["sent"])

    @patch.object(google_gmail, "print_output")
    @patch.object(google_gmail, "run_gws_json")
    def test_draft_discard_is_single_attempt(
        self, run_gws: MagicMock, print_output: MagicMock
    ) -> None:
        run_gws.return_value = {}

        with patch.object(
            sys, "argv", ["google_gmail.py", "draft-discard", "draft-1"]
        ):
            google_gmail.main()

        run_gws.assert_called_once_with(
            ["gmail", "users", "drafts", "delete"],
            required_scopes=[google_gmail.GMAIL_SCOPE],
            params={"userId": "me", "id": "draft-1"},
            retry_transient=False,
        )
        print_output.assert_called_once_with(
            {"id": "draft-1", "discarded": True}, "json"
        )


if __name__ == "__main__":
    unittest.main()
