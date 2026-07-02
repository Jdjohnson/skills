#!/usr/bin/env python3
"""Thin Gmail wrapper around GWS for Gmail read, draft, label, and archive work."""

from __future__ import annotations

import argparse
import base64
import json
from email.message import EmailMessage
from typing import Any

from google_oauth import run_gws, run_gws_json


GMAIL_SCOPE = "https://www.googleapis.com/auth/gmail.modify"


def add_common_output_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--format",
        default="json",
        choices=["json", "table"],
        help="Output format. Default: json.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Thin Gmail wrapper around GWS.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search Gmail messages.")
    search.add_argument("query", nargs="?", default="", help="Gmail query string.")
    search.add_argument("--max-results", type=int, default=10, help="Default: 10.")
    search.add_argument(
        "--include-spam-trash",
        action="store_true",
        help="Include spam and trash in the search result set.",
    )
    add_common_output_flag(search)

    read_cmd = subparsers.add_parser("read", help="Read a Gmail message.")
    read_cmd.add_argument("message_id", help="Gmail message ID.")
    add_common_output_flag(read_cmd)

    thread = subparsers.add_parser("thread", help="Read a Gmail thread.")
    thread.add_argument("thread_id", help="Gmail thread ID.")
    add_common_output_flag(thread)

    draft = subparsers.add_parser("draft", help="Create a Gmail draft.")
    draft.add_argument("--to", required=True, help="Comma-separated recipients.")
    draft.add_argument("--subject", required=True, help="Draft subject line.")
    draft.add_argument("--body", required=True, help="Plain text draft body.")
    draft.add_argument("--cc", default="", help="Optional CC recipients.")
    draft.add_argument("--bcc", default="", help="Optional BCC recipients.")
    add_common_output_flag(draft)

    archive = subparsers.add_parser("archive", help="Archive one or more Gmail messages.")
    archive.add_argument("message_ids", nargs="+", help="One or more Gmail message IDs.")
    add_common_output_flag(archive)

    labels = subparsers.add_parser("labels", help="List Gmail labels.")
    add_common_output_flag(labels)

    metadata = subparsers.add_parser("metadata", help="Read Gmail message metadata.")
    metadata.add_argument("message_ids", nargs="+", help="One or more Gmail message IDs.")
    metadata.add_argument(
        "--headers",
        default="Subject,From,To,Date,List-ID,List-Unsubscribe,List-Unsubscribe-Post,Precedence,Auto-Submitted,Reply-To,Sender",
        help="Comma-separated metadata headers to fetch.",
    )
    add_common_output_flag(metadata)

    modify = subparsers.add_parser("modify-labels", help="Add/remove labels on a Gmail message.")
    modify.add_argument("message_id", help="Gmail message ID.")
    modify.add_argument("--add", default="", help="Comma-separated label IDs to add.")
    modify.add_argument("--remove", default="", help="Comma-separated label IDs to remove.")
    add_common_output_flag(modify)

    return parser


def header_map(headers: list[dict[str, str]] | None) -> dict[str, str]:
    if not headers:
        return {}
    return {
        item.get("name", "").lower(): item.get("value", "")
        for item in headers
        if item.get("name")
    }


def decode_body_data(data: str) -> str:
    padding = "=" * (-len(data) % 4)
    decoded = base64.urlsafe_b64decode(data + padding)
    return decoded.decode("utf-8", errors="replace")


def collect_message_bodies(part: dict[str, Any] | None) -> dict[str, str]:
    bodies: dict[str, str] = {}
    if not part:
        return bodies

    mime_type = part.get("mimeType", "")
    body = part.get("body", {}) or {}
    data = body.get("data")
    if data and mime_type in {"text/plain", "text/html"}:
        bodies[mime_type] = decode_body_data(data)

    for child in part.get("parts", []) or []:
        bodies.update(collect_message_bodies(child))
    return bodies


def summarize_message(message: dict[str, Any]) -> dict[str, Any]:
    payload = message.get("payload", {}) or {}
    headers = header_map(payload.get("headers"))
    bodies = collect_message_bodies(payload)
    return {
        "id": message.get("id"),
        "threadId": message.get("threadId"),
        "labelIds": message.get("labelIds", []),
        "snippet": message.get("snippet", ""),
        "subject": headers.get("subject", ""),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "date": headers.get("date", ""),
        "headers": headers,
        "body_text": bodies.get("text/plain", ""),
        "body_html": bodies.get("text/html", ""),
    }


def print_output(command: list[str], payload: Any, output_format: str) -> None:
    if output_format == "table":
        text = run_gws(command, required_scopes=[GMAIL_SCOPE], output_format="table")
        print(text, end="" if text.endswith("\n") else "\n")
        return
    print(json.dumps(payload, indent=2))


