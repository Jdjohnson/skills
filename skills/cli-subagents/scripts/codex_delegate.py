#!/usr/bin/env python3
from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SECRET_ENV_NAMES = (
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "XAI_API_KEY",
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "OLLAMA_API_KEY",
    "OLLAMA_CLOUD_API_KEY",
)

CREDENTIAL_ENV_NAMES = (
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
)

DEFAULT_CODEX_CANDIDATES = (
    "/opt/homebrew/bin/codex",
    "/usr/local/bin/codex",
    "~/.local/bin/codex",
)

DEFAULT_CODEX_MODEL = "gpt-5.6-sol"
DEFAULT_CODEX_EFFORT = "medium"
EFFORTS = ("medium", "high", "xhigh", "max")
DATA_CLASSIFICATIONS = ("public", "internal", "sanitized", "client-private")
MODES = ("read", "plan", "edit")

MODE_PREFACE = {
    "read": (
        "You are a read-only reviewer. Inspect and reason about the project, "
        "but do not write, edit, delete, move, install, commit, push, or run mutating commands. "
        "Return findings and evidence in plain text."
    ),
    "plan": (
        "You are a planning reviewer. Inspect and reason about the project, "
        "but do not write, edit, delete, move, install, commit, push, or run mutating commands. "
        "Return a concise implementation plan, risks, and verification steps."
    ),
    "edit": (
        "You are an editing delegate. You may inspect the project, modify files only under the trusted cwd, "
        "and run relevant existing validation commands to complete the task. "
        "Do not write outside the cwd, delete unrelated files, install packages, change dependency lockfiles "
        "unless explicitly requested, commit, push, publish, or run destructive commands. "
        "Return a concise summary of files changed, validation performed, and remaining issues."
    ),
}

MODE_SANDBOX = {
    "read": "read-only",
    "plan": "read-only",
    "edit": "workspace-write",
}


@dataclass
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str


def redact(text: str | bytes, env: dict[str, str] | None = None) -> str:
    # Timeout paths can hand us bytes (subprocess captures before decode).
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    if not text:
        return text

    env = env or os.environ
    redacted = text
    for name in SECRET_ENV_NAMES:
        value = env.get(name)
        if value and len(value) >= 4:
            redacted = redacted.replace(value, f"<redacted:{name}>")

    redacted = re.sub(r"sk-[A-Za-z0-9_-]{12,}", "<redacted:api-key>", redacted)
    redacted = re.sub(r"xai-[A-Za-z0-9_-]{8,}", "<redacted:xai-key>", redacted)
    redacted = re.sub(r"AIza[0-9A-Za-z_-]{20,}", "<redacted:google-api-key>", redacted)
    redacted = re.sub(r"(api[_-]?key[\"':=\s]+)[A-Za-z0-9._~+/=-]{12,}", r"\1<redacted:api-key>", redacted, flags=re.IGNORECASE)
    redacted = re.sub(
        r"(Bearer\s+)[A-Za-z0-9._~+/=-]{12,}",
        r"\1<redacted:bearer-token>",
        redacted,
        flags=re.IGNORECASE,
    )
    redacted = re.sub(
        r"([\"']?set-cookie[\"']?\s*[:=]\s*[\"']?)[^\"\r\n]+",
        r"\1<redacted:cookie>",
        redacted,
        flags=re.IGNORECASE,
    )
    redacted = re.sub(
        r"/Users/[^ \n\"']+/\.codex/auth\.json",
        "~/.codex/auth.json",
        redacted,
    )
    return redacted


def json_print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def default_candidates() -> tuple[str, ...]:
    override = os.environ.get("CODEX_DELEGATE_TEST_CANDIDATES")
    if override:
        return tuple(item for item in override.split(os.pathsep) if item)
    return DEFAULT_CODEX_CANDIDATES


def find_codex(codex_bin: str | None) -> dict[str, Any]:
    if codex_bin:
        if os.sep in codex_bin:
            candidate = Path(codex_bin).expanduser()
            resolved = str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None
        else:
            resolved = shutil.which(codex_bin)
    else:
        resolved = shutil.which("codex")
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
            # Never let the child inherit a live stdin pipe — codex exec
            # blocks reading it and hangs to timeout.
            stdin=subprocess.DEVNULL,
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


@contextmanager
def isolated_codex_env() -> Any:
    source_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    with tempfile.TemporaryDirectory(prefix="codex-delegate-") as raw_temp:
        temp_home = Path(raw_temp)
        auth_file = source_home / "auth.json"
        if auth_file.is_file():
            copied_auth = temp_home / "auth.json"
            shutil.copy2(auth_file, copied_auth)
            copied_auth.chmod(0o600)
        env = os.environ.copy()
        env["CODEX_HOME"] = str(temp_home)
        yield env


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


