---
description: |
  Deterministic daily-note write path for context-sweep. Load after gather
  and classify.
---

# Write

Use the helper script for all daily-note writes and checkpoint updates:

```bash
python3 skills/context-sweep/scripts/context_sweep.py write --root . --payload-file <path>
```

To write into a specific journal file:

```bash
python3 skills/context-sweep/scripts/context_sweep.py write --root . --journal-file <path> --payload-file <path>
```

For dry-run:

```bash
python3 skills/context-sweep/scripts/context_sweep.py write --root . --payload-file <path> --dry-run
```

## Payload Contract

Write a temporary JSON payload with this shape:

```json
{
  "sources": {
    "superhuman": {
      "status": "success",
      "high_water": "2026-04-22T11:18:00-05:00",
      "note": "2 kept"
    },
    "crm": {
      "status": "skipped",
      "high_water": null,
      "note": "CRM connector unavailable in this session"
    }
  },
  "items": [
    {
      "source": "superhuman",
      "source_id": "18fabc123",
      "timestamp": "2026-04-22T10:30:00-05:00",
      "summary": "Sent email to Andy re component wizard next steps."
    },
    {
      "source": "codex",
      "source_id": "019db8ca-f63b-7063-9eae-40e40a0def34",
      "timestamp": "2026-04-22T14:01:00-05:00",
      "end_timestamp": "2026-04-22T14:15:00-05:00",
      "summary": "Worked in Codex from workspace: Implement context-sweep."
    }
  ]
}
```

## Writer Guarantees

The helper will:

- create the target daily note or `## Log` section if needed
- write bullets with hidden stable markers keyed by source + native id
- update existing marker-matched bullets instead of duplicating them
- keep insertions chronological within `## Log`
- preserve source event times instead of using sweep time
- advance only successful per-source checkpoints on non-dry runs

After the write:

- report what was created, updated, unchanged, skipped, or failed
- call out best-effort limits honestly
- do not claim CRM coverage if the CRM connector or database access was unavailable
