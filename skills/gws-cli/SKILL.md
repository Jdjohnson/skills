---
name: gws-cli
description: Run guarded Google Workspace command-line operations through local helper scripts. Use for bounded Drive, Sheets, Gmail, or Calendar reads; for approved mutations; or when exact JSON evidence and restore-safe handling matter.
---

# Google Workspace CLI

Use the narrowest bundled helper that fits the request. Prefer read-only inspection. Mutations require an explicit target and clear user approval.

## Helpers

Resolve `<skill-root>` to this skill's installed directory.

- Gmail: `python3 <skill-root>/scripts/google_gmail.py --help`
- Calendar: `python3 <skill-root>/scripts/google_calendar.py --help`
- Drive: `python3 <skill-root>/scripts/google_drive.py --help`
- Sheets: `python3 <skill-root>/scripts/google_sheets_read.py --help`
- Export an authenticated CLI token bundle: `python3 <skill-root>/scripts/google_token_export.py --help`
- Create a token bundle from Application Default Credentials: `python3 <skill-root>/scripts/google_token_from_adc.py --help`

Read [smoke tests](nodes/smoke-tests.md) when validating a new setup.

## Node Map

| Node | Purpose |
|------|---------|
| [smoke tests](nodes/smoke-tests.md) | Check local helper wiring without contacting Google. |

## Routing

1. Identify the Workspace product, account, resource, and intended read or mutation.
2. Run `--help` before using an unfamiliar subcommand.
3. Use the smallest result window and fields that answer the request.
4. For a mutation, preview or re-read the exact target and confirm approval.
5. Capture resource IDs, URLs, counts, and returned state without exposing token contents.
6. Verify the post-mutation state from the service.

## Authentication

The helpers use the installed Google CLI and a local token bundle, normally `~/.config/gws/token_full.json`. Treat credential files as secrets: never print, copy into a repository, or include their values in receipts. If authentication is absent or invalid, report the interactive setup step instead of asking for pasted credentials.

## Safety

- Do not delete, move, overwrite, share, send, or change permissions without explicit approval.
- Prefer reversible operations and preserve stable IDs for recovery.
- Never infer an account or resource when more than one is available.
- Keep live-service tests separate from local regression tests.
- A local command receipt is not proof of a remote mutation unless the returned service state confirms it.
