#!/usr/bin/env python3
"""Read-only, bounded inventory of closeout-related text matches."""

from __future__ import annotations

import argparse
from fnmatch import fnmatchcase
import json
from pathlib import Path
import re
import sys


TEXT_SUFFIXES = {".csv", ".json", ".md", ".txt", ".yaml", ".yml"}
SKIP_DIRS = {".git", ".stversions", ".cache", "node_modules", "runtime"}
MAX_FILE_BYTES = 2_000_000


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def parse_class_rule(value: str) -> tuple[str, str]:
    surface_class, separator, pattern = value.partition("=")
    if not separator or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", surface_class):
        raise argparse.ArgumentTypeError("class rules must use CLASS=GLOB with a lowercase kebab-case class")
    if not pattern or Path(pattern).is_absolute():
        raise argparse.ArgumentTypeError("class-rule globs must be non-empty and relative")
    return surface_class, pattern


def classify(relative: Path, rules: list[tuple[str, str]]) -> str:
    relative_path = relative.as_posix()
    for surface_class, pattern in rules:
        if fnmatchcase(relative_path, pattern):
            return surface_class
    return "other"


def iter_files(root: Path):
    if root.is_file():
        yield root
        return

    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
        except OSError:
            continue
        yield path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find exact closeout terms within explicit subject roots without writing files."
    )
    parser.add_argument("--workspace", required=True, help="Workspace root")
    parser.add_argument(
        "--root",
        action="append",
        required=True,
        help="Explicit file or directory to inspect, relative to workspace or absolute",
    )
    parser.add_argument(
        "--term",
        action="append",
        required=True,
        help="Literal case-insensitive term to find; repeat for multiple terms",
    )
    parser.add_argument(
        "--class-rule",
        action="append",
        type=parse_class_rule,
        default=[],
        metavar="CLASS=GLOB",
        help="Classify relative paths with an ordered glob rule; first match wins",
    )
    parser.add_argument(
        "--allow-workspace-root",
        action="store_true",
        help="Permit a deliberate full-workspace root; omitted by default as a safety gate",
    )
    parser.add_argument("--max-results", type=int, default=1000)
    return parser.parse_args()


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(2)


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.is_dir():
        fail(f"workspace is not a directory: {workspace}")
    if args.max_results < 1:
        fail("--max-results must be at least 1")

    roots: list[Path] = []
    for raw_root in args.root:
        candidate = Path(raw_root).expanduser()
        if not candidate.is_absolute():
            candidate = workspace / candidate
        candidate = candidate.resolve()
        if not inside(candidate, workspace):
            fail(f"root is outside workspace: {candidate}")
        if candidate == workspace and not args.allow_workspace_root:
            fail("workspace-root scans require --allow-workspace-root")
        if not candidate.exists():
            fail(f"root does not exist: {candidate}")
        roots.append(candidate)

    terms = [term for term in args.term if term]
    if not terms:
        fail("at least one non-empty --term is required")
    lowered_terms = [(term, term.casefold()) for term in terms]

    seen_files: set[Path] = set()
    matches: list[dict[str, object]] = []
    scanned_files = 0
    truncated = False

    for root in roots:
        for path in iter_files(root):
            resolved = path.resolve()
            if resolved in seen_files:
                continue
            seen_files.add(resolved)
            scanned_files += 1
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            relative = path.relative_to(workspace)
            surface_class = classify(relative, args.class_rule)
            for line_number, line in enumerate(text.splitlines(), start=1):
                lowered_line = line.casefold()
                for original, lowered in lowered_terms:
                    if lowered not in lowered_line:
                        continue
                    matches.append(
                        {
                            "path": relative.as_posix(),
                            "line": line_number,
                            "term": original,
                            "class": surface_class,
                            "text": line.strip(),
                        }
                    )
                    if len(matches) >= args.max_results:
                        truncated = True
                        break
                if truncated:
                    break
            if truncated:
                break
        if truncated:
            break

    result = {
        "schema_version": 1,
        "workspace": str(workspace),
        "roots": [str(root.relative_to(workspace)) if root != workspace else "." for root in roots],
        "terms": terms,
        "class_rules": [
            {"class": surface_class, "glob": pattern}
            for surface_class, pattern in args.class_rule
        ],
        "scanned_files": scanned_files,
        "truncated": truncated,
        "matches": matches,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
