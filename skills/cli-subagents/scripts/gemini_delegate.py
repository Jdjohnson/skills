#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from _delegate_common import (
    classify_failure,
    find_binary,
    json_print,
    parse_json,
    prepare_artifacts,
    read_prompt,
    run_subprocess,
    safe_run_id,
    text_values,
    validate_cwd,
    write_artifacts,
)


DEFAULT_MODEL = "gemini-3.6-flash"
DEFAULT_CANDIDATES = (
    "/opt/homebrew/bin/gemini",
    "/usr/local/bin/gemini",
    "~/.local/bin/gemini",
)
SECRET_ENV_NAMES = ("GEMINI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS")
MODES = ("read", "plan", "edit")
MODE_PREFACE = {
    "read": "Act as a read-only reviewer. Do not edit files or run mutating commands.",
    "plan": "Inspect in read-only plan mode. Return a concise plan, risks, and checks. Do not edit files.",
    "edit": "Edit only inside the trusted workspace. Do not commit, push, publish, install, or make unrelated changes.",
}


def auth_state() -> dict[str, Any]:
    env_names = [name for name in SECRET_ENV_NAMES if os.environ.get(name)]
    selected_type: str | None = None
    settings_path = Path.home() / ".gemini" / "settings.json"
    if settings_path.is_file():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
            selected = settings.get("security", {}).get("auth", {}).get("selectedType")
            if isinstance(selected, str):
                selected_type = selected
        except (OSError, json.JSONDecodeError):
            pass

    oauth_paths = (
        Path.home() / ".gemini" / "oauth_creds.json",
        Path.home() / ".gemini" / "google_accounts.json",
    )
    cached = [str(path) for path in oauth_paths if path.is_file()]
    if selected_type == "gemini-api-key":
        ok = bool(env_names)
        method = "environment" if env_names else "api-key-selected-but-missing"
    elif selected_type == "oauth-personal":
        ok = False
        method = "cached-login-unverified" if cached else "oauth-selected-but-missing"
    else:
        ok = bool(env_names)
        method = "environment" if env_names else "cached-login-unverified" if cached else "runtime-check-required"
    return {
        "ok": ok,
        "method": method,
        "selected_type": selected_type,
        "env_credentials": env_names,
        "cached_login_detected": bool(cached),
        "runtime_attempt_allowed": bool(env_names or cached),
    }


def preflight(
    args: argparse.Namespace,
    require_auth: bool = True,
    allow_cached_attempt: bool = False,
) -> dict[str, Any]:
    cwd = validate_cwd(args.cwd)
    binary = find_binary(args.gemini_bin, "gemini", DEFAULT_CANDIDATES)
    issues = list(cwd["issues"])
    version = {"ok": False, "text": None}
    if not binary:
        issues.append("gemini_cli_missing")
    else:
        result = run_subprocess(
            [binary, "--version"], cwd=None, timeout=15, secret_env_names=SECRET_ENV_NAMES
        )
        version = {
            "ok": result.returncode == 0,
            "text": (result.stdout or result.stderr).strip() or None,
            "returncode": result.returncode,
        }
        if not version["ok"]:
            issues.append("gemini_version_failed")

    auth = auth_state()
    usable_auth = auth["ok"] or (
        allow_cached_attempt and auth["cached_login_detected"]
    )
    if require_auth and not usable_auth:
        issues.append("gemini_auth_unverified")
    return {
        "ok": not issues,
        "status": "ready" if not issues else "blocked",
        "issues": issues,
        "gemini": {"found": bool(binary), "path": binary, "version": version},
        "auth": auth,
        "cwd": cwd,
        "model": args.model or DEFAULT_MODEL,
    }


def build_argv(args: argparse.Namespace, prompt: str, *, probe: bool = False) -> list[str]:
    binary = find_binary(args.gemini_bin, "gemini", DEFAULT_CANDIDATES) or args.gemini_bin or "gemini"
    mode = "read" if probe else args.mode
    task = "Reply with exactly GEMINI_READY." if probe else f"{MODE_PREFACE[mode]}\n\nUser task:\n{prompt}"
    argv = [
        binary,
        "--model",
        args.model or DEFAULT_MODEL,
        "--skip-trust",
        "--approval-mode",
        "plan" if mode in {"read", "plan"} else "auto_edit",
        "--prompt",
        task,
        "--output-format",
        "json",
    ]
    return argv


