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


DEFAULT_CANDIDATES = (
    "~/.local/bin/cursor-agent",
    "/opt/homebrew/bin/cursor-agent",
    "/usr/local/bin/cursor-agent",
)
SECRET_ENV_NAMES = ("CURSOR_API_KEY",)
MODES = ("read", "plan", "edit")
MODE_PREFACE = {
    "read": "Act as a read-only reviewer. Do not edit files or run mutating commands.",
    "plan": "Inspect in read-only plan mode. Return a concise plan, risks, and checks. Do not edit files.",
    "edit": "Edit only inside the trusted workspace. Do not commit, push, publish, install, or make unrelated changes.",
}


def preflight(args: argparse.Namespace, require_auth: bool = True) -> dict[str, Any]:
    cwd = validate_cwd(args.cwd)
    binary = find_binary(args.cursor_bin, "cursor-agent", DEFAULT_CANDIDATES)
    issues = list(cwd["issues"])
    version = {"ok": False, "text": None}
    auth: dict[str, Any] = {"ok": False, "method": "missing", "status_text": None}
    if not binary:
        issues.append("cursor_cli_missing")
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
            issues.append("cursor_version_failed")

        status = run_subprocess(
            [binary, "status"], cwd=Path(cwd["path"]) if cwd["ok"] else None, timeout=30, secret_env_names=SECRET_ENV_NAMES
        )
        status_text = (status.stdout or status.stderr).strip()
        lower = status_text.lower()
        ok = status.returncode == 0 and "not logged in" not in lower
        auth = {
            "ok": ok,
            "method": "cursor-status" if ok else "environment" if os.environ.get("CURSOR_API_KEY") else "missing",
            "status_text": status_text or None,
            "returncode": status.returncode,
        }
        if not ok and os.environ.get("CURSOR_API_KEY"):
            auth["ok"] = True
        if require_auth and not auth["ok"]:
            issues.append("cursor_auth_missing")

    return {
        "ok": not issues,
        "status": "inactive-ready" if not issues else "blocked",
        "active": False,
        "issues": issues,
        "cursor": {"found": bool(binary), "path": binary, "version": version},
        "auth": auth,
        "cwd": cwd,
        "model": args.model,
        "note": "Cursor is inactive and must be selected explicitly.",
    }


def build_argv(args: argparse.Namespace, prompt: str, *, probe: bool = False) -> list[str]:
    binary = find_binary(args.cursor_bin, "cursor-agent", DEFAULT_CANDIDATES) or args.cursor_bin or "cursor-agent"
    mode = "read" if probe else args.mode
    task = "Reply with exactly CURSOR_READY." if probe else f"{MODE_PREFACE[mode]}\n\nUser task:\n{prompt}"
    argv = [
        binary,
        "--print",
        "--output-format",
        "json",
        "--workspace",
        args.cwd,
        "--sandbox",
        "enabled",
    ]
    if mode == "read":
        argv.extend(["--mode", "ask"])
    elif mode == "plan":
        argv.extend(["--mode", "plan"])
    else:
        argv.append("--auto-review")
    if args.model:
        argv.extend(["--model", args.model])
    argv.append(task)
    return argv


def do_doctor(args: argparse.Namespace) -> int:
    payload = preflight(args, require_auth=not args.no_auth_required)
    json_print(payload)
    return 0 if payload["ok"] else 2


def do_probe(args: argparse.Namespace) -> int:
    if not args.allow_inactive:
        json_print({"ok": False, "status": "inactive", "issues": ["cursor_inactive_requires_explicit_opt_in"]})
        return 2
    payload = preflight(args, require_auth=not args.no_auth_required)
    if not payload["ok"]:
        json_print(payload)
        return 2
    argv = build_argv(args, "", probe=True)
    result = run_subprocess(
        argv, cwd=Path(payload["cwd"]["path"]), timeout=args.timeout, secret_env_names=SECRET_ENV_NAMES
    )
    parsed = parse_json(result.stdout)
    response = " ".join(text_values(parsed)).strip() if parsed is not None else result.stdout.strip()
    exact = response in {"CURSOR_READY", "CURSOR_READY."}
    payload.update(
        {
            "ok": result.returncode == 0 and exact,
            "status": "ready" if result.returncode == 0 and exact else "blocked",
            "failure_kind": None if exact else classify_failure(result.returncode, result.stdout, result.stderr) or "unexpected_response",
            "result": {"returncode": result.returncode, "response_text": response},
        }
    )
    json_print(payload)
    return 0 if payload["ok"] else 1


def do_run(args: argparse.Namespace) -> int:
    if not args.allow_inactive:
        json_print({"ok": False, "status": "inactive", "issues": ["cursor_inactive_requires_explicit_opt_in"]})
        return 2
    try:
        prompt = read_prompt(args)
    except (OSError, ValueError) as exc:
        json_print({"ok": False, "status": "blocked", "issues": [str(exc)]})
        return 2

    payload = preflight(args, require_auth=not args.no_auth_required)
    if not payload["ok"]:
        json_print(payload)
        return 2

    cwd = Path(payload["cwd"]["path"])
    delegated_prompt = f"{MODE_PREFACE[args.mode]}\n\nUser task:\n{prompt}"
    artifacts = prepare_artifacts(cwd, "cursor", safe_run_id(args.run_id), delegated_prompt)
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
    parser.add_argument("--cursor-bin")
    parser.add_argument("--cwd", default=os.getcwd())
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--model")
    parser.add_argument("--no-auth-required", action="store_true")


def add_prompt(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--stdin", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guarded wrapper for inactive Cursor CLI delegation.")
    sub = parser.add_subparsers(dest="command", required=True)
    doctor = sub.add_parser("doctor")
    add_common(doctor)
    doctor.set_defaults(func=do_doctor)
    probe = sub.add_parser("probe")
    add_common(probe)
    probe.add_argument("--allow-inactive", action="store_true")
    probe.set_defaults(func=do_probe)
    run = sub.add_parser("run")
    add_common(run)
    add_prompt(run)
    run.add_argument("--mode", choices=MODES, default="plan")
    run.add_argument("--run-id")
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--allow-inactive", action="store_true")
    run.set_defaults(func=do_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
