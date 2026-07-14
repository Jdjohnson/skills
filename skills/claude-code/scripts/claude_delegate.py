#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SECRET_ENV_NAMES = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "ANTHROPIC_AWS_API_KEY",
    "ANTHROPIC_AWS_WORKSPACE_ID",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "AZURE_CLIENT_SECRET",
)

CREDENTIAL_ENV_NAMES = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
)

DEFAULT_CLAUDE_CANDIDATES = (
    "~/.local/bin/claude",
    "/opt/homebrew/bin/claude",
    "/usr/local/bin/claude",
)

DEFAULT_CLAUDE_MODEL = "opus"

DEFAULT_MODE_TOOLS = {
    "read": ["Read", "Glob", "Grep"],
    "plan": ["Read", "Glob", "Grep", "Bash"],
    "edit": ["Read", "Glob", "Grep", "Edit", "Write", "Bash"],
}

DEFAULT_ALLOWED_TOOLS = {
    "read": ["Read", "Glob", "Grep"],
    "plan": [
        "Read",
        "Glob",
        "Grep",
        "Bash(pwd)",
        "Bash(ls *)",
        "Bash(rg *)",
        "Bash(git status *)",
        "Bash(git diff *)",
        "Bash(git log *)",
    ],
    "edit": ["Read", "Glob", "Grep", "Edit", "Write"],
}

MODE_PERMISSION = {
    "read": "dontAsk",
    # Claude Code's built-in plan mode may try to persist plan files under
    # ~/.claude/plans. Keep delegated planning inside stdout and the project cwd.
    "plan": "dontAsk",
    "edit": "acceptEdits",
}

DATA_CLASSIFICATIONS = ("public", "internal", "sanitized", "client-private")

PRIVATE_PROMPT_PATTERNS = (
    (r"/projects/[^ \n]+/source-material/", "source_material_path"),
    (r"/Users/[^ \n]+/Downloads/[^ \n]*(usage|export|report)[^ \n]*\.(zip|csv|xlsx?|docx)", "downloaded_source_package"),
    (r"\braw\s+(csv|exports?|source)\b", "raw_export_request"),
    (r"\bsource\s+(csv|exports?)\b", "source_export_request"),
    (r"\b(users?|projects?|gpts?)\s+export\b", "workspace_usage_export"),
    (r"\bChatGPT Enterprise usage\b", "enterprise_usage_data"),
)


@dataclass
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str


def redact(text: str, env: dict[str, str] | None = None) -> str:
    if not text:
        return text

    env = env or os.environ
    redacted = text
    for name in SECRET_ENV_NAMES:
        value = env.get(name)
        if value and len(value) >= 4:
            redacted = redacted.replace(value, f"<redacted:{name}>")

    redacted = re.sub(r"sk-ant-[A-Za-z0-9_-]{8,}", "<redacted:anthropic-key>", redacted)
    redacted = re.sub(
        r"(Bearer\s+)[A-Za-z0-9._~+/=-]{12,}",
        r"\1<redacted:bearer-token>",
        redacted,
        flags=re.IGNORECASE,
    )
    return redacted


def json_print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def find_claude(claude_bin: str | None) -> dict[str, Any]:
    if claude_bin:
        if os.sep in claude_bin:
            candidate = Path(claude_bin).expanduser()
            resolved = str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None
        else:
            resolved = shutil.which(claude_bin)
    else:
        resolved = shutil.which("claude")
        if not resolved:
            for candidate in DEFAULT_CLAUDE_CANDIDATES:
                path = Path(candidate).expanduser()
                if path.is_file() and os.access(path, os.X_OK):
                    resolved = str(path)
                    break

    return {
        "found": bool(resolved),
        "path": str(Path(resolved).expanduser()) if resolved else None,
    }


def run_subprocess(argv: list[str], cwd: Path | None = None, timeout: int = 60) -> CommandResult:
    try:
        completed = subprocess.run(
            argv,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return CommandResult(
            argv=argv,
            returncode=completed.returncode,
            stdout=redact(completed.stdout),
            stderr=redact(completed.stderr),
        )
    except FileNotFoundError as exc:
        return CommandResult(argv=argv, returncode=127, stdout="", stderr=str(exc))
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            argv=argv,
            returncode=124,
            stdout=redact(exc.stdout or ""),
            stderr=redact(exc.stderr or f"Timed out after {timeout} seconds"),
        )