def parse_jsonl_events(output: str) -> list[Any]:
    events: list[Any] = []
    for line in output.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def _extract_text_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return []
    if isinstance(value, list):
        text: list[str] = []
        for item in value:
            text.extend(_extract_text_values(item))
        return text
    if not isinstance(value, dict):
        return []

    text: list[str] = []
    if value.get("type") in ("agent_message", "assistant_message", "message") or "msg" in value:
        for key in ("message", "text", "content", "last_agent_message"):
            item = value.get(key)
            if isinstance(item, str):
                text.append(item)
    for key in ("msg", "item", "content", "parts", "delta", "data"):
        if key in value:
            text.extend(_extract_text_values(value[key]))
    return text


def extract_response_text(last_message_file: Path | None, events: list[Any], stdout: str) -> str:
    if last_message_file is not None and last_message_file.is_file():
        try:
            text = last_message_file.read_text(encoding="utf-8").strip()
            if text:
                return text
        except OSError:
            pass
    if events:
        text = "\n".join(_extract_text_values(events)).strip()
        return text
    return ""


def is_ready_response(text: str) -> bool:
    return re.fullmatch(r"CODEX_READY[.!?]?", text.strip()) is not None


def classify_failure(returncode: int, stdout: str, stderr: str) -> str | None:
    text = f"{stdout}\n{stderr}".lower()
    if returncode == 0:
        if not stdout.strip() and not stderr.strip():
            return "empty_result"
        return None

    if returncode == 124:
        return "timeout"
    if returncode == 127 or "no such file" in text or "command not found" in text:
        return "missing_cli"
    if "not logged in" in text or "login" in text or "authentication" in text or "401" in text:
        return "missing_auth"
    if "invalid api key" in text or "unauthorized" in text or "forbidden" in text:
        return "missing_auth"
    if "usage limit" in text or "rate limit" in text or "429" in text or "quota" in text:
        return "rate_limit_or_quota"
    if "unable to connect" in text or "enotfound" in text or "econnreset" in text or "stream disconnected" in text:
        return "network_or_sandbox"
    if "ssl" in text or "tls" in text or "certificate" in text or "could not resolve host" in text:
        return "network_or_sandbox"
    if "operation not permitted" in text and (
        "network" in text or "socket" in text or "sandbox" in text or "app-server" in text
    ):
        return "network_or_sandbox"
    if "sandbox" in text and ("denied" in text or "rejected" in text or "failed" in text):
        return "permission_or_policy"
    if "approval" in text or "permission" in text or "blocked for safety" in text or "denied" in text:
        return "permission_or_policy"
    if "model" in text and ("not available" in text or "unsupported" in text or "retired" in text or "not found" in text):
        return "model_missing"
    if "unexpected argument" in text or "unknown option" in text or "invalid option" in text:
        return "unsupported_flag"
    if "not inside a trusted directory" in text or "git repo" in text:
        return "untrusted_directory"
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
    run_dir = cwd / ".tmp" / "codex" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    prompt_file = run_dir / "prompt.md"
    last_message_file = run_dir / "last-message.txt"
    if last_message_file.exists():
        last_message_file.unlink()
    write_text(prompt_file, prompt)
    write_text(run_dir / "git-status-before.txt", git_status(cwd))
    return {
        "run_dir": str(run_dir),
        "prompt_file": str(prompt_file),
        "stdout": str(run_dir / "stdout.log"),
        "stderr": str(run_dir / "stderr.log"),
        "last_message": str(last_message_file),
        "meta": str(run_dir / "meta.json"),
        "git_status_before": str(run_dir / "git-status-before.txt"),
        "git_status_after": str(run_dir / "git-status-after.txt"),
    }


def command_preview(argv: list[str], prompt: str | None = None, env: dict[str, str] | None = None) -> list[str]:
    preview: list[str] = []
    replaced_prompt = False
    for item in argv:
        if prompt is not None and item == prompt and not replaced_prompt:
            preview.append(f"<prompt:{len(prompt)} chars>")
            replaced_prompt = True
        else:
            preview.append(redact(item, env))
    return preview


def build_delegation_prompt(mode: str, prompt: str) -> str:
    return f"{MODE_PREFACE[mode]}\n\nUser task:\n{prompt}"


