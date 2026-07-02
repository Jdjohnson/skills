#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SECRET_ENV_NAMES = (
    "XAI_API_KEY",
    "GROK_API_KEY",
    "GROK_OAUTH_TOKEN",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
)

CREDENTIAL_ENV_NAMES = (
    "XAI_API_KEY",
    "GROK_API_KEY",
    "GROK_OAUTH_TOKEN",
)

DEFAULT_GROK_CANDIDATES = (
    "/Users/jaradjohnson/.grok/bin/grok",
    "~/.grok/bin/grok",
    "~/.local/bin/grok",
    "/opt/homebrew/bin/grok",
    "/usr/local/bin/grok",
)

DEFAULT_GROK_MODEL = "grok-composer-2.5-fast"

COMPAT_ENV_NAMES = (
    "GROK_CLAUDE_SKILLS_ENABLED",
    "GROK_CLAUDE_RULES_ENABLED",
    "GROK_CLAUDE_AGENTS_ENABLED",
    "GROK_CLAUDE_MCPS_ENABLED",
    "GROK_CLAUDE_HOOKS_ENABLED",
    "GROK_CURSOR_SKILLS_ENABLED",
    "GROK_CURSOR_RULES_ENABLED",
    "GROK_CURSOR_AGENTS_ENABLED",
    "GROK_CURSOR_MCPS_ENABLED",
    "GROK_CURSOR_HOOKS_ENABLED",
)

MODE_PERMISSION = {
    "read": "dontAsk",
    # Grok's built-in plan permission mode can return an internal cancelled
    # state without user-facing text. Delegated planning should stay in stdout.
    "plan": "dontAsk",
    "edit": "bypassPermissions",
    "trusted": "bypassPermissions",
    "mcp": "plan",
}

DATA_CLASSIFICATIONS = ("public", "internal", "sanitized", "client-private")

