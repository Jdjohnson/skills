---
name: work-log
description: Explicitly close out the active work thread into configured local records. Use only when the user asks to log, close out, or record the current thread; capture outcomes, decisions, deadlines, dependencies, blockers, and next actions without broadening into unrelated systems.
---

# Work Log

Record a concise, source-backed closeout for the active thread. This skill is explicit-only and must never run automatically because work appears finished.

## Invocation gate

- Run only after an unambiguous request such as `$work-log`, `log this work`, or `close out this thread`.
- If the request could mean something else, ask before writing.
- Invocation authorizes only the configured log targets. It does not authorize sending, publishing, task discovery, or external mutations.

## Resolve targets

Use write destinations in this order:

1. A file or record explicitly named in the current request.
2. A work-log route defined by workspace instructions.
3. An existing current-day log clearly identified by the workspace.
4. If no destination is configured, propose `.work-log/YYYY-MM-DD.md` and ask before creating it.

Do not search external task systems for a target. Use an external record only when the user names its exact URL or stable ID and explicitly approves the update.

## Review the thread

Extract only durable, useful facts:

- Outcomes and shipped artifacts.
- Decisions made or confirmed.
- Exact deadlines, date changes, dependencies, or owners.
- Open follow-ups and the next concrete action.
- Blockers, skipped work, approvals still needed, or systems intentionally untouched.
- The exact state boundary: drafted, prepared, staged, committed, pushed, merged, sent, published, deployed, blocked, or verified.

Do not invent commitments, owners, dates, identifiers, or completed states.

## Write rules

- Prefer one short status entry over a narrative recap.
- Update an existing matching item rather than adding a duplicate.
- Preserve surrounding structure and human-authored source material.
- Include links or paths only when they make re-entry easier.
- If a stable thread identifier is available, use it as a deduplication marker; otherwise deduplicate by normalized outcome plus date.
- Do not broaden the closeout to adjacent threads or stale work merely because it is visible.

## External boundary

A work-log request alone does not authorize comments, status changes, due-date changes, task creation, email, chat, calendar, or publishing. If the user separately approves a mutation to an exact external record, perform only that mutation and report its result precisely.

## Receipt

Report the path or record written, any configured target skipped with a reason, and remaining follow-ups or blockers. Keep the receipt short.
