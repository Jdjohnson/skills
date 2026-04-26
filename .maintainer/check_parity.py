#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARITY_DIR = ROOT / ".maintainer" / "parity"
SKILLS = ("style-guide", "writer", "brief")
FORBIDDEN = ("Dot", "Jarad", ".dot/", "/Users/", "Assistant", "jj-")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} is invalid JSON: {exc}")


def validate_parity_file(skill: str) -> None:
    path = PARITY_DIR / f"{skill}.json"
    if not path.exists():
        fail(f"missing parity file for {skill}")

    data = load_json(path)
    if data.get("skill") != skill:
        fail(f"{path.relative_to(ROOT)} has wrong skill name")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        fail(f"{path.relative_to(ROOT)} must contain non-empty cases")

    skill_root = ROOT / "skills" / skill
    if not (skill_root / "SKILL.md").exists():
        fail(f"missing skills/{skill}/SKILL.md")

    for case in cases:
        for key in ("id", "prompt", "expected_nodes", "expected_output_shape"):
            if key not in case:
                fail(f"{path.relative_to(ROOT)} case missing {key}")
        if not isinstance(case["expected_nodes"], list) or not case["expected_nodes"]:
            fail(f"{path.relative_to(ROOT)} case {case['id']} must list expected nodes")
        if not isinstance(case["expected_output_shape"], list) or not case["expected_output_shape"]:
            fail(f"{path.relative_to(ROOT)} case {case['id']} must list expected output shape")
        for node in case["expected_nodes"]:
            node_path = skill_root / node
            if not node_path.exists():
                fail(f"{path.relative_to(ROOT)} references missing node {node}")


def validate_wikilinks(skill: str) -> None:
    skill_root = ROOT / "skills" / skill
    for md in skill_root.rglob("*.md"):
        text = md.read_text()
        for match in WIKILINK_RE.finditer(text):
            target = match.group(1).split("|", 1)[0]
            if target.startswith("#"):
                continue
            target_path = (md.parent / target).resolve()
            try:
                target_path.relative_to(ROOT)
            except ValueError:
                fail(f"{md.relative_to(ROOT)} links outside repo: {target}")
            if not target_path.exists():
                fail(f"{md.relative_to(ROOT)} has broken wikilink: {target}")


def validate_no_local_leakage(skill: str) -> None:
    skill_root = ROOT / "skills" / skill
    for path in skill_root.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(errors="ignore")
        for token in FORBIDDEN:
            if token in text:
                fail(f"{path.relative_to(ROOT)} contains forbidden local token: {token}")


def validate_output_contracts(skill: str) -> None:
    skill_root = ROOT / "skills" / skill
    text = (skill_root / "SKILL.md").read_text()
    if "[[" not in text:
        fail(f"skills/{skill}/SKILL.md does not route to nodes")
    if skill == "brief":
        for header in ("Bottom Line", "Key Judgments", "What To Decide", "Gaps"):
            if header not in text and header not in (skill_root / "nodes" / "brief-format.md").read_text():
                fail(f"brief output contract missing {header}")
    if skill == "style-guide":
        for mode in ("calibrate", "check", "rewrite", "redflags", "checklist"):
            if mode not in text:
                fail(f"style-guide missing mode {mode}")
    if skill == "writer":
        for phase in ("phase-01-intake", "phase-06-draft", "phase-07-refine"):
            if phase not in text:
                fail(f"writer missing phase route {phase}")


def main() -> None:
    for skill in SKILLS:
        validate_parity_file(skill)
        validate_wikilinks(skill)
        validate_no_local_leakage(skill)
        validate_output_contracts(skill)
    print("Maintainer parity checks passed.")


if __name__ == "__main__":
    main()