PRIVATE_PROMPT_PATTERNS = (
    (r"/projects/[^ \n]+/source-material/", "source_material_path"),
    (r"/Users/[^ \n]+/Downloads/[^ \n]*(usage|export|report)[^ \n]*\.(zip|csv|xlsx?|docx)", "downloaded_source_package"),
    (r"\braw\s+(csv|exports?|source)\b", "raw_export_request"),
    (r"\bsource\s+(csv|exports?)\b", "source_export_request"),
    (r"\b(users?|projects?|gpts?)\s+export\b", "workspace_usage_export"),
    (r"\bChatGPT Enterprise usage\b", "enterprise_usage_data"),
    (r"\bPSB Bank\b", "client_identifier_psb_bank"),
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

    redacted = re.sub(r"xai-[A-Za-z0-9_-]{8,}", "<redacted:xai-key>", redacted)
    redacted = re.sub(r"sk-[A-Za-z0-9_-]{12,}", "<redacted:api-key>", redacted)
    redacted = re.sub(
        r"(Bearer\s+)[A-Za-z0-9._~+/=-]{12,}",
        r"\1<redacted:bearer-token>",
        redacted,
        flags=re.IGNORECASE,
    )
    return redacted


def json_print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def default_candidates() -> tuple[str, ...]:
    override = os.environ.get("GROK_BUILD_TEST_CANDIDATES")
    if override:
        return tuple(item for item in override.split(os.pathsep) if item)
    return DEFAULT_GROK_CANDIDATES


def find_grok(grok_bin: str | None) -> dict[str, Any]:
    if grok_bin:
        if os.sep in grok_bin:
            candidate = Path(grok_bin).expanduser()
            resolved = str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None
        else:
            resolved = shutil.which(grok_bin)
    else:
        resolved = shutil.which("grok")
        if not resolved:
            for candidate in default_candidates():
                path = Path(candidate).expanduser()
                if path.is_file() and os.access(path, os.X_OK):
                    resolved = str(path)
                    break

    return {
        "found": bool(resolved),
        "path": str(Path(resolved).expanduser()) if resolved else None,
    }


def run_subprocess(
    argv: list[str],
    cwd: Path | None = None,
    timeout: int = 60,
    env: dict[str, str] | None = None,
) -> CommandResult:
    try:
        completed = subprocess.run(
            argv,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=env,
        )
        return CommandResult(
            argv=argv,
            returncode=completed.returncode,
            stdout=redact(completed.stdout, env),
            stderr=redact(completed.stderr, env),
        )
    except FileNotFoundError as exc:
        return CommandResult(argv=argv, returncode=127, stdout="", stderr=str(exc))
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            argv=argv,
            returncode=124,
            stdout=redact(exc.stdout or "", env),
            stderr=redact(exc.stderr or f"Timed out after {timeout} seconds", env),
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
    return [name for name in CREDENTIAL_ENV_NAMES if env.get(name)]


def grok_env(args: argparse.Namespace) -> tuple[dict[str, str], dict[str, str]]:
    env = os.environ.copy()
    policy: dict[str, str] = {}
    compat = getattr(args, "compat", "dot-only")
    if compat in {"dot-only", "none"}:
        for name in COMPAT_ENV_NAMES:
            env[name] = "false"
            policy[name] = "false"
    return env, policy


def collect_preflight(args: argparse.Namespace, require_auth: bool = True) -> dict[str, Any]:
    issues: list[str] = []
    env, env_policy = grok_env(args)
    binary = find_grok(getattr(args, "grok_bin", None))
    version: dict[str, Any] = {"ok": False, "text": None}
    inspect: dict[str, Any] = {"ok": False, "summary": None, "stderr": None}
    auth: dict[str, Any] = {
        "ok": False,
        "method": "missing",
        "env_credentials": present_credentials(env),
    }

    cwd = validate_cwd(getattr(args, "cwd", None))
    if not cwd["ok"]:
        issues.extend(cwd["issues"])

    if not binary["found"]:
        issues.append("grok_cli_missing")
    else:
        version_result = run_subprocess([binary["path"], "--version"], timeout=15, env=env)
        version = {
            "ok": version_result.returncode == 0,
            "text": (version_result.stdout or version_result.stderr).strip() or None,
            "returncode": version_result.returncode,
        }
        if not version["ok"]:
            issues.append("grok_version_failed")

        if cwd["ok"]:
            inspect_result = run_subprocess(
                [binary["path"], "inspect", "--json"],
                cwd=Path(cwd["path"]),
                timeout=30,
                env=env,
            )
            parsed = parse_json_output(inspect_result.stdout)
            inspect = {
                "ok": inspect_result.returncode == 0,
                "summary": summarize_inspect(parsed),
                "stderr": inspect_result.stderr or None,
                "returncode": inspect_result.returncode,
            }
            if inspect["ok"]:
                auth["ok"] = True
                auth["method"] = "grok-inspect"
            elif auth["env_credentials"]:
                auth["ok"] = True
                auth["method"] = "environment"
            elif require_auth:
                issues.append("grok_auth_missing")
        elif auth["env_credentials"]:
            auth["ok"] = True
            auth["method"] = "environment"

    return {
        "ok": not issues,
        "status": "ready" if not issues else "blocked",
        "issues": issues,
        "grok": binary | {"version": version, "inspect": inspect},
        "auth": auth,
        "cwd": cwd,
        "env_policy": env_policy,
    }


def classify_failure(returncode: int, stdout: str, stderr: str) -> str | None:
    text = f"{stdout}\n{stderr}".lower()
    if returncode == 0:
        if "bundle too large" in text or "bundle_create_failed" in text:
            return "bundle_too_large_warning"
        return None

    if returncode == 127 or "no such file" in text or "command not found" in text:
        return "missing_cli"
    if "not logged in" in text or "sign in" in text or "grok login" in text or "authentication required" in text:
        return "not_authenticated"
    if "invalid api key" in text or "unauthorized" in text or "oauth" in text:
        return "authentication_error"
    if "sandbox initialization failed" in text or ("operation not permitted" in text and "sandbox" in text):
        return "nested_sandbox_unsupported"
    if "unable to connect" in text or "enotfound" in text or "econnreset" in text:
        return "network_or_sandbox"
    if "ssl" in text or "tls" in text or "certificate" in text or "could not resolve host" in text:
        return "network_or_sandbox"
    if "operation not permitted" in text and ("network" in text or "socket" in text):
        return "network_or_sandbox"
    if "mcp" in text and ("failed" in text or "unauthorized" in text or "initialization" in text):
        return "mcp_initialization"
    if "permission" in text or "approval" in text or "blocked for safety" in text:
        return "permission_or_policy"
    if "rate limit" in text or "429" in text or "quota" in text or "credit" in text:
        return "rate_limit_or_quota"
    if "max turns" in text or "maximum turns" in text:
        return "max_turns"
    if "model" in text and ("not available" in text or "unsupported" in text or "retired" in text):
        return "model_issue"
    if "bundle too large" in text or "bundle_create_failed" in text:
        return "bundle_too_large_warning"
    if "unexpected argument" in text or "unknown option" in text:
        return "unsupported_flag"
    return "unknown"


def parse_json_output(output: str) -> Any:
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return None


def semantic_json_failure(parsed: Any) -> str | None:
    if not isinstance(parsed, dict):
        return None

    stop_reason = str(parsed.get("stopReason") or parsed.get("stop_reason") or "").lower()
    if stop_reason == "cancelled":
        return "cancelled"

    text = parsed.get("text")
    if isinstance(text, str) and not text.strip():
        return "empty_result"

    return None


def summarize_inspect(parsed: Any) -> dict[str, Any] | None:
    if not isinstance(parsed, dict):
        return None

    compat_cells: list[dict[str, Any]] = []
    external_compat = parsed.get("externalCompat")
    if isinstance(external_compat, dict):
        for cell in external_compat.get("cells", []):
            if isinstance(cell, dict):
                compat_cells.append(
                    {
                        "vendor": cell.get("vendor"),
                        "surface": cell.get("surface"),
                        "enabled": cell.get("enabled"),
                        "source": cell.get("source"),
                    }
                )

    def count(name: str) -> int | None:
        value = parsed.get(name)
        return len(value) if isinstance(value, list) else None

    return {
        "grokVersion": parsed.get("grokVersion"),
        "agents": count("agents"),
        "skills": count("skills"),
        "mcpServers": count("mcpServers"),
        "plugins": count("plugins"),
        "externalCompat": compat_cells,
    }


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
            "Run private/client data analysis locally in the orchestrating agent, or create a sanitized aggregate packet "
            "with no raw export paths, client identifiers, user-level rows, or source files before using external agents."
        )
        if issues
        else None,
    }


