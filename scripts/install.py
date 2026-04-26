#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def ensure_installable(path: Path, force: bool, noun: str) -> None:
    if (path.exists() or path.is_symlink()) and not force:
        raise SystemExit(f"Refusing to overwrite existing {noun}: {path}")


def is_same_symlink(dest: Path, src: Path) -> bool:
    if not dest.is_symlink():
        return False
    try:
        return dest.resolve() == src.resolve()
    except FileNotFoundError:
        return False


def is_same_file_content(path: Path, content: str) -> bool:
    if not path.exists() or path.is_symlink() or not path.is_file():
        return False
    try:
        return path.read_text() == content
    except OSError:
        return False


def install_path(src: Path, dest: Path, mode: str, force: bool) -> None:
    if dest.exists() or dest.is_symlink():
        if not force:
            raise SystemExit(f"Refusing to overwrite existing path: {dest}")
        remove_existing(dest)

    dest.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        dest.symlink_to(src, target_is_directory=src.is_dir())
    else:
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() or path.is_symlink():
        if not force:
            raise SystemExit(f"Refusing to overwrite existing file: {path}")
        remove_existing(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Install run-workflow for Codex and Claude Code.")
    parser.add_argument("--host", choices=["codex", "claude", "both"], default="both")
    parser.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    planner_skill = repo_root / "skills" / "run"
    runner_script = repo_root / "skills" / "run" / "scripts" / "run.sh"

    home = Path.home()
    installs = []

    if args.host in {"codex", "both"}:
        codex_root = Path(os.environ.get("CODEX_HOME", home / ".codex")) / "skills"
        installs.append((planner_skill, codex_root / "run"))

    if args.host in {"claude", "both"}:
        claude_root = home / ".claude"
        installs.append((planner_skill, claude_root / "skills" / "run"))

    for src, dest in installs:
        if args.mode == "symlink" and is_same_symlink(dest, src):
            continue
        ensure_installable(dest, args.force, "path")

    command_target = None
    command_body = None
    if args.host in {"claude", "both"}:
        command_target = home / ".claude" / "commands" / "run.md"
        command_body = f"Read and follow `{home / '.claude' / 'skills' / 'run' / 'SKILL.md'}`.\n"
        if not (command_target and is_same_file_content(command_target, command_body)):
            ensure_installable(command_target, args.force, "file")

    runner_targets = [
        home / ".local" / "bin" / "run-workflow",
        home / ".local" / "bin" / "run-skill",
    ]
    for runner_target in runner_targets:
        if not is_same_symlink(runner_target, runner_script):
            ensure_installable(runner_target, args.force, "path")

    for src, dest in installs:
        if args.mode == "symlink" and is_same_symlink(dest, src):
            continue
        install_path(src, dest, args.mode, args.force)

    if command_target is not None and command_body is not None and not is_same_file_content(command_target, command_body):
        write_file(command_target, command_body, args.force)

    for runner_target in runner_targets:
        if not is_same_symlink(runner_target, runner_script):
            install_path(runner_script, runner_target, "symlink", args.force)
        runner_target.chmod(0o755)

    primary_runner = runner_targets[0]
    compatibility_runner = runner_targets[1]
    print("Installed run-workflow.")
    print(f"Runner: {primary_runner}")
    print(f"Compatibility alias: {compatibility_runner}")
    bin_dir = primary_runner.parent
    if str(bin_dir) not in os.environ.get("PATH", "").split(":"):
        print(f"PATH note: add {bin_dir} to your PATH if run-workflow is not found.")
    print("Restart Claude Code or Codex to pick up the updated run planner cleanly.")


if __name__ == "__main__":
    main()
