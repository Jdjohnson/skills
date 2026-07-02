#!/usr/bin/env python3
"""Read a Google Sheets range through GWS with safe sheet-name quoting."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
from pathlib import Path
from typing import Any

from google_oauth import run_gws_json


SHEETS_SCOPE = "https://www.googleapis.com/auth/spreadsheets"


def parse_spreadsheet_id(raw_value: str) -> str:
    if "docs.google.com/spreadsheets/d/" in raw_value:
        match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", raw_value)
        if not match:
            raise RuntimeError(f"Could not extract spreadsheet ID from {raw_value}")
        return match.group(1)
    return raw_value


def quote_sheet_name(sheet_name: str) -> str:
    escaped = sheet_name.replace("'", "''")
    return f"'{escaped}'"


def build_a1_notation(sheet_name: str | None, raw_range: str | None, a1: str | None) -> str:
    if a1:
        return a1
    if not sheet_name or not raw_range:
        raise RuntimeError("Provide --a1 or both --sheet and --range.")
    return f"{quote_sheet_name(sheet_name)}!{raw_range}"


def render_text(values: list[list[Any]]) -> str:
    if not values:
        return "(empty range)\n"
    return "\n".join("\t".join(str(cell) for cell in row) for row in values) + "\n"


def render_csv(values: list[list[Any]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    for row in values:
        writer.writerow(row)
    return buffer.getvalue()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read a Google Sheet range with safe A1 quoting through GWS."
    )
    parser.add_argument("spreadsheet", help="Spreadsheet URL or raw spreadsheet ID.")
    parser.add_argument("--sheet", default="", help="Sheet tab name when not using --a1.")
    parser.add_argument("--range", dest="sheet_range", default="", help="Cell range like A1:C10.")
    parser.add_argument("--a1", default="", help="Full A1 notation range.")
    parser.add_argument(
        "--format",
        default="text",
        choices=["text", "csv", "json"],
        help="Output format. Default: text.",
    )
    parser.add_argument(
        "--value-render-option",
        default="FORMATTED_VALUE",
        choices=["FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"],
        help="Google Sheets valueRenderOption. Default: FORMATTED_VALUE.",
    )
    parser.add_argument(
        "--major-dimension",
        default="ROWS",
        choices=["ROWS", "COLUMNS"],
        help="Google Sheets major dimension. Default: ROWS.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional output file path. Prints to stdout when omitted.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    spreadsheet_id = parse_spreadsheet_id(args.spreadsheet)
    a1 = build_a1_notation(args.sheet or None, args.sheet_range or None, args.a1 or None)
    payload = run_gws_json(
        ["sheets", "spreadsheets", "values", "get"],
        required_scopes=[SHEETS_SCOPE],
        params={
            "spreadsheetId": spreadsheet_id,
            "range": a1,
            "valueRenderOption": args.value_render_option,
            "majorDimension": args.major_dimension,
        },
    )
    values = payload.get("values", [])

    if args.format == "json":
        rendered = json.dumps(payload, indent=2) + "\n"
    elif args.format == "csv":
        rendered = render_csv(values)
    else:
        rendered = render_text(values)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered)
        print(f"Wrote {payload.get('range', a1)} to {output_path}")
        return

    print(rendered, end="")


if __name__ == "__main__":
    main()