def safe_run_id(raw_run_id: str | None) -> str:
    if raw_run_id:
        cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", raw_run_id).strip(".-")
        if cleaned:
            return cleaned[:80]
    return time.strftime("%Y%m%dT%H%M%S")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def git_status(cwd: Path) -> str:
    result = run_subprocess(["git", "-C", str(cwd), "status", "--short"], timeout=20)
    if result.returncode != 0:
        return result.stderr or result.stdout
    return result.stdout


def prepare_artifacts(cwd: Path, run_id: str, prompt: str) -> dict[str, str]:
    run_dir = cwd / ".tmp" / "grok-build" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    prompt_file = run_dir / "prompt.md"
    write_text(prompt_file, prompt)
    write_text(run_dir / "git-status-before.txt", git_status(cwd))
    return {
        "run_dir": str(run_dir),
        "prompt_file": str(prompt_file),
        "stdout": str(run_dir / "stdout.log"),
        "stderr": str(run_dir / "stderr.log"),
        "meta": str(run_dir / "meta.json"),
        "git_status_before": str(run_dir / "git-status-before.txt"),
        "git_status_after": str(run_dir / "git-status-after.txt"),
    }


def command_preview(argv: list[str], env: dict[str, str] | None = None) -> list[str]:
    return [redact(item, env) for item in argv]


