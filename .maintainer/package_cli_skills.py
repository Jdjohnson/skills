#!/usr/bin/env python3
from __future__ import annotations

import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_DIR = ROOT / "downloads" / "cli-skills"
CLI_SKILLS = ("claude-code", "codex", "grok-build", "opencode")
SKIP_NAMES = {"__pycache__", ".DS_Store"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def iter_skill_files(skill: str) -> list[Path]:
    skill_root = ROOT / "skills" / skill
    files: list[Path] = []
    for path in skill_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_NAMES for part in path.parts):
            continue
        if path.suffix in SKIP_SUFFIXES:
            continue
        files.append(path)
    return sorted(files)


def write_zip(skill: str) -> Path:
    zip_path = DOWNLOAD_DIR / f"{skill}-skill.zip"
    skill_root = ROOT / "skills" / skill
    if not (skill_root / "SKILL.md").exists():
        raise SystemExit(f"missing skills/{skill}/SKILL.md")

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in iter_skill_files(skill):
            archive.write(path, path.relative_to(ROOT).as_posix())
    return zip_path


def main() -> None:
    for skill in CLI_SKILLS:
        zip_path = write_zip(skill)
        print(zip_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
