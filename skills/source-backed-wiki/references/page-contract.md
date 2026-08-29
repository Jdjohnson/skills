# Page Contract

The guard enforces this format.

## Page

Every page starts with exactly:

```yaml
---
kind: concept
aliases: ["alternate title"]
tags: ["topic"]
updated: 2026-08-29
---
```

`kind` is `concept`, `entity`, or `synthesis`; arrays are inline JSON-compatible strings; `updated` is a real `YYYY-MM-DD` date. Exactly one H1 follows the frontmatter and matches the filename stem.

Titles and aliases are unique after Unicode NFKC normalization and lowercasing. They are nonempty single lines and exclude control characters, path separators, wiki-link delimiters, fragments, and platform-invalid filename characters.

Use populated sections in this order:

```text
# Title
## Current understanding
## Evidence and examples
## Tensions and changes
## Related
## Sources
## Human notes
```

`## Human notes` is optional and protected byte-for-byte. More than one is invalid.

## References and links

A workspace source is a normalized relative POSIX path beneath a configured source root. An external source is `<alias>: <root-relative-path>`. References reject line breaks, nulls, backslashes, `|`, brackets, fragments, and ` sha256=`.

`## Sources` contains one source per list item. Workspace sources use explicit extensions:

```markdown
- [[sources/example/current.md|Example current record]]
- archive: 2024/notes/example.md
```

Wiki links are `[[Title]]` or `[[Title|Label]]` and must resolve uniquely by H1 or alias. Fragments are unsupported.

## Index

`index.md` starts with `# Wiki Index` and the sections `## Concepts`, `## Entities`, and `## Syntheses`. Each page appears once under its kind:

```markdown
- [[Title]] | kind=concept | updated=2026-08-29 | Single-line description.
```

## Log

`log.md` starts with:

```markdown
# Wiki Log

Entries are append-only.
```

Each write appends one `ingest`, `connect`, `query-save`, or `lint-fix` entry:

```markdown
## [2026-08-29T14:03:00Z] ingest | sources/example/current.md

- sources:
  - sources/example/current.md sha256=<64 lowercase hex>
- pages-created: [[Title]]
- pages-updated: none
- contradictions: none
- batch-review: reviewed
```

Use `- sources: none` only for a source-free operation. The log source set must exactly match final guarded resolution.

## Content rules

- One independently reusable subject per page.
- Every claim traces to `## Sources`; summarize rather than copy at length.
- Update existing pages before creating near-duplicates.
- Preserve superseded evidence and dated tensions.
- Never cite wiki prose as source evidence.
- Create and update only; migrations own rename, merge, and deletion.

Workspace schema may customize titles, tags, aliases, descriptions, and page-creation preferences. It cannot weaken source containment, truth status, reference grammar, protected notes, or transaction guards.
