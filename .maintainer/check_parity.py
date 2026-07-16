#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "brainstorm", "brief", "decision-walkthrough", "plan", "steelman", "stuck",
    "writer", "meeting", "work-log",
    "chatgpt", "claude-code", "codex", "context-sweep", "grok-build",
    "gws-cli", "opencode", "run",
    "economist-council",
)
SKILL_SET = set(SKILLS)
TEXT_SUFFIXES = {".md", ".py", ".js", ".mjs", ".json", ".yaml", ".yml", ".sh", ".txt"}
LEGAL_ATTRIBUTION_PATHS = {
    Path("README.md"), Path("LICENSE"),
    Path("licenses/mostlyserious-run-workflow-MIT.txt"),
    Path(".codex-plugin/plugin.json"), Path(".claude-plugin/plugin.json"),
}
FORBIDDEN_PATTERNS = (
    (re.compile(r"\bDot\b", re.I), "private host name"),
    (re.compile(r"\bjj-[a-z0-9-]+", re.I), "personal skill name"),
    (re.compile(r"\bms-[a-z0-9-]+", re.I), "organization skill name"),
    (re.compile(r"\.dot-skills|\.dot-core|\.dot-addons", re.I), "private route"),
    (re.compile(r"/Users/[A-Za-z0-9._-]+/"), "concrete user path"),
    (re.compile(r"\b(?:Superhuman|MSCRM|PSB Bank|Ochsner|AECI|Associated Electric|visuallyacute)\b", re.I), "personal or client system"),
    (re.compile(r"\bDOT_[A-Z0-9_]+|\bMSCRM_[A-Z0-9_]+"), "internal environment variable"),
)
ATTRIBUTION_PATTERNS = (
    re.compile(r"\bJarad Johnson\b", re.I),
    re.compile(r"\bMostly Serious\b", re.I),
    re.compile(r"mostlyserious", re.I),
)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bxai-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def rel(path: Path) -> Path:
    return path.relative_to(ROOT)


def text_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name == "LICENSE":
            files.append(path)
    return files


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{rel(path)} is not valid JSON: {exc}")


def validate_inventory() -> None:
    actual = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    if actual != SKILL_SET:
        fail(f"skill inventory mismatch; missing={sorted(SKILL_SET - actual)} extra={sorted(actual - SKILL_SET)}")

    parity = {path.stem for path in (ROOT / ".maintainer" / "parity").glob("*.json")}
    if parity != SKILL_SET:
        fail(f"parity inventory mismatch; missing={sorted(SKILL_SET - parity)} extra={sorted(parity - SKILL_SET)}")

    for manifest_name in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
        data = load_json(ROOT / manifest_name)
        if data.get("version") != "2.1.0":
            fail(f"{manifest_name} must declare version 2.1.0")
        if data.get("interface", {}).get("skills") != list(SKILLS):
            fail(f"{manifest_name} skill inventory or order is stale")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    linked = set(re.findall(r"\./skills/([a-z0-9-]+)/SKILL\.md", readme))
    if linked != SKILL_SET:
        fail(f"README skill links mismatch; missing={sorted(SKILL_SET - linked)} extra={sorted(linked - SKILL_SET)}")

    if (ROOT / "downloads" / "cli-skills").exists():
        fail("committed CLI download archives are not part of the public distribution")
    if (ROOT / ".maintainer" / "package_cli_skills.py").exists():
        fail("legacy CLI archive packager is still present")


def validate_skill(skill: str) -> None:
    root = ROOT / "skills" / skill
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail(f"skills/{skill}/SKILL.md is missing YAML frontmatter")

    top_keys = [
        line.split(":", 1)[0]
        for line in match.group(1).splitlines()
        if line and not line[0].isspace() and ":" in line
    ]
    if top_keys != ["name", "description"]:
        fail(f"skills/{skill}/SKILL.md frontmatter keys must be name, description; got {top_keys}")
    name = re.search(r"^name:\s*([^\n]+)", match.group(1), re.M)
    if not name or name.group(1).strip().strip("\"'") != skill:
        fail(f"skills/{skill}/SKILL.md has an incorrect name")

    openai = root / "agents" / "openai.yaml"
    if not openai.exists():
        fail(f"skills/{skill}/agents/openai.yaml is missing")
    metadata = openai.read_text(encoding="utf-8")
    if "$" + skill not in metadata:
        fail(f"skills/{skill}/agents/openai.yaml default prompt must mention $" + skill)

    parity = load_json(ROOT / ".maintainer" / "parity" / f"{skill}.json")
    if parity.get("skill") != skill or not parity.get("cases"):
        fail(f".maintainer/parity/{skill}.json has an invalid contract")


def validate_links() -> None:
    for path in text_files():
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        targets = [match.group(1).split("|", 1)[0] for match in WIKILINK_RE.finditer(text)]
        targets += [match.group(1).split("#", 1)[0] for match in MARKDOWN_LINK_RE.finditer(text)]
        for target in targets:
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            destination = (path.parent / target).resolve()
            try:
                destination.relative_to(ROOT)
            except ValueError:
                fail(f"{rel(path)} links outside the repository: {target}")
            if not destination.exists():
                fail(f"{rel(path)} has a broken local link: {target}")


def validate_scrub() -> None:
    for path in text_files():
        relative = rel(path)
        text = path.read_text(encoding="utf-8", errors="ignore")
        if relative == Path(".maintainer/check_parity.py"):
            continue
        for pattern, label in FORBIDDEN_PATTERNS:
            match = pattern.search(text)
            if match:
                fail(f"{relative} contains {label}: {match.group(0)!r}")
        if relative not in LEGAL_ATTRIBUTION_PATHS:
            for pattern in ATTRIBUTION_PATTERNS:
                match = pattern.search(text)
                if match:
                    fail(f"{relative} contains attribution-only identity text: {match.group(0)!r}")
        email = EMAIL_RE.search(text)
        if email:
            fail(f"{relative} contains an email address: {email.group(0)!r}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"{relative} appears to contain a secret")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.name in {"__pycache__", ".pytest_cache"} or path.suffix in {".pyc", ".pyo"}:
            fail(f"{rel(path)} is generated cache output")
        lowered = path.name.lower()
        if lowered.startswith(("jj-", "ms-")) or lowered == "dot-recall":
            fail(f"{rel(path)} has a stale private name")


def main() -> None:
    validate_inventory()
    for skill in SKILLS:
        validate_skill(skill)
    validate_links()
    validate_scrub()
    print("Maintainer checks passed: 18 generic skills, metadata, parity, links, scrub, and distribution.")


if __name__ == "__main__":
    main()
