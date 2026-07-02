#!/usr/bin/env python3
"""Bootstrap the canonical GWS token bundle from gcloud ADC credentials."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from google_oauth import CANONICAL_TOKEN_PATH, REQUIRED_GWS_SCOPES


DEFAULT_ADC_PATH = Path.home() / ".config/gcloud/application_default_credentials.json"
DEFAULT_TOKEN_URI = "https://oauth2.googleapis.com/token"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Copy gcloud Application Default Credentials into the canonical "
            "GWS token bundle and attach the required Workspace scopes."
        )
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_ADC_PATH,
        help=f"ADC credential source. Default: {DEFAULT_ADC_PATH}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=CANONICAL_TOKEN_PATH,
        help=f"Canonical GWS token bundle destination. Default: {CANONICAL_TOKEN_PATH}",
    )
    parser.add_argument(
        "--scope",
        action="append",
        default=[],
        help=(
            "Scope to attach to the canonical bundle. "
            "When omitted, uses the full hard-cutover scope set."
        ),
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.source.exists():
        raise SystemExit(f"ADC credential file not found: {args.source}")

    payload = json.loads(args.source.read_text())
    required_keys = {"client_id", "client_secret", "refresh_token"}
    missing = sorted(required_keys - set(payload))
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"ADC credential file is missing required key(s): {joined}")

    scopes = args.scope or list(REQUIRED_GWS_SCOPES)
    bundle = {
        "type": payload.get("type", "authorized_user"),
        "client_id": payload["client_id"],
        "client_secret": payload["client_secret"],
        "refresh_token": payload["refresh_token"],
        "token_uri": payload.get("token_uri", DEFAULT_TOKEN_URI),
        "scopes": scopes,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bundle, indent=2) + "\n")
    print(f"Wrote canonical GWS token bundle to {args.output}")


if __name__ == "__main__":
    main()
