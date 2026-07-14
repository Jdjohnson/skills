#!/usr/bin/env python3
"""Thin Gmail wrapper around GWS for read, draft, label, and archive work."""

from __future__ import annotations

import argparse
import base64
import json
from email.message import EmailMessage
from typing import Any

from google_oauth import run_gws_json


GMAIL_SCOPE = "https://www.googleapis.com/auth/gmail.modify"
SEARCH_METADATA_HEADERS = (
    "Subject",
    "From",
    "To",
    "Cc",
    "Date",
    "Message-ID",
    "List-ID",
    "List-Unsubscribe",
    "List-Unsubscribe-Post",
    "Precedence",
    "Auto-Submitted",
    "Reply-To",
    "Sender",
    "Delivered-To",
    "X-Forwarded-To",
    "X-Forwarded-For",
    "References",
    "In-Reply-To",
)


def bounded_max_results(value: str) -> int:
    result = int(value)
    if not 1 <= result <= 100:
        raise argparse.ArgumentTypeError("max results must be between 1 and 100")
    return result


def add_common_output_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--format",
        default="json",
        choices=["json", "table"],
        help="Output format. Default: json.",
    )


def add_message_body_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--include-html",
        action="store_true",
        help="Include decoded HTML bodies in addition to plain text.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Thin Gmail wrapper around GWS.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    profile = subparsers.add_parser(
        "profile", help="Verify the authenticated Gmail account and API access."
    )
    add_common_output_flag(profile)

    count = subparsers.add_parser(
        "count", help="Count matching Gmail threads without fetching message metadata."
    )
    count.add_argument("query", nargs="?", default="", help="Gmail query string.")
    count.add_argument(
        "--page-limit",
        type=bounded_max_results,
        default=20,
        help="Maximum 500-thread pages to inspect. Default: 20; max: 100.",
    )
    count.add_argument(
        "--include-spam-trash",
        action="store_true",
        help="Include spam and trash in the count.",
    )
    add_common_output_flag(count)

    search = subparsers.add_parser(
        "search", help="Search Gmail threads and return lightweight metadata."
    )
    search.add_argument("query", nargs="?", default="", help="Gmail query string.")
    search.add_argument(
        "--max-results", type=bounded_max_results, default=10, help="Default: 10; max: 100."
    )
    search.add_argument("--page-token", help="Optional Gmail pagination token.")
    search.add_argument(
        "--include-spam-trash",
        action="store_true",
        help="Include spam and trash in the search result set.",
    )
    add_common_output_flag(search)

    read_cmd = subparsers.add_parser("read", help="Read a Gmail message.")
    read_cmd.add_argument("message_id", help="Gmail message ID.")
    add_message_body_flags(read_cmd)
    add_common_output_flag(read_cmd)

    thread = subparsers.add_parser("thread", help="Read a Gmail thread.")
    thread.add_argument("thread_id", help="Gmail thread ID.")
    add_message_body_flags(thread)
    add_common_output_flag(thread)

    draft = subparsers.add_parser("draft", help="Create a Gmail draft.")
    draft.add_argument("--to", required=True, help="Comma-separated recipients.")
    draft.add_argument("--subject", required=True, help="Draft subject line.")
    draft.add_argument("--body", required=True, help="Plain text draft body.")
    draft.add_argument("--cc", default="", help="Optional CC recipients.")
    draft.add_argument("--bcc", default="", help="Optional BCC recipients.")
    draft.add_argument("--thread-id", help="Gmail thread ID for a reply draft.")
    draft.add_argument(
        "--in-reply-to", help="RFC Message-ID of the message being replied to."
    )
    draft.add_argument(
        "--references", help="RFC References header for a threaded reply draft."
    )
    add_common_output_flag(draft)

    draft_read = subparsers.add_parser(
        "draft-read", help="Read a Gmail draft by draft ID for verification."
    )
    draft_read.add_argument("draft_id", help="Gmail draft ID.")
    add_message_body_flags(draft_read)
    add_common_output_flag(draft_read)

    draft_list = subparsers.add_parser(
        "draft-list", help="List existing Gmail drafts with message details."
    )
    draft_list.add_argument("query", nargs="?", default="", help="Gmail query string.")
    draft_list.add_argument(
        "--max-results", type=bounded_max_results, default=100, help="Default: 100; max: 100."
    )
    draft_list.add_argument("--page-token", help="Optional Gmail pagination token.")
    add_message_body_flags(draft_list)
    add_common_output_flag(draft_list)

    draft_send = subparsers.add_parser(
        "draft-send", help="Send one existing Gmail draft without retrying."
    )
    draft_send.add_argument("draft_id", help="Gmail draft ID.")
    add_common_output_flag(draft_send)

    draft_discard = subparsers.add_parser(
        "draft-discard", help="Permanently discard one existing Gmail draft without retrying."
    )
    draft_discard.add_argument("draft_id", help="Gmail draft ID.")
    add_common_output_flag(draft_discard)

    archive = subparsers.add_parser(
        "archive", help="Archive one or more Gmail threads (default) or messages."
    )
    archive.add_argument("ids", nargs="+", help="One or more Gmail thread/message IDs.")
    archive.add_argument(
        "--target",
        choices=["thread", "message"],
        default="thread",
        help="ID type to archive. Default: thread.",
    )
    add_common_output_flag(archive)

    labels = subparsers.add_parser("labels", help="List Gmail labels.")
    add_common_output_flag(labels)

    metadata = subparsers.add_parser("metadata", help="Read Gmail message metadata.")
    metadata.add_argument("message_ids", nargs="+", help="One or more Gmail message IDs.")
    metadata.add_argument(
        "--headers",
        default=",".join(SEARCH_METADATA_HEADERS),
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


def collect_message_bodies(
    part: dict[str, Any] | None, *, include_html: bool = False
) -> dict[str, str]:
    bodies: dict[str, str] = {}
    if not part:
        return bodies

    mime_type = part.get("mimeType", "")
    body = part.get("body", {}) or {}
    data = body.get("data")
    accepted_types = {"text/plain"}
    if include_html:
        accepted_types.add("text/html")
    if data and mime_type in accepted_types:
        bodies[mime_type] = decode_body_data(data)

    for child in part.get("parts", []) or []:
        for child_type, child_body in collect_message_bodies(
            child, include_html=include_html
        ).items():
            existing = bodies.get(child_type, "")
            bodies[child_type] = f"{existing}\n{child_body}".strip() if existing else child_body
    return bodies


def summarize_message(
    message: dict[str, Any],
    *,
    include_body: bool = True,
    include_html: bool = False,
) -> dict[str, Any]:
    payload = message.get("payload", {}) or {}
    headers = header_map(payload.get("headers"))
    summary: dict[str, Any] = {
        "id": message.get("id"),
        "threadId": message.get("threadId"),
        "labelIds": message.get("labelIds", []),
        "snippet": message.get("snippet", ""),
        "internalDate": message.get("internalDate"),
        "sizeEstimate": message.get("sizeEstimate"),
        "subject": headers.get("subject", ""),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "date": headers.get("date", ""),
        "headers": headers,
    }
    if include_body:
        bodies = collect_message_bodies(payload, include_html=include_html)
        summary["body_text"] = bodies.get("text/plain", "")
        if include_html:
            summary["body_html"] = bodies.get("text/html", "")
    return summary


def latest_message(messages: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not messages:
        return None

    def timestamp(message: dict[str, Any]) -> int:
        try:
            return int(message.get("internalDate") or 0)
        except (TypeError, ValueError):
            return 0

    return max(
        enumerate(messages),
        key=lambda item: (timestamp(item[1]), item[0]),
    )[1]


def summarize_thread(thread: dict[str, Any]) -> dict[str, Any]:
    messages = thread.get("messages", []) or []
    labels = sorted(
        {
            label
            for message in messages
            for label in (message.get("labelIds", []) or [])
        }
    )
    latest = latest_message(messages)
    return {
        "id": thread.get("id"),
        "historyId": thread.get("historyId"),
        "snippet": thread.get("snippet", ""),
        "messageCount": len(messages),
        "messageIds": [message.get("id") for message in messages if message.get("id")],
        "labelIds": labels,
        "latestMessage": (
            summarize_message(latest, include_body=False) if latest is not None else None
        ),
    }


def search_threads(
    query: str,
    *,
    max_results: int,
    include_spam_trash: bool = False,
    page_token: str | None = None,
) -> dict[str, Any]:
    list_params: dict[str, Any] = {
        "userId": "me",
        "maxResults": max_results,
        "includeSpamTrash": include_spam_trash,
    }
    if query:
        list_params["q"] = query
    if page_token:
        list_params["pageToken"] = page_token

    listing = run_gws_json(
        ["gmail", "users", "threads", "list"],
        required_scopes=[GMAIL_SCOPE],
        params=list_params,
    )
    summaries: list[dict[str, Any]] = []
    for listed_thread in listing.get("threads", []) or []:
        get_params = {
            "userId": "me",
            "id": listed_thread["id"],
            "format": "metadata",
            "metadataHeaders": list(SEARCH_METADATA_HEADERS),
        }
        thread = run_gws_json(
            ["gmail", "users", "threads", "get"],
            required_scopes=[GMAIL_SCOPE],
            params=get_params,
        )
        summaries.append(summarize_thread(thread))

    return {
        "resultSizeEstimate": listing.get("resultSizeEstimate", 0),
        "nextPageToken": listing.get("nextPageToken"),
        "threads": summaries,
    }


def count_threads(
    query: str,
    *,
    include_spam_trash: bool = False,
    page_limit: int = 20,
) -> dict[str, Any]:
    thread_count = 0
    page_count = 0
    page_token: str | None = None

    while page_count < page_limit:
        params: dict[str, Any] = {
            "userId": "me",
            "maxResults": 500,
            "includeSpamTrash": include_spam_trash,
        }
        if query:
            params["q"] = query
        if page_token:
            params["pageToken"] = page_token

        listing = run_gws_json(
            ["gmail", "users", "threads", "list"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
        )
        thread_count += len(listing.get("threads", []) or [])
        page_count += 1
        page_token = listing.get("nextPageToken")
        if not page_token:
            break

    return {
        "query": query,
        "threadCount": thread_count,
        "pagesRead": page_count,
        "complete": not bool(page_token),
        "nextPageToken": page_token,
    }


def list_drafts(
    query: str,
    *,
    max_results: int = 100,
    page_token: str | None = None,
    include_html: bool = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {"userId": "me", "maxResults": max_results}
    if query:
        params["q"] = query
    if page_token:
        params["pageToken"] = page_token

    listing = run_gws_json(
        ["gmail", "users", "drafts", "list"],
        required_scopes=[GMAIL_SCOPE],
        params=params,
    )
    drafts: list[dict[str, Any]] = []
    for listed_draft in listing.get("drafts", []) or []:
        draft_id = listed_draft.get("id")
        if not draft_id:
            continue
        draft = run_gws_json(
            ["gmail", "users", "drafts", "get"],
            required_scopes=[GMAIL_SCOPE],
            params={"userId": "me", "id": draft_id, "format": "full"},
        )
        drafts.append(
            {
                "id": draft.get("id", draft_id),
                "message": summarize_message(
                    draft.get("message", {}) or {}, include_html=include_html
                ),
            }
        )

    return {
        "resultSizeEstimate": listing.get("resultSizeEstimate", 0),
        "nextPageToken": listing.get("nextPageToken"),
        "drafts": drafts,
    }


def table_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        value = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return str(value).replace("\t", " ").replace("\r", " ").replace("\n", " ")


def render_table(payload: Any) -> str:
    if isinstance(payload, dict):
        list_item = next(
            (
                (key, value)
                for key, value in payload.items()
                if isinstance(value, list) and all(isinstance(row, dict) for row in value)
            ),
            None,
        )
        if list_item is not None:
            list_key, rows = list_item
            lines = [
                f"{key}\t{table_cell(value)}"
                for key, value in payload.items()
                if key != list_key
            ]
            if rows:
                columns = list(dict.fromkeys(key for row in rows for key in row))
                lines.append("\t".join(columns))
                lines.extend(
                    "\t".join(table_cell(row.get(column)) for column in columns)
                    for row in rows
                )
            return "\n".join(lines)
        return "\n".join(f"{key}\t{table_cell(value)}" for key, value in payload.items())
    if isinstance(payload, list):
        return "\n".join(table_cell(value) for value in payload)
    return table_cell(payload)


def print_output(payload: Any, output_format: str) -> None:
    if output_format == "table":
        print(render_table(payload))
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
    if args.in_reply_to:
        message["In-Reply-To"] = args.in_reply_to
    if args.references:
        message["References"] = args.references
    message.set_content(args.body)
    return base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")


def comma_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def archive_ids(ids: list[str], *, target: str = "thread") -> dict[str, Any]:
    resource = "threads" if target == "thread" else "messages"
    results: list[dict[str, Any]] = []
    for item_id in ids:
        params = {"userId": "me", "id": item_id}
        body = {"removeLabelIds": ["INBOX"]}
        payload = run_gws_json(
            ["gmail", "users", resource, "modify"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
            json_body=body,
            retry_transient=True,
        )
        if target == "thread":
            messages = payload.get("messages", []) or []
            labels = sorted(
                {
                    label
                    for message in messages
                    for label in (message.get("labelIds", []) or [])
                }
            )
            results.append(
                {
                    "id": payload.get("id", item_id),
                    "messageIds": [
                        message.get("id") for message in messages if message.get("id")
                    ],
                    "labelIds": labels,
                    "inInbox": "INBOX" in labels,
                }
            )
        else:
            labels = payload.get("labelIds", []) or []
            results.append(
                {
                    "id": payload.get("id", item_id),
                    "threadId": payload.get("threadId"),
                    "labelIds": labels,
                    "inInbox": "INBOX" in labels,
                }
            )
    return {"target": target, "archived": results}


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "profile":
        params = {"userId": "me"}
        payload = run_gws_json(
            ["gmail", "users", "getProfile"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
        )
        print_output(
            {
                "emailAddress": payload.get("emailAddress"),
                "messagesTotal": payload.get("messagesTotal"),
                "threadsTotal": payload.get("threadsTotal"),
                "historyId": payload.get("historyId"),
            },
            args.format,
        )
        return

    if args.command == "count":
        print_output(
            count_threads(
                args.query,
                include_spam_trash=args.include_spam_trash,
                page_limit=args.page_limit,
            ),
            args.format,
        )
        return

    if args.command == "search":
        payload = search_threads(
            args.query,
            max_results=args.max_results,
            include_spam_trash=args.include_spam_trash,
            page_token=args.page_token,
        )
        print_output(payload, args.format)
        return

    if args.command == "read":
        params = {"userId": "me", "id": args.message_id, "format": "full"}
        message = run_gws_json(
            ["gmail", "users", "messages", "get"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
        )
        print_output(
            summarize_message(message, include_html=args.include_html), args.format
        )
        return

    if args.command == "thread":
        params = {"userId": "me", "id": args.thread_id, "format": "full"}
        thread = run_gws_json(
            ["gmail", "users", "threads", "get"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
        )
        payload = {
            "id": thread.get("id"),
            "historyId": thread.get("historyId"),
            "snippet": thread.get("snippet", ""),
            "messages": [
                summarize_message(message, include_html=args.include_html)
                for message in thread.get("messages", []) or []
            ],
        }
        print_output(payload, args.format)
        return

    if args.command == "draft":
        threading_values = (args.thread_id, args.in_reply_to, args.references)
        if any(threading_values) and not all(threading_values):
            parser.error(
                "threaded drafts require --thread-id, --in-reply-to, and --references"
            )
        message_resource = {"raw": build_raw_message(args)}
        if args.thread_id:
            message_resource["threadId"] = args.thread_id
        body = {"message": message_resource}
        params = {"userId": "me"}
        payload = run_gws_json(
            ["gmail", "users", "drafts", "create"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
            json_body=body,
        )
        print_output(payload, args.format)
        return

    if args.command == "draft-read":
        params = {"userId": "me", "id": args.draft_id, "format": "full"}
        draft = run_gws_json(
            ["gmail", "users", "drafts", "get"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
        )
        print_output(
            {
                "id": draft.get("id", args.draft_id),
                "message": summarize_message(
                    draft.get("message", {}) or {}, include_html=args.include_html
                ),
            },
            args.format,
        )
        return

    if args.command == "draft-list":
        print_output(
            list_drafts(
                args.query,
                max_results=args.max_results,
                page_token=args.page_token,
                include_html=args.include_html,
            ),
            args.format,
        )
        return

    if args.command == "draft-send":
        payload = run_gws_json(
            ["gmail", "users", "drafts", "send"],
            required_scopes=[GMAIL_SCOPE],
            params={"userId": "me"},
            json_body={"id": args.draft_id},
            retry_transient=False,
        )
        print_output(
            {
                "draftId": args.draft_id,
                "id": payload.get("id"),
                "threadId": payload.get("threadId"),
                "labelIds": payload.get("labelIds", []),
                "sent": bool(payload.get("id")),
            },
            args.format,
        )
        return

    if args.command == "draft-discard":
        run_gws_json(
            ["gmail", "users", "drafts", "delete"],
            required_scopes=[GMAIL_SCOPE],
            params={"userId": "me", "id": args.draft_id},
            retry_transient=False,
        )
        print_output({"id": args.draft_id, "discarded": True}, args.format)
        return

    if args.command == "labels":
        params = {"userId": "me"}
        payload = run_gws_json(
            ["gmail", "users", "labels", "list"],
            required_scopes=[GMAIL_SCOPE],
            params=params,
        )
        print_output(payload, args.format)
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
            results.append(summarize_message(message, include_body=False))
        print_output({"messages": results}, args.format)
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
            retry_transient=True,
        )
        print_output(
            {
                "id": payload.get("id", args.message_id),
                "labelIds": payload.get("labelIds", []),
                "threadId": payload.get("threadId"),
            },
            args.format,
        )
        return

    print_output(archive_ids(args.ids, target=args.target), args.format)


if __name__ == "__main__":
    main()
