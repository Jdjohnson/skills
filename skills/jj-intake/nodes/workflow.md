---
description: |
  Default jj-intake run lifecycle: refresh, classify, quiet-file distractions,
  review remaining items in the five-field format, record, archive, and close
  with a short receipt.
---

## Default Workflow

Use this for every `$jj-intake` run.

1. Create a run folder:
   - `DOT_COMMS_HOME/runtime/jj-intake/runs/YYYY/MM/YYYY-MM-DD-HHMM-jj-intake/`
   - create `receipt.md` immediately and keep it current.
2. Read [[queue.md]] and refresh the local queue.
3. Read `DOT_COMMS_HOME/inbox/*.md` using
   `DOT_COMMS_HOME/integrations/comms-mcp/intake-queue.mjs` metadata
   conventions when possible. If parsing fails, keep going and flag the file.
4. Classify all active items before showing Jarad the review queue.
   - Obvious distractions or items with no clear project/priority tie are
     quietly filed.
   - Quiet-filed items are not shown to Jarad during the review unless he asks.
   - Quiet-filed items still get proof in the day log and run receipt.
5. For quiet-filed items:
   - write or append a concise log at
     `DOT_TARGET_WORKSPACE/timeline/.../YYYY-MM-DD-day/dot/intake-quiet-log-YYYY-MM-DD.md`;
   - follow `/Users/jaradjohnson/Dot/ROUTES.md` for the current day folder,
     creating the day folder and `dot/`/`source/` folders if missing;
   - read [[record.md]], update the receipt, and move the source file to the
     handled archive.
6. Sort the remaining review queue: owner/pinned first, then known senders,
   then unknown/noise; oldest first inside each group.
7. Show remaining items using [[queue.md]] and [[item.md]]. The only
   user-facing review fields are `Title`, `Link`, `Overview`, `Relevance`, and
   `Suggestion`.
8. After each item reaches a terminal route, read [[record.md]], update the
   receipt, and move the local source file to handled or deferred archive.
9. Continue until the queue is empty or Jarad says to stop after the current item.
10. Close with a short receipt:
   - handled count
   - done-now items
   - filed destinations
   - pending approvals
   - deferred items
   - remaining queue count

## Boundaries

- `jj-intake` owns Dot comms intake triage only.
- `jj-email` owns general Superhuman/Gmail email management.
- `ms-dot-work` owns delegated work once an intake item becomes a real work
  packet.
- When Jarad chooses `implement`, hand the item to `ms-dot-work` capture/run;
  do not execute the bounded delegated work inside `jj-intake`.
- The five-field intake approval only approves the handoff. It does not replace
  the full Dot Work task-card approval gate in `ms-dot-work`.
- `jj-journal` must not read or triage inbox items.
- Durable outputs from a routed item belong in the canonical New Dot home named
  by `/Users/jaradjohnson/Dot/ROUTES.md`; the external comms runtime keeps only
  inbox source files, archives, and receipts.
- The legacy expanded item readback is retired. Do not add extra context
  sections, route menus, or separate rationale sections to review items.