def build_raw_message(args: argparse.Namespace) -> str:
    message = EmailMessage()
    message["To"] = args.to
    message["Subject"] = args.subject
    if args.cc:
        message["Cc"] = args.cc
    if args.bcc:
        message["Bcc"] = args.bcc
    message.set_content(args.body)
    return base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")


def comma_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "search":
        list_params = {
            "userId": "me",
            "maxResults": args.max_results,
            "includeSpamTrash": args.include_spam_trash,
        }
        if args.query:
            list_params["q"] = args.query
        list_command = [
            "gmail",
            "users",
            "messages",
            "list",
            "--params",
            json.dumps(list_params, separators=(",", ":")),
        ]
        listing = run_gws_json(
            ["gmail", "users", "messages", "list"],
            required_scopes=[GMAIL_SCOPE],
            params=list_params,
        )
        summaries: list[dict[str, Any]] = []
        for message in listing.get("messages", []) or []:
            get_params = {
                "userId": "me",
                "id": message["id"],
                "format": "full",
            }
            full_message = run_gws_json(
                ["gmail", "users", "messages", "get"],
                required_scopes=[GMAIL_SCOPE],
                params=get_params,
            )
            summaries.append(summarize_message(full_message))
        print_output(list_command, {"resultSizeEstimate": listing.get("resultSizeEstimate"), "messages": summaries}, args.format)
        return

    if args.command == "read":
        params = {"userId": "me", "id": args.message_id, "format": "full"}
        command = [
            "gmail",
            "users",
            "messages",
            "get",
            "--params",
            json.dumps(params, separators=(",", ":")),
        ]
        message = run_gws_json(
            ["gmail", "users", "messages", "get"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
        )
        print_output(command, summarize_message(message), args.format)
        return

    if args.command == "thread":
        params = {"userId": "me", "id": args.thread_id, "format": "full"}
        command = [
            "gmail",
            "users",
            "threads",
            "get",
            "--params",
            json.dumps(params, separators=(",", ":")),
        ]
        thread = run_gws_json(
            ["gmail", "users", "threads", "get"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
        )
        payload = {
            "id": thread.get("id"),
            "snippet": thread.get("snippet", ""),
            "messages": [summarize_message(message) for message in thread.get("messages", []) or []],
        }
        print_output(command, payload, args.format)
        return

    if args.command == "draft":
        body = {"message": {"raw": build_raw_message(args)}}
        params = {"userId": "me"}
        command = [
            "gmail",
            "users",
            "drafts",
            "create",
            "--params",
            json.dumps(params, separators=(",", ":")),
            "--json",
            json.dumps(body, separators=(",", ":")),
        ]
        payload = run_gws_json(
            ["gmail", "users", "drafts", "create"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
            json_body=body,
        )
        print_output(command, payload, args.format)
        return

    if args.command == "labels":
        params = {"userId": "me"}
        command = [
            "gmail",
            "users",
            "labels",
            "list",
            "--params",
            json.dumps(params, separators=(",", ":")),
        ]
        payload = run_gws_json(
            ["gmail", "users", "labels", "list"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
        )
        print_output(command, payload, args.format)
        return

    if args.command == "metadata":
        headers = comma_list(args.headers)
        results: list[dict[str, Any]] = []
        for message_id in args.message_ids:
            params = {
                "userId": "me",
                "id": message_id,
                "format": "metadata",
                "metadataHeaders": headers,
            }
            message = run_gws_json(
                ["gmail", "users", "messages", "get"],
                required_scopes=[GMAIL_SCOPE],
                params=params,
            )
            results.append(summarize_message(message))
        print_output(
            ["gmail", "users", "messages", "get"],
            {"messages": results},
            args.format,
        )
        return

    if args.command == "modify-labels":
        body = {
            "addLabelIds": comma_list(args.add),
            "removeLabelIds": comma_list(args.remove),
        }
        params = {"userId": "me", "id": args.message_id}
        payload = run_gws_json(
            ["gmail", "users", "messages", "modify"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
            json_body=body,
        )
        print_output(
            ["gmail", "users", "messages", "modify"],
            {
                "id": payload.get("id", args.message_id),
                "labelIds": payload.get("labelIds", []),
                "threadId": payload.get("threadId"),
            },
            args.format,
        )
        return

    results: list[dict[str, Any]] = []
    for message_id in args.message_ids:
        params = {"userId": "me", "id": message_id}
        body = {"removeLabelIds": ["INBOX"]}
        payload = run_gws_json(
            ["gmail", "users", "messages", "modify"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
            json_body=body,
        )
        results.append(
            {
                "id": payload.get("id", message_id),
                "labelIds": payload.get("labelIds", []),
                "threadId": payload.get("threadId"),
            }
        )
    print_output(
        ["gmail", "users", "messages", "modify"],
        {"archived": results},
        args.format,
    )


if __name__ == "__main__":
    main()