def validate_cwd(raw_cwd: str | None) -> dict[str, Any]:
    cwd = Path(raw_cwd or os.getcwd()).expanduser()
    issues: list[str] = []

    try:
        resolved = cwd.resolve()
    except OSError as exc:
        return {"ok": False, "path": str(cwd), "issues": [f"cwd_resolve_failed:{exc}"]}

    if not resolved.exists():
        issues.append("cwd_missing")
    elif not resolved.is_dir():
        issues.append("cwd_not_directory")

    home = Path.home().resolve()
    root = Path(resolved.anchor).resolve()
    unsafe_paths = {root, home}
    if home.parent != home:
        unsafe_paths.add(home.parent)
    if Path("/Users").exists():
        unsafe_paths.add(Path("/Users").resolve())

    if resolved in unsafe_paths:
        issues.append("cwd_too_broad")

    return {"ok": not issues, "path": str(resolved), "issues": issues}


def present_credentials(env: dict[str, str] | None = None) -> list[str]:
    env = env or os.environ
    present: list[str] = []
    for name in CREDENTIAL_ENV_NAMES:
        value = env.get(name)
        if value:
            present.append(name)
    return present


def collect_preflight(args: argparse.Namespace, require_auth: bool = True) -> dict[str, Any]:
    issues: list[str] = []
    binary = find_claude(getattr(args, "claude_bin", None))
    version: dict[str, Any] = {"ok": False, "text": None}
    auth: dict[str, Any] = {
        "ok": False,
        "method": "missing",
        "env_credentials": present_credentials(),
        "status_text": None,
    }

    if not binary["found"]:
        issues.append("claude_cli_missing")
    else:
        version_result = run_subprocess([binary["path"], "--version"], timeout=15)
        version = {
            "ok": version_result.returncode == 0,
            "text": (version_result.stdout or version_result.stderr).strip() or None,
            "returncode": version_result.returncode,
        }
        if not version["ok"]:
            issues.append("claude_version_failed")

        auth_result = run_subprocess([binary["path"], "auth", "status", "--text"], timeout=20)
        status_text = (auth_result.stdout or auth_result.stderr).strip()
        auth["status_text"] = status_text or None
        if auth_result.returncode == 0:
            auth["ok"] = True
            auth["method"] = "claude-login"
        elif auth["env_credentials"]:
            auth["ok"] = True
            auth["method"] = "environment"
        elif require_auth:
            issues.append("claude_auth_missing")
            auth["codex_escalation_hint"] = (
                "Claude login can be hidden by Codex sandboxing; rerun the same wrapper command "
                "with Codex require_escalated before concluding auth is missing."
            )

    cwd = validate_cwd(getattr(args, "cwd", None))
    if not cwd["ok"]:
        issues.extend(cwd["issues"])

    return {
        "ok": not issues,
        "status": "ready" if not issues else "blocked",
        "issues": issues,
        "claude": binary | {"version": version},
        "auth": auth,
        "cwd": cwd,
    }


def classify_failure(returncode: int, stdout: str, stderr: str) -> str | None:
    if returncode == 0:
        return None

    text = f"{stdout}\n{stderr}".lower()
    if returncode == 127 or "no such file" in text or "command not found" in text:
        return "missing_cli"
    if "not logged in" in text or "please run /login" in text or "could not resolve authentication method" in text:
        return "not_authenticated"
    if "invalid api key" in text or "oauth token" in text or "organization has been disabled" in text:
        return "authentication_error"
    if "unable to connect" in text or "enotfound" in text or "econnreset" in text:
        return "network_or_sandbox"
    if "ssl" in text or "tls" in text or "certificate" in text or "could not resolve host" in text:
        return "network_or_sandbox"
    if "operation not permitted" in text and ("network" in text or "socket" in text):
        return "network_or_sandbox"
    if "permission" in text or "approval" in text or "blocked for safety" in text or "auto mode could not" in text:
        return "permission_or_policy"
    if "session limit" in text or "weekly limit" in text or "rate limit" in text or "429" in text:
        return "rate_limit_or_quota"
    if "overloaded" in text or "529" in text or "temporarily limiting" in text:
        return "rate_limit_or_quota"
    if "credit balance" in text or "usage credits required" in text:
        return "rate_limit_or_quota"
    if "max turns" in text or "maximum turns" in text:
        return "max_turns"
    if "model" in text and ("not available" in text or "unsupported" in text or "retired" in text):
        return "model_issue"
    return "unknown"


def read_prompt(args: argparse.Namespace) -> str:
    sources = [bool(args.prompt), bool(args.prompt_file), bool(args.stdin)]
    if sum(sources) != 1:
        raise ValueError("Provide exactly one of --prompt, --prompt-file, or --stdin.")

    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).expanduser().read_text(encoding="utf-8")
    return sys.stdin.read()


