# Lint

Lint is read-only unless the user explicitly asks to fix approved findings.

Check:

- invalid frontmatter, page shape, titles, filenames, aliases, or dates;
- broken, ambiguous, fragmented, or circular links;
- duplicate identities after normalized comparison;
- missing or mismatched index entries and required sources;
- excluded, unresolved, or recursive wiki sources;
- multiple protected human-notes sections;
- orphan, duplicate, overbroad, unsupported, stale, or contradictory pages;
- claims no longer supported by cited source material.

Run `wiki-guard audit --workspace <workspace> --json` and report every finding before any write. Recommend merges, renames, or deletions but do not perform them.

Only an explicit fix request runs the approved subset as one `lint-fix` transaction through [ingest](ingest.md).