def build_codex_argv(
    args: argparse.Namespace,
    prompt: str,
    last_message_path: str,
    *,
    mode: str,
) -> list[str]:
    codex = find_codex(args.codex_bin)["path"] or args.codex_bin or "codex"
    model = args.model or DEFAULT_CODEX_MODEL
    effort = getattr(args, "effort", None) or DEFAULT_CODEX_EFFORT
    argv = [
        codex,
        "exec",
        "--cd",
        args.cwd,
        "--skip-git-repo-check",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--sandbox",
        # --full-access uses Codex's native unrestricted sandbox level; runs
        # are still headless with approval_policy=never.
        "danger-full-access" if getattr(args, "full_access", False) else MODE_SANDBOX[mode],
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "-c",
        'approval_policy="never"',
        "--color",
        "never",
        "--json",
        "--output-last-message",
        last_message_path,
        prompt,
    ]
    return argv


def summarize_login_status(result: CommandResult) -> dict[str, Any]:
    text = (result.stdout or result.stderr).strip()
    lower = text.lower()
    env_credentials = present_credentials()
    ok = result.returncode == 0 and "logged in" in lower and "not logged in" not in lower
    method = "codex-login-status" if ok else "environment" if env_credentials else "missing"
    return {
        "ok": ok or bool(env_credentials),
        "method": method,
        "env_credentials": env_credentials,
        "status_text": text or None,
        "returncode": result.returncode,
    }


def collect_preflight(args: argparse.Namespace, require_auth: bool = True) -> dict[str, Any]:
    issues: list[str] = []
    binary = find_codex(getattr(args, "codex_bin", None))
    version: dict[str, Any] = {"ok": False, "text": None}
    auth: dict[str, Any] = {
        "ok": False,
        "method": "missing",
        "env_credentials": present_credentials(),
    }
    model = {
        "ok": True,
        "provider": "openai",
        "model": getattr(args, "model", DEFAULT_CODEX_MODEL) or DEFAULT_CODEX_MODEL,
        "effort": getattr(args, "effort", None) or DEFAULT_CODEX_EFFORT,
        "note": "model availability is validated at run time; failures classify as model_missing",
    }

    cwd = validate_cwd(getattr(args, "cwd", None))
    if not cwd["ok"]:
        issues.extend(cwd["issues"])

    if not binary["found"]:
        issues.append("codex_cli_missing")
    else:
        version_result = run_subprocess([binary["path"], "--version"], timeout=15)
        version = {
            "ok": version_result.returncode == 0,
            "text": (version_result.stdout or version_result.stderr).strip() or None,
            "returncode": version_result.returncode,
        }
        if not version["ok"]:
            issues.append("codex_version_failed")

        auth_result = run_subprocess([binary["path"], "login", "status"], timeout=30)
        auth = summarize_login_status(auth_result)
        auth_failure = classify_failure(auth_result.returncode, auth_result.stdout, auth_result.stderr)
        if not auth["ok"] and require_auth:
            issues.append("codex_auth_missing" if auth_failure in {None, "unknown"} else auth_failure)

    issues = list(dict.fromkeys(issues))
    return {
        "ok": not issues,
        "status": "ready" if not issues else "blocked",
        "issues": issues,
        "codex": binary | {"version": version},
        "auth": auth,
        "model": model,
        "cwd": cwd,
    }


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
    args.mode = "read"

    payload = collect_preflight(args, require_auth=True)
    if not payload["ok"]:
        payload["probe"] = {"ok": False, "stdout": "", "stderr": "", "returncode": None}
        json_print(payload)
        return 2

    prompt = "Reply exactly CODEX_READY."
    cwd = Path(payload["cwd"]["path"])
    run_id = safe_run_id(args.run_id or "probe")
    artifacts = prepare_artifacts(cwd, run_id, prompt)
    argv = build_codex_argv(args, prompt, artifacts["last_message"], mode="read")

    if args.dry_run:
        payload.update(
            {
                "ok": True,
                "status": "dry-run",
                "command": {"argv": command_preview(argv, prompt)},
                "artifacts": artifacts,
            }
        )
        write_text(Path(artifacts["meta"]), json.dumps(payload, indent=2, sort_keys=True))
        json_print(payload)
        return 0

    with isolated_codex_env() as env:
        result = run_subprocess(argv, cwd=cwd, timeout=args.timeout, env=env)
    events = parse_jsonl_events(result.stdout)
    response_text = extract_response_text(Path(artifacts["last_message"]), events, result.stdout)
    exact_ready = result.returncode == 0 and is_ready_response(response_text)
    payload.update(
        {
            "ok": exact_ready,
            "status": "ready" if exact_ready else "blocked",
            "failure_kind": None
            if exact_ready
            else classify_failure(result.returncode, result.stdout, result.stderr) or "unexpected_probe_response",
            "command": {"argv": command_preview(argv, prompt)},
            "artifacts": artifacts,
            "probe": {
                "ok": exact_ready,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "response_text": response_text,
                "returncode": result.returncode,
            },
        }
    )
    write_result_artifacts(artifacts, result, payload)
    json_print(payload)
    return 0 if exact_ready else 1


