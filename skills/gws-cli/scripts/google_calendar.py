#!/usr/bin/env python3
"""Thin calendar wrapper around GWS for list, events, and free/busy."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta

from google_oauth import run_gws, run_gws_json


CALENDAR_SCOPE = "https://www.googleapis.com/auth/calendar"


def rfc3339_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def rfc3339_in_days(days: int) -> str:
    return (datetime.now().astimezone() + timedelta(days=days)).replace(microsecond=0).isoformat()


def add_common_output_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--format",
        default="json",
        choices=["json", "table"],
        help="Output format. Default: json.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Thin calendar wrapper around GWS."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    calendars = subparsers.add_parser("calendars", help="List accessible calendars.")
    calendars.add_argument("--max-results", type=int, default=100, help="Default: 100.")
    calendars.add_argument(
        "--show-hidden",
        action="store_true",
        help="Include hidden calendars in the calendar list response.",
    )
    add_common_output_flag(calendars)

    events = subparsers.add_parser("events", help="List events for a calendar.")
    events.add_argument(
        "--calendar-id",
        default="primary",
        help='Calendar identifier. Default: "primary".',
    )
    events.add_argument("--time-min", default="", help="RFC3339 lower bound.")
    events.add_argument("--time-max", default="", help="RFC3339 upper bound.")
    events.add_argument("--query", default="", help="Free-text event search.")
    events.add_argument("--max-results", type=int, default=25, help="Default: 25.")
    events.add_argument(
        "--single-events",
        action="store_true",
        help="Expand recurring events into single instances.",
    )
    events.add_argument(
        "--order-by",
        default="",
        choices=["", "startTime", "updated"],
        help="Optional event ordering.",
    )
    events.add_argument("--time-zone", default="", help="Optional response timezone.")
    add_common_output_flag(events)

    freebusy = subparsers.add_parser("freebusy", help="Query busy windows for calendars.")
    freebusy.add_argument(
        "calendar_ids",
        nargs="+",
        help='One or more calendar IDs, such as "primary" or an email address.',
    )
    freebusy.add_argument(
        "--time-min",
        default="",
        help="RFC3339 start time. Default: now.",
    )
    freebusy.add_argument(
        "--time-max",
        default="",
        help="RFC3339 end time. Default: now + 7 days.",
    )
    freebusy.add_argument(
        "--time-zone",
        default="",
        help="Optional timezone for the free/busy response.",
    )
    add_common_output_flag(freebusy)

    return parser


def render_output(command: list[str], payload: dict[str, object], output_format: str) -> None:
    if output_format == "table":
        text = run_gws(command, required_scopes=[CALENDAR_SCOPE], output_format="table")
        print(text, end="" if text.endswith("\n") else "\n")
        return
    print(json.dumps(payload, indent=2))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "calendars":
        command = ["calendar", "calendarList", "list"]
        params = {
            "maxResults": args.max_results,
            "showHidden": args.show_hidden,
        }
        payload = run_gws_json(command, required_scopes=[CALENDAR_SCOPE], params=params)
        render_output(command + ["--params", json.dumps(params, separators=(",", ":"))], payload, args.format)
        return

    if args.command == "events":
        command = ["calendar", "events", "list"]
        params: dict[str, object] = {
            "calendarId": args.calendar_id,
            "maxResults": args.max_results,
        }
        if args.time_min:
            params["timeMin"] = args.time_min
        if args.time_max:
            params["timeMax"] = args.time_max
        if args.query:
            params["q"] = args.query
        if args.single_events:
            params["singleEvents"] = True
        if args.order_by:
            params["orderBy"] = args.order_by
        if args.time_zone:
            params["timeZone"] = args.time_zone
        payload = run_gws_json(command, required_scopes=[CALENDAR_SCOPE], params=params)
        render_output(command + ["--params", json.dumps(params, separators=(",", ":"))], payload, args.format)
        return

    command = ["calendar", "freebusy", "query"]
    json_body: dict[str, object] = {
        "timeMin": args.time_min or rfc3339_now(),
        "timeMax": args.time_max or rfc3339_in_days(7),
        "items": [{"id": calendar_id} for calendar_id in args.calendar_ids],
    }
    if args.time_zone:
        json_body["timeZone"] = args.time_zone
    payload = run_gws_json(command, required_scopes=[CALENDAR_SCOPE], json_body=json_body)
    render_output(command + ["--json", json.dumps(json_body, separators=(",", ":"))], payload, args.format)


if __name__ == "__main__":
    main()
