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
    "OLLAMA_API_KEY",
    "OLLAMA_CLOUD_API_KEY",
    "OPENCODE_SERVER_PASSWORD",
    "OPENCODE_SERVER_USERNAME",
    "OPENCODE_AUTH_TOKEN",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "XAI_API_KEY",
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
)

CREDENTIAL_ENV_NAMES = (
    "OLLAMA_API_KEY",
    "OLLAMA_CLOUD_API_KEY",
    "OPENCODE_AUTH_TOKEN",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "XAI_API_KEY",
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
)

DEFAULT_OPENCODE_CANDIDATES = (
    "~/.local/bin/opencode",
    "/opt/homebrew/bin/opencode",
    "/usr/local/bin/opencode",
)

DEFAULT_OPENCODE_MODEL = "ollama-cloud/glm-5.2"
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


@dataclass
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str


def redact(text: str | bytes, env: dict[str, str] | None = None) -> str:
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
        r"/Users/[^ \n\"']+/.local/share/opencode/auth\.json",
        "~/.local/share/opencode/auth.json",
        redacted,
    )
    return redacted


def json_print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def default_candidates() -> tuple[str, ...]:
    override = os.environ.get("OPENCODE_DELEGATE_TEST_CANDIDATES")
    if override:
        return tuple(item for item in override.split(os.pathsep) if item)
    return DEFAULT_OPENCODE_CANDIDATES


def find_opencode(opencode_bin: str | None) -> dict[str, Any]:
    if opencode_bin:
        if os.sep in opencode_bin:
            candidate = Path(opencode_bin).expanduser()
            resolved = str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None
        else:
            resolved = shutil.which(opencode_bin)
    else:
        resolved = shutil.which("opencode")
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


def parse_json_output(output: str) -> Any:
    stripped = output.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    items: list[Any] = []
    for line in stripped.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            return None
    return items or None


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
    for key in ("result", "text", "content", "message"):
        item = value.get(key)
        if isinstance(item, str):
            text.append(item)
    for key in ("message", "content", "parts", "part", "delta", "data"):
        if key in value:
            text.extend(_extract_text_values(value[key]))
    return text


def extract_response_text(parsed: Any, stdout: str) -> str:
    if parsed is None:
        return stdout.strip()
    text = "".join(_extract_text_values(parsed)).strip()
    return text


def is_ready_response(text: str) -> bool:
    return re.fullmatch(r"OPENCODE_READY[.!?]?", text.strip()) is not None


def classify_failure(returncode: int, stdout: str, stderr: str) -> str | None:
    text = f"{stdout}\n{stderr}".lower()
    if returncode == 0:
        if not stdout.strip() and not stderr.strip():
            return "empty_result"
        return None

    if returncode == 127 or "no such file" in text or "command not found" in text:
        return "missing_cli"
    if returncode == 124:
        return "timeout"
    if "no such column" in text or "sqlite" in text or "database schema" in text or "opencode.db" in text:
        return "state_schema_incompatible"
    if "not logged in" in text or "sign in" in text or "login" in text or "authentication required" in text:
        return "missing_auth"
    if "invalid api key" in text or "unauthorized" in text or "oauth" in text or "forbidden" in text:
        return "missing_auth"
    if "unable to connect" in text or "enotfound" in text or "econnreset" in text:
        return "network_or_sandbox"
    if "ssl" in text or "tls" in text or "certificate" in text or "could not resolve host" in text:
        return "network_or_sandbox"
    if "filesystem.open" in text and ".local/share/opencode" in text:
        return "network_or_sandbox"
    if "operation not permitted" in text and ("network" in text or "socket" in text or "sandbox" in text):
        return "network_or_sandbox"
    if "permission" in text or "approval" in text or "blocked for safety" in text or "denied" in text:
        return "permission_or_policy"
    if "rate limit" in text or "429" in text or "quota" in text or "credit" in text:
        return "rate_limit_or_quota"
    if "model" in text and ("not available" in text or "unsupported" in text or "retired" in text or "not found" in text):
        return "model_missing"
    if "unexpected argument" in text or "unknown option" in text or "invalid option" in text:
        return "unsupported_flag"
    return "unknown"


def semantic_json_failure(parsed: Any, response_text: str) -> str | None:
    if parsed is None:
        return None

    lower = json.dumps(parsed).lower()
    if "cancelled" in lower or "canceled" in lower:
        return "cancelled"
    if not response_text.strip():
        return "empty_result"
    return None


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
    run_dir = cwd / ".tmp" / "opencode" / run_id
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


