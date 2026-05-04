---
description: |
  Gather rules and source-specific collection patterns for jj-context-sweep.
  Load after checkpoints are understood.
---

# Gather

The sweep is best-effort across five sources:

- Superhuman sent work mail
- Slack sent messages
- Notion activity
- CRM updates
- Local Codex sessions on this machine

Build a normalized payload with:

- `sources`: source status metadata keyed by source name
- `items`: kept items only, each with `source`, `source_id`, `timestamp`, and `summary`
- optional `end_timestamp` for ranged items such as Codex sessions

## Superhuman

Use Superhuman Mail MCP for sent work email. Do not use GWS for default sent
email sweeps.

Rules:

- Fetch broadly enough to survive same-day reruns and timezone edge cases.
- Exact-filter by parsed message timestamp after the effective lower bound.
- Normalize with `id` or `message_id`, `thread_id`, timestamp, `to`, `subject`, and `snippet` or private-safe summary.
- Use sent-message timestamps, not the sweep time.
- Use `source: "superhuman"` in the normalized payload.
- Use GWS only if the current task explicitly needs verification/export fallback.

## Slack

Resolve the current user's Slack user id once, then search sent messages across:

- public channels
- private channels
- DMs

Rules:

- Filter to current-user-authored messages only.
- Use exact `ts` filtering after the effective lower bound when the connector surface allows it.
- If search requires a broader read window, do a broad search first and exact-filter by `ts` yourself.
- Keep the source-native `ts` as the stable id.

## Notion

V1 is best-effort only. Do not pretend it is a full-workspace edit feed.

Use:

- current-user meeting notes with `last_edited_*` filters where available
- current-user page search for newly created pages after the lower bound

Rules:

- Prefer `last_edited_time` for edited items and `created_time` for new pages.
- Say explicitly when the connector cannot provide true "all edits since X" coverage.
- Keep the page id as the stable source id.

## CRM

Use the CRM connector or database access available in the current host.

Rules:

- If the current session exposes database query tools, prefer structured queries over manual copy/paste.
- Filter to the current user's owned or relevant records when ownership data exists.
- Prefer source ids that reflect the concrete CRM update record. Use audit-log ids when available; otherwise use the most specific live record id available from the query.
- If CRM access is unavailable, mark CRM as `skipped`, explain the unavailable connector or credential, and leave the CRM checkpoint untouched.

## Codex

Use the deterministic local parser:

```bash
python3 skills/jj-context-sweep/scripts/jj_context_sweep.py codex --since "<ISO-8601>"
```

Rules:

- Scope is all local Codex sessions on this machine, not just the current thread or current repository.
- Use `session_meta.cwd` plus user-message timing to summarize qualifying sessions.
- Preserve start and end times when a session spans multiple user turns.
- Use the Codex thread id or rollout id as the stable id.
