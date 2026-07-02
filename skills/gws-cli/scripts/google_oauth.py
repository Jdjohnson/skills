#!/usr/bin/env python3
"""Shared GWS token refresh and CLI helpers for local Dot scripts."""

from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


CANONICAL_SOURCE_NAME = "gws-full"
CANONICAL_TOKEN_PATH = Path.home() / ".config/gws/token_full.json"
DEFAULT_TOKEN_VAR = "GOOGLE_WORKSPACE_CLI_TOKEN"
REQUIRED_GWS_SCOPES = (
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.modify",
)


@dataclass(frozen=True)
class TokenSource:
    name: str
    token_path: Path


@dataclass
class TokenBundle:
    source: TokenSource
    refresh_token: str
    client_id: str
    client_secret: str
    token_uri: str
    scopes: set[str]
    access_token: str | None = None
    expiry: str | int | None = None


def reauth_instructions() -> str:
    scopes = ",".join(REQUIRED_GWS_SCOPES)
    return (
        "Re-auth the canonical GWS token bundle with:\n"
        "1. gws auth logout\n"
        f"2. gws auth login --scopes {scopes}\n"
        f"3. Write the authorized-user credentials to {CANONICAL_TOKEN_PATH}\n"
        f"   Preferred: gws auth export --unmasked > {CANONICAL_TOKEN_PATH}\n"
        "   If `gws auth export` fails with `Failed to decrypt credentials`, run:\n"
        f"   gcloud auth application-default login --client-id-file=$HOME/.config/gws/client_secret.json --scopes {scopes}\n"
        "   python3 .dot-skills/gws-cli/scripts/google_token_from_adc.py\n"
        "4. Verify token_full.json contains the full required scope set"
    )


def normalize_scopes(raw_scopes: Any) -> set[str]:
    if raw_scopes is None:
        return set()
    if isinstance(raw_scopes, str):
        return {scope.strip() for scope in raw_scopes.split() if scope.strip()}
    if isinstance(raw_scopes, list):
        return {str(scope).strip() for scope in raw_scopes if str(scope).strip()}
    return set()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_token_bundle() -> TokenBundle:
    source = TokenSource(name=CANONICAL_SOURCE_NAME, token_path=CANONICAL_TOKEN_PATH)
    if not source.token_path.exists():
        raise RuntimeError(
            f"Canonical GWS token store not found at {source.token_path}.\n{reauth_instructions()}"
        )

    payload = _load_json(source.token_path)
    required_keys = {"refresh_token", "client_id", "client_secret"}
    missing = sorted(required_keys - set(payload))
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(
            f"{source.token_path} is missing required key(s): {joined}.\n"
            f"{reauth_instructions()}"
        )

    return TokenBundle(
        source=source,
        refresh_token=payload["refresh_token"],
        client_id=payload["client_id"],
        client_secret=payload["client_secret"],
        token_uri=payload.get("token_uri", "https://oauth2.googleapis.com/token"),
        scopes=normalize_scopes(payload.get("scopes")),
        access_token=payload.get("token"),
        expiry=payload.get("expiry"),
    )


def ensure_scopes(bundle: TokenBundle, required_scopes: Iterable[str] | None = None) -> None:
    required = {scope for scope in (required_scopes or []) if scope}
    if not required:
        return
    missing = sorted(required - bundle.scopes)
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(
            f"{bundle.source.token_path} does not include the required scope(s): {joined}.\n"
            f"{reauth_instructions()}"
        )


def refresh_access_token(bundle: TokenBundle, timeout: int = 20) -> dict[str, Any]:
    form_data = urllib.parse.urlencode(
        {
            "client_id": bundle.client_id,
            "client_secret": bundle.client_secret,
            "refresh_token": bundle.refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        bundle.token_uri,
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Token refresh failed for {bundle.source.name}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Token refresh failed for {bundle.source.name}: {exc.reason}") from exc

    access_token = payload.get("access_token")
    if not access_token:
        raise RuntimeError(
            f"Token refresh for {bundle.source.name} did not return an access token."
        )

    return {
        "source": bundle.source.name,
        "token_path": str(bundle.source.token_path),
        "access_token": access_token,
        "token_type": payload.get("token_type", "Bearer"),
        "expires_in": payload.get("expires_in"),
        "scopes": sorted(bundle.scopes),
    }


def refresh_token_payload(required_scopes: Iterable[str] | None = None) -> dict[str, Any]:
    bundle = load_token_bundle()
    ensure_scopes(bundle, required_scopes)
    return refresh_access_token(bundle)


def build_gws_env(
    required_scopes: Iterable[str] | None = None,
    *,
    var_name: str = DEFAULT_TOKEN_VAR,
) -> tuple[dict[str, str], dict[str, Any]]:
    payload = refresh_token_payload(required_scopes)
    env = os.environ.copy()
    env[var_name] = payload["access_token"]
    return env, payload


def run_gws(
    command: Sequence[str],
    *,
    required_scopes: Iterable[str] | None = None,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    output_format: str = "json",
) -> str:
    env, _ = build_gws_env(required_scopes)
    argv = ["gws", *command, "--format", output_format]
    if params is not None:
        argv.extend(["--params", json.dumps(params, separators=(",", ":"))])
    if json_body is not None:
        argv.extend(["--json", json.dumps(json_body, separators=(",", ":"))])

    completed = subprocess.run(
        argv,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        stdout = completed.stdout.strip()
        detail = stderr or stdout or f"exit code {completed.returncode}"
        raise RuntimeError(f"`{' '.join(argv)}` failed: {detail}")
    return completed.stdout


def run_gws_json(
    command: Sequence[str],
    *,
    required_scopes: Iterable[str] | None = None,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    raw = run_gws(
        command,
        required_scopes=required_scopes,
        params=params,
        json_body=json_body,
        output_format="json",
    )
    return json.loads(raw) if raw.strip() else {}