def do_audit_prompt(args: argparse.Namespace) -> int:
    try:
        read_prompt(args)
    except (OSError, ValueError) as exc:
        json_print({"ok": False, "status": "blocked", "issues": [str(exc)]})
        return 2

    json_print({"ok": True, "status": "safe", "issues": []})
    return 0


def do_run(args: argparse.Namespace) -> int:
    try:
        prompt = read_prompt(args)
    except (OSError, ValueError) as exc:
        json_print({"ok": False, "status": "blocked", "issues": [str(exc)]})
        return 2

    payload = collect_preflight(args, require_auth=True)
    if not payload["ok"]:
        payload["result"] = None
        json_print(payload)
        return 2

    delegation_prompt = build_delegation_prompt(args.mode, prompt)
    cwd = Path(payload["cwd"]["path"])
    run_id = safe_run_id(args.run_id)
    artifacts = prepare_artifacts(cwd, run_id, delegation_prompt)
    argv = build_codex_argv(args, delegation_prompt, artifacts["last_message"], mode=args.mode)
    payload.update(
        {
            "mode": args.mode,
            "effort": getattr(args, "effort", None) or DEFAULT_CODEX_EFFORT,
            "command": {"argv": command_preview(argv, delegation_prompt)},
            "artifacts": artifacts,
        }
    )

    if args.dry_run:
        payload.update({"ok": True, "status": "dry-run", "result": None})
        write_text(Path(artifacts["meta"]), json.dumps(payload, indent=2, sort_keys=True))
        json_print(payload)
        return 0

    with isolated_codex_env() as env:
        result = run_subprocess(argv, cwd=cwd, timeout=args.timeout, env=env)
    events = parse_jsonl_events(result.stdout)
    response_text = extract_response_text(Path(artifacts["last_message"]), events, result.stdout)
    ok = result.returncode == 0 and bool(response_text.strip())
    payload.update(
        {
            "ok": ok,
            "status": "complete" if ok else "blocked",
            "failure_kind": None if ok else classify_failure(result.returncode, result.stdout, result.stderr),
            "mode": args.mode,
            "result": {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "response_text": response_text,
            },
        }
    )
    write_result_artifacts(artifacts, result, payload)
    json_print(payload)
    return 0 if ok else 1


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--codex-bin", help="Path or command name for Codex CLI.")
    parser.add_argument("--cwd", default=os.getcwd(), help="Trusted project directory to run Codex in.")
    parser.add_argument("--timeout", type=int, default=1200, help="Subprocess timeout in seconds.")
    parser.add_argument("--model", default=DEFAULT_CODEX_MODEL)
    parser.add_argument("--effort", choices=EFFORTS, default=DEFAULT_CODEX_EFFORT, help="Reasoning effort for the run.")


def add_prompt_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--data-classification", choices=DATA_CLASSIFICATIONS, default="internal")
    parser.add_argument(
        "--allow-private-data",
        action="store_true",
        help="Waive the private-data block (requires the user's explicit instruction); findings are still reported.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe wrapper for Codex CLI delegation.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check local Codex readiness.")
    add_common(doctor)
    doctor.add_argument("--no-auth-required", action="store_true", help="Do not fail when auth is missing.")
    doctor.set_defaults(func=do_doctor)

    probe = subparsers.add_parser("probe", help="Run a minimal CODEX_READY smoke test.")
    add_common(probe)
    probe.add_argument("--run-id")
    probe.add_argument("--dry-run", action="store_true")
    probe.set_defaults(func=do_probe)

    audit = subparsers.add_parser("audit-prompt", help="Compatibility check; task context follows the active workspace policy.")
    add_prompt_args(audit)
    audit.set_defaults(func=do_audit_prompt)

    run = subparsers.add_parser("run", help="Run a bounded Codex delegation.")
    add_common(run)
    run.add_argument("--mode", choices=MODES, default="plan")
    add_prompt_args(run)
    run.add_argument("--run-id")
    run.add_argument("--dry-run", action="store_true")
    run.add_argument(
        "--full-access",
        action="store_true",
        help="Run Codex with its unrestricted sandbox (danger-full-access) instead of the mode's sandbox.",
    )
    run.set_defaults(func=do_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
