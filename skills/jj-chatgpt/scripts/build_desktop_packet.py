#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

DEFAULT_MAX_UPLOAD_FILES = 20
SLUG_PATTERN = re.compile(r"[^a-z0-9]+")


@dataclass
class CopiedFile:
    source_path: str
    packet_name: str


@dataclass
class PacketBuildResult:
    packet_dir: str
    prompt_path: str
    included_files: list[CopiedFile]
    omitted_files: list[str]


def normalize_slug(value: str) -> str:
    slug = SLUG_PATTERN.sub("-", value.strip().lower()).strip("-")
    return slug or "order"


def unique_upload_files(paths: Iterable[str]) -> list[Path]:
    unique_paths: list[Path] = []
    seen: set[Path] = set()

    for raw_path in paths:
        resolved = Path(raw_path).expanduser().resolve()
        if resolved in seen:
            continue
        if not resolved.exists():
            raise FileNotFoundError(f"upload file not found: {resolved}")
        if not resolved.is_file():
            raise ValueError(f"upload path is not a file: {resolved}")
        seen.add(resolved)
        unique_paths.append(resolved)

    return unique_paths


def allocate_packet_name(original_name: str, used_names: set[str]) -> str:
    candidate = original_name
    if candidate not in used_names:
        used_names.add(candidate)
        return candidate

    original_path = Path(original_name)
    stem = original_path.stem
    suffix = original_path.suffix
    index = 2

    while True:
        candidate = f"{stem}-{index}{suffix}"
        if candidate not in used_names:
            used_names.add(candidate)
            return candidate
        index += 1


def create_packet_dir(desktop_root: Path, lane: str, slug: str, packet_date: str) -> Path:
    base_name = f"chatgpt-{normalize_slug(lane)}-{normalize_slug(slug)}-packet-{packet_date}"
    candidate = desktop_root / base_name
    suffix = 2

    while candidate.exists():
        candidate = desktop_root / f"{base_name}-{suffix}"
        suffix += 1

    candidate.mkdir(parents=True, exist_ok=False)
    return candidate


def build_packet(
    *,
    lane: str,
    slug: str,
    prompt_text: str,
    upload_paths: Iterable[str],
    desktop_root: Path,
    packet_date: str,
    max_upload_files: int = DEFAULT_MAX_UPLOAD_FILES,
) -> PacketBuildResult:
    if max_upload_files < 0:
        raise ValueError("max_upload_files must be non-negative")

    desktop_root = desktop_root.expanduser().resolve()
    desktop_root.mkdir(parents=True, exist_ok=True)

    resolved_paths = unique_upload_files(upload_paths)
    included_paths = resolved_paths[:max_upload_files]
    omitted_paths = resolved_paths[max_upload_files:]

    packet_dir = create_packet_dir(desktop_root, lane, slug, packet_date)
    prompt_path = packet_dir / "PROMPT.md"
    prompt_path.write_text(prompt_text, encoding="utf-8")

    used_names = {"PROMPT.md"}
    copied_files: list[CopiedFile] = []

    for source_path in included_paths:
        packet_name = allocate_packet_name(source_path.name, used_names)
        shutil.copy2(source_path, packet_dir / packet_name)
        copied_files.append(
            CopiedFile(
                source_path=str(source_path),
                packet_name=packet_name,
            )
        )

    return PacketBuildResult(
        packet_dir=str(packet_dir),
        prompt_path=str(prompt_path),
        included_files=copied_files,
        omitted_files=[str(path) for path in omitted_paths],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a flat Desktop packet for a ChatGPT order."
    )
    parser.add_argument(
        "--lane",
        required=True,
        choices=("deep-research", "agent", "pro-review"),
        help="ChatGPT lane for the packet name.",
    )
    parser.add_argument("--slug", required=True, help="Short topic slug for the packet name.")
    parser.add_argument(
        "--prompt-file",
        required=True,
        help="Path to the exact prompt text that should become PROMPT.md.",
    )
    parser.add_argument(
        "--desktop-root",
        default="~/Desktop",
        help="Desktop-like parent directory where the packet folder should be created.",
    )
    parser.add_argument(
        "--date",
        dest="packet_date",
        default=date.today().isoformat(),
        help="Date to use in the packet folder name.",
    )
    parser.add_argument(
        "--max-upload-files",
        type=int,
        default=DEFAULT_MAX_UPLOAD_FILES,
        help="Maximum number of upload files to copy into the packet.",
    )
    parser.add_argument("files", nargs="*", help="Ordered local upload files to include.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prompt_path = Path(args.prompt_file).expanduser().resolve()
    prompt_text = prompt_path.read_text(encoding="utf-8")

    result = build_packet(
        lane=args.lane,
        slug=args.slug,
        prompt_text=prompt_text,
        upload_paths=args.files,
        desktop_root=Path(args.desktop_root),
        packet_date=args.packet_date,
        max_upload_files=args.max_upload_files,
    )

    print(json.dumps(asdict(result), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
