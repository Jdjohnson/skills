#!/usr/bin/env python3
"""Refresh the canonical GWS OAuth token and print it in a reusable format."""

from __future__ import annotations

import argparse
import json
import shlex

from google_oauth import (
    DEFAULT_TOKEN_VAR,
    REQUIRED_GWS_SCOPES,
    refresh_token_payload,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Refresh the canonical GWS OAuth token and print an access token export."
    )
    parser.add_argument(
        "--require-scope",
        action="append",
        default=[],
        help=(
            "Require a specific scope before exporting the token. "
            "When omitted, validates the full hard-cutover scope set."
        ),
    )
    parser.add_argument(
        "--format",
        default="shell",
        choices=["shell", "json", "token"],
        help="How to print the refreshed access token. Default: shell.",
    )
    parser.add_argument(
        "--var-name",
        default=DEFAULT_TOKEN_VAR,
        help=(
            "Shell variable name used with --format shell. "
            f"Default: {DEFAULT_TOKEN_VAR}."
        ),
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    required_scopes = args.require_scope or list(REQUIRED_GWS_SCOPES)
    payload = refresh_token_payload(required_scopes)

    if args.format == "token":
        print(payload["access_token"])
        return

    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return

    token = shlex.quote(payload["access_token"])
    print(f"export {args.var_name}={token}")


if __name__ == "__main__":
    main()
