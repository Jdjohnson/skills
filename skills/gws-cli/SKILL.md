---
name: gws-cli
description: Use guarded local wrappers around the Google Workspace CLI for deterministic Drive, Sheets, Gmail, and Calendar reads or authorized mutations. Best for exact verification, export, recovery, or workflows that need machine-readable evidence.
---

# GWS CLI

Use the bundled wrappers when deterministic Google Workspace access is more useful than an interactive connector. Follow the active workspace's preferred app-routing policy; this skill does not override it.

## Use

Read [commands](nodes/commands.md) when selecting a wrapper. Start with a read-only profile or status call when account, scopes, or authentication are uncertain. Search metadata first and fetch full bodies only for likely candidates.

The wrappers:

- load an authorized-user token bundle from `GWS_TOKEN_PATH`, falling back to the user's standard GWS config path;
- require the credential file to be owned by the current user and unreadable by group or others;
- cache and refresh access tokens without printing them;
- retry bounded transient failures for reads and explicitly idempotent writes only;
- never retry a non-idempotent mutation after an ambiguous response.

Use raw `gws` only when no wrapper covers the operation and the current authentication environment supports it.

## Safety

- Never print token files, access tokens, client secrets, cookies, or auth bundles.
- Diagnose authentication before attempting repair. Follow the wrapper's recovery instructions without weakening file permissions.
- Drafting, sending, discarding, archiving, label changes, file creation, sharing, moving, overwriting, and deletion require authority for the exact action and target.
- For a reply draft, preserve the provider's thread ID plus RFC `In-Reply-To` and `References` headers.
- Treat a command receipt as operation evidence. Read back mutations when the API supports it, and report ambiguous responses as unresolved.

For package validation and safe smoke checks, read [smoke tests](nodes/smoke-tests.md).
