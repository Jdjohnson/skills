#!/usr/bin/env python3
"""Bootstrap the configured GWS token bundle from gcloud ADC credentials."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from google_oauth import CANONICAL_TOKEN_PATH, REQUIRED_GWS_SCOPES


DEFAULT_ADC_PATH = Path.home() / ".config/gcloud/application_default_credentials.json"
DEFAULT_TOKEN_URI = "https://oauth2.googleapis.com/token"


def write_private_json(path: Path, payload: dict[str, object]) -> None:
    path = path.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError(f"Refusing symlinked credential destination: {path}")

    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_path, 0o600)
        os.replace(temp_path, path)
        os.chmod(path, 0o600)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Copy gcloud Application Default Credentials into the configured "
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
            "When omitted, uses the required Workspace scope set."
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

    write_private_json(args.output, bundle)
    print(f"Wrote GWS token bundle to {args.output}")


if __name__ == "__main__":
    main()
