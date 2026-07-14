#!/usr/bin/env python3
"""Shared Google Workspace token refresh and CLI helpers."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

import fcntl


CANONICAL_SOURCE_NAME = "gws-full"
CANONICAL_TOKEN_PATH = Path.home() / ".config/gws/token_full.json"
DEFAULT_TOKEN_VAR = "GOOGLE_WORKSPACE_CLI_TOKEN"
DEFAULT_COMMAND_TIMEOUT_SECONDS = 30
TOKEN_REFRESH_SKEW_SECONDS = 60
TOKEN_REFRESH_ATTEMPTS = 4
TOKEN_REFRESH_RETRY_DELAY_SECONDS = 0.5
GWS_READ_ATTEMPTS = 4
GWS_RETRY_DELAY_SECONDS = 0.5
REQUIRED_GWS_SCOPES = (
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.modify",
)


_cached_token_payload: dict[str, Any] | None = None
_cached_token_expires_at = 0.0


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
        "   python3 <skill-root>/scripts/google_token_from_adc.py\n"
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

    token_stat = source.token_path.stat()
    mode = stat.S_IMODE(token_stat.st_mode)
    if hasattr(os, "getuid") and token_stat.st_uid != os.getuid():
        raise RuntimeError(
            f"Canonical GWS token store {source.token_path} is not owned by the current user."
        )
    if mode & 0o077:
        raise RuntimeError(
            f"Canonical GWS token store {source.token_path} has insecure permissions "
            f"{mode:04o}; run `chmod 600 {source.token_path}`."
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
    payload: dict[str, Any] | None = None
    for attempt in range(TOKEN_REFRESH_ATTEMPTS):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code not in {429, 500, 502, 503, 504} or attempt + 1 >= TOKEN_REFRESH_ATTEMPTS:
                raise RuntimeError(
                    f"Token refresh failed for {bundle.source.name}: {body}"
                ) from exc
            time.sleep(TOKEN_REFRESH_RETRY_DELAY_SECONDS * (2**attempt))
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt + 1 >= TOKEN_REFRESH_ATTEMPTS:
                reason = getattr(exc, "reason", exc)
                raise RuntimeError(
                    f"Token refresh failed for {bundle.source.name} after "
                    f"{TOKEN_REFRESH_ATTEMPTS} attempts: {reason}"
                ) from exc
            time.sleep(TOKEN_REFRESH_RETRY_DELAY_SECONDS * (2**attempt))

    access_token = (payload or {}).get("access_token")
    if not access_token:
        raise RuntimeError(
            f"Token refresh for {bundle.source.name} did not return an access token."
        )

    return {
        "source": bundle.source.name,
        "token_path": str(bundle.source.token_path),
        "access_token": access_token,
        "token_type": (payload or {}).get("token_type", "Bearer"),
        "expires_in": (payload or {}).get("expires_in"),
        "scopes": sorted(bundle.scopes),
    }


def _expiry_epoch(expiry: str | int | float | None) -> float | None:
    if expiry is None:
        return None
    if isinstance(expiry, (int, float)):
        return float(expiry)
    raw = str(expiry).strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        pass
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def _stored_access_token_payload(bundle: TokenBundle) -> dict[str, Any] | None:
    expires_at = _expiry_epoch(bundle.expiry)
    if (
        not bundle.access_token
        or expires_at is None
        or time.time() + TOKEN_REFRESH_SKEW_SECONDS >= expires_at
    ):
        return None
    return {
        "source": bundle.source.name,
        "token_path": str(bundle.source.token_path),
        "access_token": bundle.access_token,
        "token_type": "Bearer",
        "expires_in": max(0, int(expires_at - time.time())),
        "scopes": sorted(bundle.scopes),
    }


def _persist_access_token(bundle: TokenBundle, payload: dict[str, Any]) -> None:
    expires_in = max(0, int(payload.get("expires_in") or 0))
    expires_at = datetime.fromtimestamp(
        time.time() + expires_in, tz=timezone.utc
    ).isoformat().replace("+00:00", "Z")
    stored = _load_json(bundle.source.token_path)
    stored["token"] = payload["access_token"]
    stored["expiry"] = expires_at

    temp_path = bundle.source.token_path.with_name(
        f".{bundle.source.token_path.name}.{os.getpid()}.tmp"
    )
    descriptor = os.open(temp_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(stored, handle, indent=2)
            handle.write("\n")
        os.chmod(temp_path, 0o600)
        os.replace(temp_path, bundle.source.token_path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


@contextmanager
def _token_refresh_lock(token_path: Path):
    lock_path = token_path.with_name(f".{token_path.name}.lock")
    descriptor = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        os.chmod(lock_path, 0o600)
        with os.fdopen(descriptor, "r+") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            yield
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    finally:
        pass


def refresh_token_payload(required_scopes: Iterable[str] | None = None) -> dict[str, Any]:
    bundle = load_token_bundle()
    ensure_scopes(bundle, required_scopes)
    stored = _stored_access_token_payload(bundle)
    if stored is not None:
        return stored

    with _token_refresh_lock(bundle.source.token_path):
        # Another wrapper process may have refreshed while this one waited.
        bundle = load_token_bundle()
        ensure_scopes(bundle, required_scopes)
        stored = _stored_access_token_payload(bundle)
        if stored is not None:
            return stored
        payload = refresh_access_token(bundle)
        _persist_access_token(bundle, payload)
        return payload


def clear_access_token_cache() -> None:
    """Clear the process-local token cache, primarily for tests and recovery."""
    global _cached_token_payload, _cached_token_expires_at
    _cached_token_payload = None
    _cached_token_expires_at = 0.0


def access_token_payload(required_scopes: Iterable[str] | None = None) -> dict[str, Any]:
    """Return one reusable access token for the lifetime of this process."""
    global _cached_token_payload, _cached_token_expires_at

    required = {scope for scope in (required_scopes or []) if scope}
    now = time.monotonic()
    cached_scopes = set((_cached_token_payload or {}).get("scopes", []))
    if (
        _cached_token_payload is not None
        and required.issubset(cached_scopes)
        and now + TOKEN_REFRESH_SKEW_SECONDS < _cached_token_expires_at
    ):
        return _cached_token_payload

    payload = refresh_token_payload(required)
    try:
        expires_in = max(0, int(payload.get("expires_in") or 0))
    except (TypeError, ValueError):
        expires_in = 0

    _cached_token_payload = payload
    _cached_token_expires_at = now + expires_in
    return payload


def build_gws_env(
    required_scopes: Iterable[str] | None = None,
    *,
    var_name: str = DEFAULT_TOKEN_VAR,
) -> tuple[dict[str, str], dict[str, Any]]:
    payload = access_token_payload(required_scopes)
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
    timeout_seconds: int = DEFAULT_COMMAND_TIMEOUT_SECONDS,
    retry_transient: bool | None = None,
) -> str:
    env, _ = build_gws_env(required_scopes)
    argv = ["gws", *command, "--format", output_format]
    if params is not None:
        argv.extend(["--params", json.dumps(params, separators=(",", ":"))])
    if json_body is not None:
        argv.extend(["--json", json.dumps(json_body, separators=(",", ":"))])

    read_only_actions = {
        "get",
        "getProfile",
        "list",
        "search",
        "batchGet",
        "valuesGet",
    }
    is_read_only = bool(command and command[-1] in read_only_actions)
    should_retry = is_read_only if retry_transient is None else retry_transient
    attempts = GWS_READ_ATTEMPTS if should_retry else 1
    retry_markers = (
        "http request failed",
        "timed out",
        "timeout",
        "connection reset",
        "connection refused",
        "temporarily unavailable",
        "service unavailable",
        "too many requests",
        "rate limit",
        "internal server error",
        "transport error",
        " 429",
        " 502",
        " 503",
        " 504",
    )

    for attempt in range(attempts):
        try:
            completed = subprocess.run(
                argv,
                env=env,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            if attempt + 1 >= attempts:
                raise RuntimeError(
                    f"`{' '.join(argv)}` timed out after {attempts} attempts."
                ) from exc
            time.sleep(GWS_RETRY_DELAY_SECONDS * (2**attempt))
            continue

        if completed.returncode == 0:
            return completed.stdout

        stderr = completed.stderr.strip()
        stdout = completed.stdout.strip()
        detail = stderr or stdout or f"exit code {completed.returncode}"
        retryable = any(marker in detail.lower() for marker in retry_markers)
        if not retryable or attempt + 1 >= attempts:
            suffix = f" after {attempts} attempts" if retryable and attempts > 1 else ""
            raise RuntimeError(f"`{' '.join(argv)}` failed{suffix}: {detail}")
        time.sleep(GWS_RETRY_DELAY_SECONDS * (2**attempt))

    raise RuntimeError(f"`{' '.join(argv)}` failed without a result.")


def run_gws_json(
    command: Sequence[str],
    *,
    required_scopes: Iterable[str] | None = None,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    retry_transient: bool | None = None,
) -> dict[str, Any]:
    raw = run_gws(
        command,
        required_scopes=required_scopes,
        params=params,
        json_body=json_body,
        output_format="json",
        retry_transient=retry_transient,
    )
    return json.loads(raw) if raw.strip() else {}
