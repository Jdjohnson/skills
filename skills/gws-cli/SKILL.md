---
name: gws-cli
description: |
  Google Workspace CLI routing guard. Use for Google Docs, Drive, Sheets,
  Slides, and audit-grade Gmail/Calendar verification or export. Day-to-day
  work email and calendar management routes through Superhuman Mail MCP first.
---

# GWS CLI

Use the local Google Workspace CLI path for Google Workspace files and for
deterministic Gmail/Calendar verification, export, or recovery.

This skill takes precedence over connector-first defaults in `dot-work`, `docs`,
and other skills for its trigger surface. When this skill applies, do not route
the same Google Workspace work through native Google connectors or MCP plugins.

## When To Use

- Jarad asks about Google Drive, Google Docs, Google Sheets, Google Slides, or Google Workspace file operations.
- Jarad asks for exact Gmail/Calendar verification, exports, restore-safe cleanup, audit-grade evidence, or fallback after Superhuman is unavailable or ambiguous.
- Another skill needs deterministic Google Workspace data as part of its workflow.

Do not trigger for generic web search just because Google exists as a search engine.

## Routing Rule

Use Superhuman Mail MCP first for day-to-day work email and calendar management.
Use local GWS CLI routes for Google Workspace files and Gmail/Calendar
verification:

- Prefer the thin wrappers in `.dot-skills/gws-cli/scripts/` when they fit the job.
- Use raw `gws` when a wrapper does not cover the needed operation.
- Use the canonical token bundle at `~/.config/gws/token_full.json`.
- If this is fallback after Superhuman timeout/unavailability, keep the action
  read-only unless Jarad separately approved a mutation. Run the local wrapper
  once for the bounded evidence needed; do not retry Superhuman or switch to
  Google/Gmail/Calendar connector tools.

Do not use:

- Google MCP servers
- curated Google plugins
- Drive, Docs, Sheets, Slides, Gmail, or Calendar connector tools

If another skill also applies, keep this routing rule active underneath it. For
email/calendar tasks, Superhuman owns the default route and `gws-cli` is the
verifier or recovery fallback.

## Useful Local Commands

Start with status when auth or scope is uncertain:

```bash
gws auth status
```

Common wrapper families:

```bash
python3 .dot-skills/gws-cli/scripts/google_gmail.py
python3 .dot-skills/gws-cli/scripts/google_calendar.py
python3 .dot-skills/gws-cli/scripts/google_drive.py
python3 .dot-skills/gws-cli/scripts/google_sheets_read.py
```

Use raw `gws` for supported operations that do not have a wrapper:

```bash
gws --help
gws <service> <resource> <action> --help
```

## Verification

Read-only smoke checks: [smoke-tests](nodes/smoke-tests.md)

## Safety

- Do not print tokens, credential files, or auth bundles.
- If CLI auth is broken, diagnose with `gws auth status` before attempting repair.
- If a Google operation would delete, move, overwrite, or share sensitive data, get explicit user approval first unless Jarad already made the target and permissions explicit.
- Mutation-capable wrappers (`draft`, `archive`, `modify-labels`, `create-native`, raw `gws` writes) require explicit user approval before use.
