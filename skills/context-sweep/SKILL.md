---
name: context-sweep
description: Gather high-signal activity from user-configured sources into a daily note with stable deduplication and per-source checkpoints. Use for a best-effort cross-source context sweep, a dry run, or a bounded sweep since a specific time.
---

# Context Sweep

Gather useful activity from the sources available in the current host, keep only context worth reconstructing later, and write it into a daily note `## Log`.

## Modes

- Normal: gather, classify, write, then advance checkpoints for successful sources.
- `dry-run`: gather and classify without writing or advancing checkpoints.
- `since:<ISO-8601>`: use the supplied lower bound for this run while keeping stored checkpoints forward-only.

Read [checkpoints](nodes/checkpoints.md), [gather](nodes/gather.md), [classify](nodes/classify.md), and [write](nodes/write.md) in that order.

## Portable runtime

- State defaults to `.context-sweep/state.json`.
- Daily notes default to `.context-sweep/journal/YYYY-MM-DD.md`.
- Use `--state-path` and `--journal-file` to follow an existing workspace convention.
- Source names are configuration. The helper accepts stable lowercase source slugs and does not require any particular provider.
