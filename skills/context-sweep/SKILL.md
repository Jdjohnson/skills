---
name: context-sweep
version: 1.0.0
description: |
  Best-effort cross-app context sweep. Gathers sent Superhuman work email,
  sent Slack, best-effort Notion activity, CRM updates, and local Codex usage
  since per-source checkpoints, then writes only high-signal items into a
  daily note `## Log` with stable dedupe markers.
argument-hint: "[dry-run] [since:<ISO-8601>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Bash
  - ToolSearch
  - AskUserQuestion
---

# context-sweep — Cross-App Daily Context Sweep

Sweep the operating surfaces around a working day, keep only the high-signal context, and write it directly into a daily note `## Log`.

This public version is standalone. It does not assume a private assistant workspace, a private daily-note system, or any local workspace layout.

## Invocation

```text
/context-sweep
/context-sweep dry-run
/context-sweep since:2026-04-22T09:00:00-05:00
/context-sweep since:2026-04-22T09:00:00-05:00 dry-run
```

## Mode Routing

| Mode | When | Behavior | Node |
|------|------|----------|------|
| **normal** | Standard sweep request | Gather, classify, write to the configured daily note, then advance successful per-source checkpoints | [[nodes/gather.md]], [[nodes/classify.md]], [[nodes/write.md]], [[nodes/checkpoints.md]] |
| **dry-run** | User says `dry-run` | Gather and classify, but do not write or advance checkpoints | [[nodes/gather.md]], [[nodes/classify.md]], [[nodes/write.md]], [[nodes/checkpoints.md]] |
| **since override** | User says `since:<ISO-8601>` | Use the override as the lower bound for this run's gathering window while keeping checkpoint writes forward-only | [[nodes/checkpoints.md]], [[nodes/gather.md]], [[nodes/classify.md]], [[nodes/write.md]] |

## Working Contract

1. Read `[[nodes/checkpoints.md]]` first so per-source windows are correct.
2. Read `[[nodes/gather.md]]` and gather each source best-effort.
3. Read `[[nodes/classify.md]]` and keep only context worth reconstructing later.
4. Read `[[nodes/write.md]]` and write through the helper so dedupe/order/checkpoints stay deterministic.

## Portable Runtime

- Checkpoints default to `.context-sweep/context-sweep/state.json`.
- Daily-note writes default to `.context-sweep/journal/YYYY-MM-DD.md`.
- Pass `--journal-file <path>` to the helper when the user has a real journal file.
- Pass `--state-path <path>` when the user wants checkpoints somewhere else.