def build_opencode_argv(args: argparse.Namespace, prompt: str, *, probe: bool = False) -> list[str]:
    opencode = find_opencode(args.opencode_bin)["path"] or args.opencode_bin or "opencode"
    model = args.model or DEFAULT_OPENCODE_MODEL
    title = args.title or ("opencode-probe" if probe else f"opencode-{args.mode}")
    argv = [
        opencode,
        "run",
        prompt,
        "--pure",
        "--dir",
        args.cwd,
        "--model",
        model,
        "--format",
        "json",
        "--title",
        title,
    ]
    if probe or args.mode in {"read", "plan"}:
        argv.extend(["--agent", "plan"])
    if getattr(args, "variant", None):
        argv.extend(["--variant", args.variant])
    return argv


def summarize_auth_list(result: CommandResult, provider: str) -> dict[str, Any]:
    text = (result.stdout or result.stderr).strip()
    lower = text.lower()
    env_credentials = present_credentials()
    provider_names = {provider.lower(), provider.lower().replace("-", " ")}
    provider_present = any(name and name in lower for name in provider_names)
    ok = result.returncode == 0 and provider_present
    method = "opencode-auth-list" if ok else "environment" if env_credentials else "missing"
    return {
        "ok": ok or bool(env_credentials),
        "method": method,
        "env_credentials": env_credentials,
        "provider": provider,
        "provider_present": provider_present,
        "status_text": text or None,
        "returncode": result.returncode,
    }