def do_doctor(args: argparse.Namespace) -> int:
    payload = preflight(args, require_auth=not args.no_auth_required)
    json_print(payload)
    return 0 if payload["ok"] else 2


def do_probe(args: argparse.Namespace) -> int:
    payload = preflight(
        args,
        require_auth=not args.no_auth_required,
        allow_cached_attempt=True,
    )
    if not payload["ok"]:
        json_print(payload)
        return 2
    argv = build_argv(args, "", probe=True)
    result = run_subprocess(
        argv, cwd=Path(payload["cwd"]["path"]), timeout=args.timeout, secret_env_names=SECRET_ENV_NAMES
    )
    parsed = parse_json(result.stdout)
    response = " ".join(text_values(parsed)).strip() if parsed is not None else result.stdout.strip()
    exact = response in {"GEMINI_READY", "GEMINI_READY."}
    payload.update(
        {
            "ok": result.returncode == 0 and exact,
            "status": "ready" if result.returncode == 0 and exact else "blocked",
            "failure_kind": None if exact else classify_failure(result.returncode, result.stdout, result.stderr) or "unexpected_response",
            "result": {
                "returncode": result.returncode,
                "response_text": response,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "json": parsed,
            },
        }
    )
    json_print(payload)
    return 0 if payload["ok"] else 1


def do_run(args: argparse.Namespace) -> int:
    try:
        prompt = read_prompt(args)
    except (OSError, ValueError) as exc:
        json_print({"ok": False, "status": "blocked", "issues": [str(exc)]})
        return 2

    payload = preflight(
        args,
        require_auth=not args.no_auth_required,
        allow_cached_attempt=True,
    )
    if not payload["ok"]:
        json_print(payload)
        return 2

    cwd = Path(payload["cwd"]["path"])
    delegated_prompt = f"{MODE_PREFACE[args.mode]}\n\nUser task:\n{prompt}"
    artifacts = prepare_artifacts(cwd, "gemini", safe_run_id(args.run_id), delegated_prompt)
    argv = build_argv(args, prompt)
    payload.update(
        {
            "mode": args.mode,
            "command": {"argv": [f"<prompt:{len(prompt)} chars>" if item == delegated_prompt else item for item in argv]},
            "artifacts": artifacts,
        }
    )
    if args.dry_run:
        payload.update({"ok": True, "status": "dry-run", "result": None})
        Path(artifacts["meta"]).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        json_print(payload)
        return 0

    result = run_subprocess(argv, cwd=cwd, timeout=args.timeout, secret_env_names=SECRET_ENV_NAMES)
    parsed = parse_json(result.stdout)
    response = " ".join(text_values(parsed)).strip() if parsed is not None else result.stdout.strip()
    ok = result.returncode == 0 and bool(response)
    payload.update(
        {
            "ok": ok,
            "status": "complete" if ok else "blocked",
            "failure_kind": None if ok else classify_failure(result.returncode, result.stdout, result.stderr),
            "result": {
                "returncode": result.returncode,
                "response_text": response,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "json": parsed,
            },
        }
    )
    write_artifacts(artifacts, result, payload)
    json_print(payload)
    return 0 if ok else 1


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--gemini-bin")
    parser.add_argument("--cwd", default=os.getcwd())
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--no-auth-required", action="store_true")


def add_prompt(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--stdin", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guarded wrapper for Gemini CLI delegation.")
    sub = parser.add_subparsers(dest="command", required=True)
    doctor = sub.add_parser("doctor")
    add_common(doctor)
    doctor.set_defaults(func=do_doctor)
    probe = sub.add_parser("probe")
    add_common(probe)
    probe.set_defaults(func=do_probe)
    run = sub.add_parser("run")
    add_common(run)
    add_prompt(run)
    run.add_argument("--mode", choices=MODES, default="plan")
    run.add_argument("--run-id")
    run.add_argument("--dry-run", action="store_true")
    run.set_defaults(func=do_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
