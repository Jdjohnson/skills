from __future__ import annotations

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


@dataclass
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str


def redact(text: str | bytes, secret_env_names: tuple[str, ...]) -> str:
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    if not text:
        return text

    redacted = text
    for name in secret_env_names:
        value = os.environ.get(name)
        if value and len(value) >= 4:
            redacted = redacted.replace(value, f"<redacted:{name}>")

    redacted = re.sub(r"AIza[0-9A-Za-z_-]{20,}", "<redacted:google-api-key>", redacted)
    redacted = re.sub(r"sk-[A-Za-z0-9_-]{12,}", "<redacted:api-key>", redacted)
    redacted = re.sub(
        r"(Bearer\s+)[A-Za-z0-9._~+/=-]{12,}",
        r"\1<redacted:bearer-token>",
        redacted,
        flags=re.IGNORECASE,
    )
    return redacted


def run_subprocess(
    argv: list[str],
    *,
    cwd: Path | None,
    timeout: int,
    secret_env_names: tuple[str, ...],
) -> CommandResult:
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
            stdout=redact(completed.stdout, secret_env_names),
            stderr=redact(completed.stderr, secret_env_names),
        )
    except FileNotFoundError as exc:
        return CommandResult(argv=argv, returncode=127, stdout="", stderr=str(exc))
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            argv=argv,
            returncode=124,
            stdout=redact(exc.stdout or "", secret_env_names),
            stderr=redact(exc.stderr or f"Timed out after {timeout} seconds", secret_env_names),
        )


def json_print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def find_binary(explicit: str | None, command: str, candidates: tuple[str, ...]) -> str | None:
    if explicit:
        if os.sep in explicit:
            path = Path(explicit).expanduser()
            return str(path) if path.is_file() and os.access(path, os.X_OK) else None
        return shutil.which(explicit)

    found = shutil.which(command)
    if found:
        return found
    for candidate in candidates:
        path = Path(candidate).expanduser()
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
    return None


def validate_cwd(raw_cwd: str | None) -> dict[str, Any]:
    cwd = Path(raw_cwd or os.getcwd()).expanduser()
    try:
        resolved = cwd.resolve()
    except OSError as exc:
        return {"ok": False, "path": str(cwd), "issues": [f"cwd_resolve_failed:{exc}"]}

    issues: list[str] = []
    if not resolved.exists():
        issues.append("cwd_missing")
    elif not resolved.is_dir():
        issues.append("cwd_not_directory")

    home = Path.home().resolve()
    broad = {Path(resolved.anchor).resolve(), home}
    if home.parent != home:
        broad.add(home.parent)
    if Path("/Users").exists():
        broad.add(Path("/Users").resolve())
    if resolved in broad:
        issues.append("cwd_too_broad")

    return {"ok": not issues, "path": str(resolved), "issues": issues}


def read_prompt(args: Any) -> str:
    sources = [bool(args.prompt), bool(args.prompt_file), bool(args.stdin)]
    if sum(sources) != 1:
        raise ValueError("Provide exactly one of --prompt, --prompt-file, or --stdin.")
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).expanduser().read_text(encoding="utf-8")
    return sys.stdin.read()


def safe_run_id(raw: str | None) -> str:
    if raw:
        cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", raw).strip(".-")
        if cleaned:
            return cleaned[:80]
    return time.strftime("%Y%m%d-%H%M%S")


def prepare_artifacts(cwd: Path, provider: str, run_id: str, prompt: str) -> dict[str, str]:
    root = cwd / ".cli-subagents" / "runs" / provider / run_id
    root.mkdir(parents=True, exist_ok=False)
    prompt_file = root / "prompt.txt"
    prompt_file.write_text(prompt, encoding="utf-8")
    return {
        "run_dir": str(root),
        "prompt_file": str(prompt_file),
        "stdout": str(root / "stdout.log"),
        "stderr": str(root / "stderr.log"),
        "meta": str(root / "meta.json"),
    }


def write_artifacts(artifacts: dict[str, str], result: CommandResult, payload: dict[str, Any]) -> None:
    Path(artifacts["stdout"]).write_text(result.stdout, encoding="utf-8")
    Path(artifacts["stderr"]).write_text(result.stderr, encoding="utf-8")
    Path(artifacts["meta"]).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def parse_json(output: str) -> Any:
    stripped = output.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        items: list[Any] = []
        for line in stripped.splitlines():
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                return None
        return items or None


def text_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(text_values(item))
        return values
    if not isinstance(value, dict):
        return []

    values: list[str] = []
    for key in ("response", "result", "text", "content", "message"):
        item = value.get(key)
        if isinstance(item, str):
            values.append(item)
    for key in ("parts", "part", "delta", "data"):
        if key in value:
            values.extend(text_values(value[key]))
    return values


def classify_failure(returncode: int, stdout: str, stderr: str) -> str | None:
    if returncode == 0:
        return None
    text = f"{stdout}\n{stderr}".lower()
    if returncode == 127 or "command not found" in text or "no such file" in text:
        return "missing_cli"
    if "not logged in" in text or "authentication required" in text or "sign in" in text:
        return "missing_auth"
    if "unauthorized" in text or "invalid api key" in text or "forbidden" in text:
        return "authentication_error"
    if (
        "ineligibletiererror" in text
        or "unsupported_client" in text
        or "client is no longer supported" in text
    ):
        return "unsupported_account_tier"
    if "rate limit" in text or "quota" in text or "429" in text or "credit" in text:
        return "rate_limit_or_quota"
    if "model" in text and ("not found" in text or "unsupported" in text or "not available" in text):
        return "model_missing"
    if "operation not permitted" in text or "permission denied" in text or "sandbox" in text:
        return "permission_or_sandbox"
    if "unable to connect" in text or "enotfound" in text or "could not resolve" in text:
        return "network"
    if returncode == 124:
        return "timeout"
    return "unknown"
