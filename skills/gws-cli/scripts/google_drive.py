#!/usr/bin/env python3
"""Thin Drive wrapper around GWS for search, get, and native file creation."""

from __future__ import annotations

import argparse
import json
import re

from google_oauth import run_gws, run_gws_json


DRIVE_SCOPE = "https://www.googleapis.com/auth/drive"
NATIVE_MIME_TYPES = {
    "doc": "application/vnd.google-apps.document",
    "sheet": "application/vnd.google-apps.spreadsheet",
    "slide": "application/vnd.google-apps.presentation",
    "folder": "application/vnd.google-apps.folder",
}


def parse_drive_file_id(raw_value: str) -> str:
    patterns = (
        r"/document/d/([a-zA-Z0-9-_]+)",
        r"/spreadsheets/d/([a-zA-Z0-9-_]+)",
        r"/presentation/d/([a-zA-Z0-9-_]+)",
        r"/file/d/([a-zA-Z0-9-_]+)",
        r"/drive/folders/([a-zA-Z0-9-_]+)",
        r"[?&]id=([a-zA-Z0-9-_]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, raw_value)
        if match:
            return match.group(1)
    return raw_value


def escape_drive_query(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def add_common_output_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--format",
        default="json",
        choices=["json", "table"],
        help="Output format. Default: json.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Thin Drive wrapper around GWS."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search Drive files and folders.")
    search.add_argument(
        "query",
        nargs="?",
        default="",
        help="Optional Drive search term. Uses name/fullText matching when provided.",
    )
    search.add_argument("--parent", default="", help="Optional parent folder ID or URL.")
    search.add_argument("--mime-type", default="", help="Optional MIME type filter.")
    search.add_argument("--page-size", type=int, default=10, help="Default: 10.")
    search.add_argument(
        "--include-trashed",
        action="store_true",
        help="Include trashed items in results.",
    )
    add_common_output_flag(search)

    get_cmd = subparsers.add_parser("get", help="Get a file or folder by ID or URL.")
    get_cmd.add_argument("file", help="Drive/Docs/Sheets/Slides URL or raw file ID.")
    add_common_output_flag(get_cmd)

    create = subparsers.add_parser("create-native", help="Create a native Google file or folder.")
    create.add_argument(
        "type",
        choices=sorted(NATIVE_MIME_TYPES),
        help="Native Google item type to create.",
    )
    create.add_argument("name", help="Title for the new item.")
    create.add_argument("--parent", default="", help="Optional parent folder ID or URL.")
    add_common_output_flag(create)

    return parser


def print_output(command: list[str], payload: dict[str, object], output_format: str) -> None:
    if output_format == "table":
        text = run_gws(command, required_scopes=[DRIVE_SCOPE], output_format="table")
        print(text, end="" if text.endswith("\n") else "\n")
        return
    print(json.dumps(payload, indent=2))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "search":
        clauses: list[str] = []
        if args.query:
            escaped = escape_drive_query(args.query)
            clauses.append(f"(name contains '{escaped}' or fullText contains '{escaped}')")
        if args.parent:
            parent_id = parse_drive_file_id(args.parent)
            clauses.append(f"'{escape_drive_query(parent_id)}' in parents")
        if args.mime_type:
            clauses.append(f"mimeType = '{escape_drive_query(args.mime_type)}'")
        if not args.include_trashed:
            clauses.append("trashed = false")

        params = {
            "pageSize": args.page_size,
            "q": " and ".join(clauses) if clauses else "trashed = false",
            "fields": "files(id,name,mimeType,parents,webViewLink,modifiedTime),nextPageToken",
            "supportsAllDrives": True,
            "includeItemsFromAllDrives": True,
        }
        command = ["drive", "files", "list", "--params", json.dumps(params, separators=(",", ":"))]
        payload = run_gws_json(["drive", "files", "list"], required_scopes=[DRIVE_SCOPE], params=params)
        print_output(command, payload, args.format)
        return

    if args.command == "get":
        file_id = parse_drive_file_id(args.file)
        params = {
            "fileId": file_id,
            "fields": (
                "id,name,mimeType,parents,webViewLink,modifiedTime,createdTime,"
                "owners(displayName,emailAddress),size,driveId,shared,trashed"
            ),
            "supportsAllDrives": True,
        }
        command = ["drive", "files", "get", "--params", json.dumps(params, separators=(",", ":"))]
        payload = run_gws_json(["drive", "files", "get"], required_scopes=[DRIVE_SCOPE], params=params)
        print_output(command, payload, args.format)
        return

    metadata: dict[str, object] = {
        "name": args.name,
        "mimeType": NATIVE_MIME_TYPES[args.type],
    }
    if args.parent:
        metadata["parents"] = [parse_drive_file_id(args.parent)]
    params = {
        "fields": "id,name,mimeType,parents,webViewLink",
        "supportsAllDrives": True,
    }
    command = [
        "drive",
        "files",
        "create",
        "--params",
        json.dumps(params, separators=(",", ":")),
        "--json",
        json.dumps(metadata, separators=(",", ":")),
    ]
    payload = run_gws_json(
        ["drive", "files", "create"],
        required_scopes=[DRIVE_SCOPE],
        params=params,
        json_body=metadata,
    )
    print_output(command, payload, args.format)


if __name__ == "__main__":
    main()