def collect_preflight(args: argparse.Namespace, require_auth: bool = True, require_model: bool = True) -> dict[str, Any]:
    issues: list[str] = []
    binary = find_opencode(getattr(args, "opencode_bin", None))
    version: dict[str, Any] = {"ok": False, "text": None}
    auth: dict[str, Any] = {
        "ok": False,
        "method": "missing",
        "env_credentials": present_credentials(),
        "provider": None,
        "provider_present": False,
    }
    requested_model = getattr(args, "model", DEFAULT_OPENCODE_MODEL) or DEFAULT_OPENCODE_MODEL
    provider = requested_model.split("/", 1)[0] if "/" in requested_model else ""
    model: dict[str, Any] = {
        "ok": False,
        "provider": provider,
        "model": requested_model,
        "available": [],
    }

    cwd = validate_cwd(getattr(args, "cwd", None))
    if not cwd["ok"]:
        issues.extend(cwd["issues"])

    if not binary["found"]:
        issues.append("opencode_cli_missing")
    else:
        version_result = run_subprocess([binary["path"], "--version"], timeout=15)
        version = {
            "ok": version_result.returncode == 0,
            "text": (version_result.stdout or version_result.stderr).strip() or None,
            "returncode": version_result.returncode,
        }
        if not version["ok"]:
            issues.append("opencode_version_failed")

        auth_result = run_subprocess([binary["path"], "auth", "list"], timeout=30)
        auth = summarize_auth_list(auth_result, provider)
        auth_failure = classify_failure(auth_result.returncode, auth_result.stdout, auth_result.stderr)
        if not auth["ok"] and require_auth:
            issues.append("opencode_auth_missing" if auth_failure in {None, "unknown"} else auth_failure)

        models_result = run_subprocess([binary["path"], "models", provider], timeout=60)
        model_text = (models_result.stdout or models_result.stderr).strip()
        available = sorted(set(re.findall(rf"{re.escape(provider)}/[A-Za-z0-9_.:-]+", model_text)))
        model = {
            "ok": models_result.returncode == 0 and model["model"] in available,
            "provider": provider,
            "model": model["model"],
            "available": available,
            "returncode": models_result.returncode,
            "status_text": model_text or None,
        }
        if require_model and not model["ok"]:
            if models_result.returncode != 0:
                issues.append(classify_failure(models_result.returncode, models_result.stdout, models_result.stderr) or "model_lookup_failed")
            else:
                issues.append("model_missing")

    issues = list(dict.fromkeys(issues))
    return {
        "ok": not issues,
        "status": "ready" if not issues else "blocked",
        "issues": issues,
        "opencode": binary | {"version": version},
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
    payload = collect_preflight(args, require_auth=not args.no_auth_required, require_model=not args.no_model_required)
    json_print(payload)
    return 0 if payload["ok"] else 2


def do_probe(args: argparse.Namespace) -> int:
    if not args.allow_inactive:
        json_print({
            "ok": False,
            "active": False,
            "status": "inactive",
            "issues": ["opencode_inactive_requires_explicit_opt_in"],
        })
        return 2
    args.mode = "read"
    args.title = getattr(args, "title", None)

    payload = collect_preflight(args, require_auth=True, require_model=True)
    if not payload["ok"]:
        payload["probe"] = {"ok": False, "stdout": "", "stderr": "", "returncode": None}
        json_print(payload)
        return 2

    prompt = "Reply exactly OPENCODE_READY."
    cwd = Path(payload["cwd"]["path"])
    run_id = safe_run_id(args.run_id or "probe")
    artifacts = prepare_artifacts(cwd, run_id, prompt)
    argv = build_opencode_argv(args, prompt, probe=True)

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

    result = run_subprocess(argv, cwd=cwd, timeout=args.timeout)
    parsed = parse_json_output(result.stdout)
    response_text = extract_response_text(parsed, result.stdout)
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
                "json": parsed,
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

    if not args.allow_inactive:
        json_print({
            "ok": False,
            "active": False,
            "status": "inactive",
            "issues": ["opencode_inactive_requires_explicit_opt_in"],
        })
        return 2

    payload = collect_preflight(args, require_auth=True, require_model=True)
    if not payload["ok"]:
        payload["result"] = None
        json_print(payload)
        return 2

    delegation_prompt = build_delegation_prompt(args.mode, prompt)
    cwd = Path(payload["cwd"]["path"])
    run_id = safe_run_id(args.run_id)
    artifacts = prepare_artifacts(cwd, run_id, delegation_prompt)
    argv = build_opencode_argv(args, delegation_prompt)
    payload.update(
        {
            "mode": args.mode,
            "command": {"argv": command_preview(argv, delegation_prompt)},
            "artifacts": artifacts,
        }
    )

    if args.dry_run:
        payload.update({"ok": True, "status": "dry-run", "result": None})
        write_text(Path(artifacts["meta"]), json.dumps(payload, indent=2, sort_keys=True))
        json_print(payload)
        return 0

    result = run_subprocess(argv, cwd=cwd, timeout=args.timeout)
    parsed = parse_json_output(result.stdout)
    response_text = extract_response_text(parsed, result.stdout)
    semantic_failure = semantic_json_failure(parsed, response_text)
    ok = result.returncode == 0 and semantic_failure is None and bool(response_text.strip())
    payload.update(
        {
            "ok": ok,
            "status": "complete" if ok else "blocked",
            "failure_kind": semantic_failure or classify_failure(result.returncode, result.stdout, result.stderr),
            "mode": args.mode,
            "result": {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "response_text": response_text,
                "json": parsed,
            },
        }
    )
    write_result_artifacts(artifacts, result, payload)
    json_print(payload)
    return 0 if ok else 1


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--opencode-bin", help="Path or command name for OpenCode CLI.")
    parser.add_argument("--cwd", default=os.getcwd(), help="Trusted project directory to run OpenCode in.")
    parser.add_argument("--timeout", type=int, default=600, help="Subprocess timeout in seconds.")
    parser.add_argument("--model", default=DEFAULT_OPENCODE_MODEL)


def add_prompt_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--data-classification", choices=DATA_CLASSIFICATIONS, default="internal")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe wrapper for OpenCode CLI delegation.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check local OpenCode readiness.")
    add_common(doctor)
    doctor.add_argument("--no-auth-required", action="store_true", help="Do not fail when auth is missing.")
    doctor.add_argument("--no-model-required", action="store_true", help="Do not fail when the default model is missing.")
    doctor.set_defaults(func=do_doctor)

    probe = subparsers.add_parser("probe", help="Run a minimal OPENCODE_READY smoke test.")
    add_common(probe)
    probe.add_argument("--run-id")
    probe.add_argument("--title")
    probe.add_argument("--variant")
    probe.add_argument("--dry-run", action="store_true")
    probe.add_argument("--allow-inactive", action="store_true")
    probe.set_defaults(func=do_probe)

    audit = subparsers.add_parser("audit-prompt", help="Compatibility check; task context follows the active workspace policy.")
    add_prompt_args(audit)
    audit.set_defaults(func=do_audit_prompt)

    run = subparsers.add_parser("run", help="Run a bounded OpenCode delegation.")
    add_common(run)
    run.add_argument("--mode", choices=MODES, default="plan")
    add_prompt_args(run)
    run.add_argument("--run-id")
    run.add_argument("--title")
    run.add_argument("--variant")
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--allow-inactive", action="store_true")
    run.set_defaults(func=do_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