def audit_external_data_safety(prompt: str, args: argparse.Namespace) -> dict[str, Any]:
    classification = getattr(args, "data_classification", "internal")
    findings: list[str] = []

    if classification == "client-private":
        findings.append("declared_client_private")

    for pattern, label in PRIVATE_PROMPT_PATTERNS:
        if re.search(pattern, prompt, flags=re.IGNORECASE):
            findings.append(label)

    findings = list(dict.fromkeys(findings))
    issues = ["external_private_data_not_allowed"] if findings else []
    return {
        "ok": not issues,
        "data_classification": classification,
        "findings": findings,
        "issues": issues,
        "recommendation": (
            "Run private/client data analysis locally in Codex, or create a sanitized aggregate packet "
            "with no raw export paths, client identifiers, user-level rows, or source files before using external agents."
        )
        if issues
        else None,
    }


def merge_csv(values: list[str]) -> str:
    items: list[str] = []
    for value in values:
        for part in value.split(","):
            stripped = part.strip()
            if stripped:
                items.append(stripped)
    return ",".join(dict.fromkeys(items))


def build_claude_run_argv(
    args: argparse.Namespace,
    prompt: str,
    *,
    probe: bool = False,
) -> list[str]:
    mode = "read" if probe else args.mode
    claude = find_claude(args.claude_bin)["path"] or args.claude_bin or "claude"
    argv = [
        claude,
        "-p",
        prompt,
        "--output-format",
        "text" if probe else args.output_format,
        "--permission-mode",
        "dontAsk" if probe else MODE_PERMISSION[mode],
        "--max-turns",
        str(1 if probe else args.max_turns),
    ]

    if probe or args.no_session_persistence:
        argv.append("--no-session-persistence")

    tools: list[str] = [] if probe else list(DEFAULT_MODE_TOOLS[mode])
    if not probe and args.tool:
        tools.extend(args.tool)
    if tools:
        argv.extend(["--tools", merge_csv(tools)])

    if probe or getattr(args, "safe_mode", False):
        argv.append("--safe-mode")

    allowed_tools: list[str] = [] if probe else list(DEFAULT_ALLOWED_TOOLS[mode])
    if args.allowed_tool:
        allowed_tools.extend(args.allowed_tool)
    if allowed_tools:
        argv.extend(["--allowedTools", merge_csv(allowed_tools)])

    if args.model:
        argv.extend(["--model", args.model])
    if args.effort:
        argv.extend(["--effort", args.effort])
    if args.max_budget_usd is not None:
        argv.extend(["--max-budget-usd", str(args.max_budget_usd)])
    if args.resume:
        argv.extend(["--resume", args.resume])
    if args.continue_session:
        argv.append("--continue")
    if args.name:
        argv.extend(["--name", args.name])

    return argv


def command_preview(argv: list[str], prompt: str) -> list[str]:
    preview: list[str] = []
    replaced = False
    for item in argv:
        if not replaced and item == prompt:
            preview.append(f"<prompt:{len(prompt)} chars>")
            replaced = True
        else:
            preview.append(redact(item))
    return preview


def parse_json_output(output: str) -> Any:
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return None


def do_doctor(args: argparse.Namespace) -> int:
    payload = collect_preflight(args, require_auth=not args.no_auth_required)
    json_print(payload)
    return 0 if payload["ok"] else 2


def do_probe(args: argparse.Namespace) -> int:
    payload = collect_preflight(args, require_auth=True)
    if not payload["ok"]:
        payload["probe"] = {"ok": False, "stdout": "", "stderr": "", "returncode": None}
        json_print(payload)
        return 2

    prompt = "Reply exactly READY."
    cwd = Path(payload["cwd"]["path"])
    argv = build_claude_run_argv(args, prompt, probe=True)
    result = run_subprocess(argv, cwd=cwd, timeout=args.timeout)
    ready_text = result.stdout.strip()
    exact_ready = result.returncode == 0 and ready_text.rstrip(".") == "READY"
    payload.update(
        {
            "ok": exact_ready,
            "status": "ready" if exact_ready else "blocked",
            "failure_kind": classify_failure(result.returncode, result.stdout, result.stderr),
            "command": {"argv": command_preview(argv, prompt)},
            "probe": {
                "ok": exact_ready,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            },
        }
    )
    json_print(payload)
    return 0 if exact_ready else 1


