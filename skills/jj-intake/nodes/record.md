---
description: |
  Receipt and archive rules for jj-intake handled and deferred items.
---

## Run Receipt

Write a live receipt at:

```text
DOT_COMMS_HOME/runtime/jj-intake/runs/YYYY/MM/YYYY-MM-DD-HHMM-jj-intake/receipt.md
```

For each handled item, record:

- source metadata
- original local source path
- Title
- Link
- Overview
- Relevance
- Suggestion
- Jarad response or pre-authorized quiet filing reason
- outcome
- action taken
- destination link or file path
- pending approval, if any
- archived source path

Use a compact table when possible. Add short notes below the table only when an
item needs more context.

Quiet-filed items must include the day-log destination and the reason Dot did
not bring the item forward for Jarad review.

## Source File Lifecycle

Never delete local inbox source files.

Handled items move to:

```text
DOT_COMMS_HOME/runtime/jj-intake/handled/YYYY/MM/
```

Deferred items move to:

```text
DOT_COMMS_HOME/runtime/jj-intake/deferred/YYYY/MM/
```

Preserve the original file name. If a file name collision exists, prefix the
new path with the run timestamp.

For deferred items, add a short note to the receipt with the reason and review
date. Do not leave the deferred item in active `inbox/`.

## Closeout

End with a short receipt in chat:

- `Handled`
- `Done now`
- `Filed`
- `Pending approval`
- `Deferred`
- `Remaining`

If freshness was reduced because refresh failed, say so in one line.
