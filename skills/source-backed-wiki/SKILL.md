---
name: source-backed-wiki
description: Build, query, connect, and lint a local Markdown wiki whose claims trace to allowlisted source files. Use for reusable cross-source understanding, not for replacing canonical records or locating a single current status fact.
---

# Source-Backed Wiki

Compile reusable understanding into a linked Markdown wiki while keeping source records authoritative.

## Modes

| Mode | Purpose | Read |
|---|---|---|
| `ingest` | Create or update pages from source material | [ingest](nodes/ingest.md) |
| `query` | Answer a cross-source question | [query](nodes/query.md) |
| `connect` | Add a supported relationship between pages | [connect](nodes/connect.md) |
| `lint` | Check structural and semantic health | [lint](nodes/lint.md) |

## Workspace contract

The workspace provides `wiki/schema.md`, `wiki/sources.md`, `wiki/index.md`, `wiki/log.md`, and `wiki/pages/`. Read schema, source policy, and index before a write. Resolve `<skill-root>` to this skill's installed folder. The guard treats `sources/` as canonical; configure additional roots with the comma-separated `SOURCE_BACKED_WIKI_ROOTS` variable.

Read [page contract](references/page-contract.md) when creating or changing pages and [source policy](references/source-policy.md) for external roots.

## Invariants

- Sources are read-only and opened only through `<skill-root>/scripts/wiki-guard.mjs resolve`.
- Wiki pages are derived; when a page and source disagree, the source controls.
- Never ingest wiki prose as evidence for another page. Cite the underlying source.
- Update before creating. Preserve contradictions as dated tensions and mark supersession without rewriting history.
- Never edit a `## Human notes` span through this skill.
- Page-changing operations create or update only. Rename, merge, and deletion require a separately designed migration.
- A write touches only declared pages, `index.md`, and `log.md`, then passes guarded source re-resolution, audit, exact-path staging, and one commit.
- Read-only query and lint do not commit or touch index/log.

Use the workspace's configured search/index adapter when the wiki index is insufficient. Cache output is evidence, not canonical truth, and a failed adapter is an unknown rather than an empty result.

## Authority

Write only when the request clearly asks to ingest, connect, save a query, or fix approved lint findings. Never write because another workflow happened to surface useful information. Report rejected sources, unresolved contradictions, dirty repositories, and failed verification without bypassing a guard.
