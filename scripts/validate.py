#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.S)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TEXT_SUFFIXES = {".md", ".py", ".rb", ".js", ".mjs", ".json", ".yaml", ".yml", ".sh", ".txt"}
SECRET_PATTERNS = (
    re.compile(r"\b(?:sk|xai)-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{30,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)
PRIVATE_NAMESPACE_FRAGMENTS = (".dot" + "-skills/",)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {error}")


def frontmatter_value(body: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", body, re.M)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def validate_catalog() -> tuple[list[dict[str, str]], set[str]]:
    catalog = load_json(ROOT / "catalog.json")
    if not isinstance(catalog, dict) or catalog.get("repository") != "Jdjohnson/skills":
        fail("catalog.json has an invalid repository")

    items = catalog.get("skills")
    if not isinstance(items, list) or not items:
        fail("catalog.json must contain skills")

    slugs: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            fail("catalog.json contains a non-object skill")
        slug = item.get("slug")
        if not isinstance(slug, str) or not NAME_RE.fullmatch(slug):
            fail(f"invalid catalog slug: {slug!r}")
        if not all(isinstance(item.get(key), str) and item[key].strip() for key in ("title", "category", "summary")):
            fail(f"catalog entry {slug} lacks title, category, or summary")
        slugs.append(slug)

    if len(slugs) != len(set(slugs)):
        fail("catalog.json contains duplicate slugs")

    actual = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
    expected = set(slugs)
    if actual != expected:
        fail(f"skill inventory mismatch; missing={sorted(expected - actual)} extra={sorted(actual - expected)}")
    grouping = load_json(ROOT / "skills.sh.json")
    groups = grouping.get("groupings") if isinstance(grouping, dict) else None
    if not isinstance(groups, list) or not groups:
        fail("skills.sh.json has no groupings")
    grouped = [slug for group in groups if isinstance(group, dict) for slug in group.get("skills", [])]
    if grouped != slugs:
        fail("skills.sh.json order does not match catalog.json")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    linked = set(re.findall(r"\./skills/([a-z0-9-]+)/SKILL\.md", readme))
    if linked != expected:
        fail(f"README skill links mismatch; missing={sorted(expected - linked)} extra={sorted(linked - expected)}")

    return items, expected


def validate_skill(slug: str) -> None:
    root = SKILLS_ROOT / slug
    entry = root / "SKILL.md"
    if not entry.is_file():
        fail(f"skills/{slug}/SKILL.md is missing")

    text = entry.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        fail(f"skills/{slug}/SKILL.md has invalid frontmatter")
    name = frontmatter_value(match.group("body"), "name")
    description = frontmatter_value(match.group("body"), "description")
    if name != slug:
        fail(f"skills/{slug}/SKILL.md declares name {name!r}")
    if not description or "TODO" in description or "TBD" in description:
        fail(f"skills/{slug}/SKILL.md has an unfinished description")

    metadata = root / "agents" / "openai.yaml"
    if not metadata.is_file():
        fail(f"skills/{slug}/agents/openai.yaml is missing")
    if f"${slug}" not in metadata.read_text(encoding="utf-8"):
        fail(f"skills/{slug}/agents/openai.yaml does not mention ${slug}")


def validate_links() -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            if raw_target.startswith("<") and raw_target.endswith(">") and "://" not in raw_target:
                continue
            target = raw_target.strip().split()[0].strip("<>")
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            destination = (path.parent / target).resolve()
            try:
                destination.relative_to(ROOT)
            except ValueError:
                fail(f"{path.relative_to(ROOT)} links outside the repository: {raw_target}")
            if not destination.exists():
                fail(f"{path.relative_to(ROOT)} has a broken link: {raw_target}")


def validate_hygiene() -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.name in {".DS_Store", "__pycache__", ".pytest_cache"} or path.suffix in {".pyc", ".pyo"}:
            fail(f"generated file committed: {path.relative_to(ROOT)}")
        if path.is_dir() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"/Users/[A-Za-z0-9._-]+/", text):
            fail(f"personal absolute path in {path.relative_to(ROOT)}")
        if any(fragment in text for fragment in PRIVATE_NAMESPACE_FRAGMENTS):
            fail(f"private source namespace in {path.relative_to(ROOT)}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible secret in {path.relative_to(ROOT)}")

def validate_media() -> None:
    visual_attribution = SKILLS_ROOT / "visual-direction" / "ATTRIBUTION.md"
    photo_attribution = SKILLS_ROOT / "photography-director" / "ATTRIBUTION.md"
    if not visual_attribution.is_file() or not photo_attribution.is_file():
        fail("visual skills must include attribution files")

    photo_root = SKILLS_ROOT / "photography-director"
    ledger = load_json(photo_root / "references" / "source-ledger.json")
    subject_catalog = load_json(photo_root / "references" / "catalog" / "subject-sets.json")
    primary = ledger.get("references") if isinstance(ledger, dict) else None
    support = subject_catalog.get("references") if isinstance(subject_catalog, dict) else None
    defaults = subject_catalog.get("sourceDefaults") if isinstance(subject_catalog, dict) else None
    if not isinstance(primary, list) or not isinstance(support, list) or not isinstance(defaults, dict):
        fail("Photography Director reference catalogs are invalid")

    references = [*primary, *({**defaults, **reference} for reference in support)]
    ids = [reference.get("id") for reference in references]
    if len(ids) != len(set(ids)):
        fail("Photography Director reference IDs are not unique")

    attribution = photo_attribution.read_text(encoding="utf-8")
    tracked_images: set[str] = set()
    for reference in references:
        reference_id = reference.get("id")
        if f"| {reference_id} |" not in attribution:
            fail(f"Photography Director attribution omits {reference_id}")

        is_pexels = "pexels.com" in str(reference.get("sourcePage", ""))
        if is_pexels and (
            reference.get("license") != "Pexels License"
            or reference.get("displayMode") != "authorized-remote"
        ):
            fail(f"Pexels reference {reference_id} must use the Pexels License and remain remote-only")

        local_path = reference.get("localPath")
        if reference.get("displayMode") == "authorized-remote":
            if local_path:
                fail(f"Remote reference {reference_id} retains a local path")
            continue
        if not isinstance(local_path, str):
            fail(f"Bundled reference {reference_id} lacks a local path")
        tracked_images.add(local_path)

    actual_images = {
        str(path.relative_to(photo_root))
        for path in (photo_root / "assets" / "references").iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg"}
    }
    if actual_images != tracked_images:
        fail(
            "Photography Director media inventory mismatch; "
            f"missing={sorted(tracked_images - actual_images)} "
            f"extra={sorted(actual_images - tracked_images)}"
        )


def main() -> None:
    items, slugs = validate_catalog()
    for slug in slugs:
        validate_skill(slug)
    validate_links()
    validate_hygiene()
    validate_media()
    print(f"Validated {len(items)} installable skills.")


if __name__ == "__main__":
    main()
