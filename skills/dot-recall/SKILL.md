---
name: dot-recall
description: |
  Use Jarad's local Dot Recall prototype to search routed Dot files and memory
  sweep proof when MEMORY.md is too thin or prior context needs lookup.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Dot Recall

Use this skill when Jarad asks what was decided, where something landed, what
Dot knows about a topic, or when a prior context lookup is needed and
`MEMORY.md` is not enough.

## Command

Run recall from the workspace root. Use `.` as the workspace unless Jarad
explicitly gives a different Dot workspace path:

Use targeted search when Jarad names a specific topic, client, project, or
decision:

```bash
dot-runtime/recall-lab/recall search --workspace . "<query>"
```

Use gather when Jarad asks for a landscape, a compare/synthesis pass, or
"what changed" across multiple lanes:

```bash
dot-runtime/recall-lab/recall gather --workspace . --since YYYY-MM-DD "<question>"
```

For relative dates, convert the date before running recall. Example: on Friday,
June 26, 2026, "since Monday" means `--since 2026-06-22`.

Inspect promising hits:

```bash
dot-runtime/recall-lab/recall inspect --workspace . <result-id>
```

Check or rebuild the cache when needed:

```bash
dot-runtime/recall-lab/recall status --workspace .
dot-runtime/recall-lab/recall index --workspace .
```

The launcher picks a compatible local Node runtime with built-in `node:sqlite`
support, so agents should use it instead of calling `recall.mjs` directly.

## Rules

1. Read `MEMORY.md` first for current re-entry context.
2. Use recall when the answer depends on older routed context, prior work, or
   memory sweep proof.
3. Use `search` for narrow lookup and `gather` for broad synthesis. If a broad
   answer spans sales/project/timeline lanes, start with `gather`.
4. Prefer canonical hits from `timeline/`, `projects/`, `sales/`, `meetings/`,
   and `resources/`.
5. Treat `dot-runtime/` hits as useful evidence, not settled truth.
6. If a runtime-only result matters long term, route it through Dot's normal
   writeback process before treating it as durable memory.
7. Recall must not query live external apps or mutate external systems.
8. Recall must not auto-promote search results into `MEMORY.md`.
9. For external-agent QA or sanitized smoke tests, prefer a synthetic Dot
   workspace. Broad real-workspace memory-sweep results can mention client or
   project names even though they come from local files.

## Good Triggers

- "What did we decide about Guardian hosting?"
- "Where did we land on the BW walkthrough?"
- "Find the prior context on Shovel memory."
- "What did the memory sweep find?"
- "Do we have anything on Visit Springfield RFP?"
- "What changed since Monday across active sales lanes?"
- "Give me the landscape of current project/sales follow-up."

## Bad Triggers

- Simple current-day questions already answered by `MEMORY.md`.
- Requests that need live app state, unless Jarad explicitly asks for connector
  verification through the appropriate tool.
- Outbound sending, posting, calendar, CRM, or task mutation workflows.