def build_grok_argv(
    args: argparse.Namespace,
    prompt_file: str,
    *,
    probe: bool = False,
) -> list[str]:
    grok = find_grok(args.grok_bin)["path"] or args.grok_bin or "grok"
    mode = "read" if probe else args.mode
    argv = [
        grok,
        "--no-auto-update",
        "--cwd",
        args.cwd,
        "--prompt-file",
        prompt_file,
        "--output-format",
        "plain" if probe else args.output_format,
        "--permission-mode",
        "dontAsk" if probe else MODE_PERMISSION[mode],
        "--max-turns",
        str(1 if probe else args.max_turns),
    ]

    if not probe and args.model:
        argv.extend(["--model", args.model])
    if not probe and args.effort:
        argv.extend(["--effort", args.effort])

    if probe or not getattr(args, "allow_web", False):
        argv.append("--disable-web-search")
    if probe or not getattr(args, "allow_subagents", False):
        argv.append("--no-subagents")
    if probe or not getattr(args, "allow_mcp", False):
        argv.extend(["--deny", "MCPTool(*)"])

    if not probe and args.rule:
        for rule in args.rule:
            argv.extend(["--rules", rule])
    if not probe and args.allow:
        for rule in args.allow:
            argv.extend(["--allow", rule])
    if not probe and args.deny:
        for rule in args.deny:
            argv.extend(["--deny", rule])
    if not probe and mode in {"edit", "trusted"}:
        argv.append("--always-approve")

    return argv


def write_result_artifacts(artifacts: dict[str, str], result: CommandResult, payload: dict[str, Any]) -> None:
    write_text(Path(artifacts["stdout"]), result.stdout)
    write_text(Path(artifacts["stderr"]), result.stderr)
    cwd = Path(payload["cwd"]["path"])
    write_text(Path(artifacts["git_status_after"]), git_status(cwd))
    write_text(Path(artifacts["meta"]), json.dumps(payload, indent=2, sort_keys=True))


def do_doctor(args: argparse.Namespace) -> int:
    payload = collect_preflight(args, require_auth=not args.no_auth_required)
    json_print(payload)
    return 0 if payload["ok"] else 2


