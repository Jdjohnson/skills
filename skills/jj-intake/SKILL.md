---
name: jj-intake
description: |
  Jarad-specific intake triage for Dot's external comms queue from SMS/email.
  Reads DOT_COMMS_HOME/inbox/ as the source of truth, refreshes safely,
  quietly files obvious low-priority items, then reviews remaining items with
  the five-field intake format.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - ToolSearch
  - AskUserQuestion
---

# JJ Intake

Triage the Dot comms inbound queue without mixing it into `jj-journal` or
general email cleanup.

Legacy triggers: `jj-inbox` and `inbox-intake` route here. The current command
is `$jj-intake`.

## Mode Routing

V1 has one default mode only.

| Mode | Use When | Behavior | Node |
|------|----------|----------|------|
| default | Jarad says `$jj-intake`, asks to triage Dot inbox/intake, or asks what came in through Dot text/email | Safe refresh, quiet day-log filing for distractions, five-field review for remaining items, local action or filing, receipt | [[nodes/workflow.md]], [[nodes/queue.md]], [[nodes/item.md]], [[nodes/record.md]] |

## Core Rules

1. Load `[[nodes/workflow.md]]` first, then use the other nodes as needed.
2. Treat `DOT_COMMS_HOME/inbox/*.md` files as the active source of truth after
   refresh. Default `DOT_COMMS_HOME` is `/Users/jaradjohnson/Developer/projects/dot-comms`.
3. Refresh may copy/sync inbound comms into that external inbox; it must not
   clean up real email/SMS inboxes or send anything.
4. Review all active items first. Quietly file obvious distractions or items
   with no clear project/priority tie to the current day log.
5. Bring remaining items to Jarad using only the five-field format from
   `[[nodes/item.md]]`: Title, Link, Overview, Relevance, Suggestion.
6. Process reviewed items one at a time until the active queue is empty or
   Jarad stops.
7. Local work and drafts are allowed; outbound sends, publishing, or external
   mutations require explicit approval.
8. Move handled/deferred local source files into
   `DOT_COMMS_HOME/runtime/jj-intake/`.
   Do not delete source files.
9. End with a short receipt.

## Shared Dependencies

- Local safety and output rules: [[nodes/local-guardrails.md]]