def do_audit_prompt(args: argparse.Namespace) -> int:
    try:
        prompt = read_prompt(args)
    except (OSError, ValueError) as exc:
        json_print({"ok": False, "status": "blocked", "issues": [str(exc)]})
        return 2

    safety = audit_external_data_safety(prompt, args)
    json_print(
        {
            "ok": safety["ok"],
            "status": "safe" if safety["ok"] else "blocked",
            "failure_kind": None if safety["ok"] else "external_private_data_not_allowed",
            "issues": safety["issues"],
            "data_safety": safety,
        }
    )
    return 0 if safety["ok"] else 2


def do_run(args: argparse.Namespace) -> int:
    try:
        prompt = read_prompt(args)
    except (OSError, ValueError) as exc:
        json_print({"ok": False, "status": "blocked", "issues": [str(exc)]})
        return 2

    data_safety = audit_external_data_safety(prompt, args)
    if not data_safety["ok"]:
        json_print(
            {
                "ok": False,
                "status": "blocked",
                "failure_kind": "external_private_data_not_allowed",
                "issues": data_safety["issues"],
                "data_safety": data_safety,
                "result": None,
            }
        )
        return 2

    payload = collect_preflight(args, require_auth=True)
    if not payload["ok"]:
        payload["result"] = None
        payload["data_safety"] = data_safety
        json_print(payload)
        return 2

    cwd = Path(payload["cwd"]["path"])
    argv = build_claude_run_argv(args, prompt)
    result = run_subprocess(argv, cwd=cwd, timeout=args.timeout)
    parsed = parse_json_output(result.stdout) if args.output_format == "json" else None
    ok = result.returncode == 0
    payload.update(
        {
            "ok": ok,
            "status": "complete" if ok else "blocked",
            "failure_kind": classify_failure(result.returncode, result.stdout, result.stderr),
            "data_safety": data_safety,
            "command": {"argv": command_preview(argv, prompt)},
            "result": {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "json": parsed,
            },
        }
    )
    json_print(payload)
    return 0 if ok else 1


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--claude-bin", help="Path or command name for Claude Code CLI.")
    parser.add_argument("--cwd", help="Trusted project directory to run Claude Code in.")
    parser.add_argument("--timeout", type=int, default=600, help="Subprocess timeout in seconds.")


def add_prompt_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--data-classification", choices=DATA_CLASSIFICATIONS, default="internal")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe wrapper for Claude Code CLI delegation.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check local Claude Code readiness.")
    add_common(doctor)
    doctor.add_argument("--no-auth-required", action="store_true", help="Do not fail when auth is missing.")
    doctor.set_defaults(func=do_doctor)

    probe = subparsers.add_parser("probe", help="Run a no-tool READY smoke test.")
    add_common(probe)
    probe.add_argument("--allowed-tool", action="append", default=[], help=argparse.SUPPRESS)
    probe.add_argument("--tool", action="append", default=[], help=argparse.SUPPRESS)
    probe.add_argument("--model")
    probe.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"])
    probe.add_argument("--max-budget-usd", type=float)
    probe.add_argument("--resume")
    probe.add_argument("--continue-session", action="store_true")
    probe.add_argument("--name")
    probe.add_argument("--no-session-persistence", action="store_true", default=True)
    probe.set_defaults(func=do_probe)

    audit = subparsers.add_parser("audit-prompt", help="Check whether a prompt is safe for external Claude handoff.")
    add_prompt_args(audit)
    audit.set_defaults(func=do_audit_prompt)

    run = subparsers.add_parser("run", help="Run a bounded Claude Code delegation.")
    add_common(run)
    run.add_argument("--mode", choices=["read", "plan", "edit"], default="plan")
    add_prompt_args(run)
    run.add_argument("--output-format", choices=["text", "json", "stream-json"], default="json")
    run.add_argument("--max-turns", type=int, default=8)
    run.add_argument("--model", default=DEFAULT_CLAUDE_MODEL)
    run.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"])
    run.add_argument("--max-budget-usd", type=float)
    run.add_argument("--resume")
    run.add_argument("--continue-session", action="store_true")
    run.add_argument("--name")
    run.add_argument("--no-session-persistence", action="store_true")
    run.add_argument("--safe-mode", dest="safe_mode", action="store_true", default=True)
    run.add_argument("--no-safe-mode", dest="safe_mode", action="store_false")
    run.add_argument("--allowed-tool", action="append", default=[])
    run.add_argument("--tool", action="append", default=[])
    run.set_defaults(func=do_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