def do_probe(args: argparse.Namespace) -> int:
    args.compat = getattr(args, "compat", "dot-only")
    args.allow_mcp = False
    args.allow_subagents = False
    args.allow_web = False
    args.mode = "read"
    args.output_format = "plain"
    args.max_turns = 1
    args.model = getattr(args, "model", None)
    args.effort = getattr(args, "effort", None)
    args.rule = []
    args.allow = []
    args.deny = []

    payload = collect_preflight(args, require_auth=True)
    if not payload["ok"]:
        payload["probe"] = {"ok": False, "stdout": "", "stderr": "", "returncode": None}
        json_print(payload)
        return 2

    prompt = "Reply exactly GROK_READY."
    cwd = Path(payload["cwd"]["path"])
    run_id = safe_run_id(args.run_id or "probe")
    artifacts = prepare_artifacts(cwd, run_id, prompt)
    env, env_policy = grok_env(args)
    argv = build_grok_argv(args, artifacts["prompt_file"], probe=True)

    if args.dry_run:
        payload.update(
            {
                "ok": True,
                "status": "dry-run",
                "command": {"argv": command_preview(argv, env)},
                "artifacts": artifacts,
                "env_policy": env_policy,
            }
        )
        write_text(Path(artifacts["meta"]), json.dumps(payload, indent=2, sort_keys=True))
        json_print(payload)
        return 0

    result = run_subprocess(argv, cwd=cwd, timeout=args.timeout, env=env)
    exact_ready = result.returncode == 0 and result.stdout.strip() == "GROK_READY"
    payload.update(
        {
            "ok": exact_ready,
            "status": "ready" if exact_ready else "blocked",
            "failure_kind": classify_failure(result.returncode, result.stdout, result.stderr),
            "command": {"argv": command_preview(argv, env)},
            "artifacts": artifacts,
            "probe": {
                "ok": exact_ready,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            },
        }
    )
    write_result_artifacts(artifacts, result, payload)
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
    run_id = safe_run_id(args.run_id)
    artifacts = prepare_artifacts(cwd, run_id, prompt)
    env, env_policy = grok_env(args)
    argv = build_grok_argv(args, artifacts["prompt_file"])
    payload.update(
        {
            "command": {"argv": command_preview(argv, env)},
            "artifacts": artifacts,
            "env_policy": env_policy,
        }
    )

    if args.dry_run:
        payload.update({"ok": True, "status": "dry-run", "result": None})
        write_text(Path(artifacts["meta"]), json.dumps(payload, indent=2, sort_keys=True))
        json_print(payload)
        return 0

    result = run_subprocess(argv, cwd=cwd, timeout=args.timeout, env=env)
    parsed = parse_json_output(result.stdout) if args.output_format == "json" else None
    semantic_failure = semantic_json_failure(parsed) if args.output_format == "json" else None
    ok = result.returncode == 0 and semantic_failure is None
    payload.update(
        {
            "ok": ok,
            "status": "complete" if ok else "blocked",
            "failure_kind": semantic_failure or classify_failure(result.returncode, result.stdout, result.stderr),
            "data_safety": data_safety,
            "result": {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "json": parsed,
            },
        }
    )
    write_result_artifacts(artifacts, result, payload)
    json_print(payload)
    return 0 if ok else 1


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--grok-bin", help="Path or command name for Grok Build CLI.")
    parser.add_argument("--cwd", default=os.getcwd(), help="Trusted project directory to run Grok in.")
    parser.add_argument("--timeout", type=int, default=600, help="Subprocess timeout in seconds.")
    parser.add_argument("--compat", choices=["dot-only", "all", "none"], default="dot-only")


def add_prompt_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--data-classification", choices=DATA_CLASSIFICATIONS, default="internal")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe wrapper for Grok Build CLI delegation.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check local Grok Build readiness.")
    add_common(doctor)
    doctor.add_argument("--no-auth-required", action="store_true", help="Do not fail when auth is missing.")
    doctor.set_defaults(func=do_doctor)

    probe = subparsers.add_parser("probe", help="Run a minimal GROK_READY smoke test.")
    add_common(probe)
    probe.add_argument("--run-id")
    probe.add_argument("--model")
    probe.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"])
    probe.add_argument("--dry-run", action="store_true")
    probe.set_defaults(func=do_probe)

    audit = subparsers.add_parser("audit-prompt", help="Check whether a prompt is safe for external Grok handoff.")
    add_prompt_args(audit)
    audit.set_defaults(func=do_audit_prompt)

    run = subparsers.add_parser("run", help="Run a bounded Grok Build delegation.")
    add_common(run)
    run.add_argument("--mode", choices=["read", "plan", "edit", "trusted", "mcp"], default="plan")
    add_prompt_args(run)
    run.add_argument("--output-format", choices=["plain", "json", "streaming-json"], default="plain")
    run.add_argument("--max-turns", type=int, default=8)
    run.add_argument("--model", default=DEFAULT_GROK_MODEL)
    run.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"])
    run.add_argument("--run-id")
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--allow-mcp", action="store_true")
    run.add_argument("--allow-subagents", action="store_true")
    run.add_argument("--allow-web", action="store_true")
    run.add_argument("--rule", action="append", default=[])
    run.add_argument("--allow", action="append", default=[])
    run.add_argument("--deny", action="append", default=[])
    run.set_defaults(func=do_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
