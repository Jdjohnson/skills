# Write

Use the helper for deterministic writes and checkpoint updates:

```bash
python3 <skill-root>/scripts/context_sweep.py write --root . --payload-file /path/to/payload.json
python3 <skill-root>/scripts/context_sweep.py write --root . --journal-file /path/to/day.md --payload-file /path/to/payload.json
python3 <skill-root>/scripts/context_sweep.py write --root . --payload-file /path/to/payload.json --dry-run
```

Payload shape:

```json
{
  "sources": {
    "email": {
      "status": "success",
      "high_water": "2026-04-22T11:18:00-05:00",
      "note": "2 kept"
    },
    "tasks": {
      "status": "skipped",
      "high_water": null,
      "note": "connector unavailable"
    }
  },
  "items": [
    {
      "source": "email",
      "source_id": "message-123",
      "timestamp": "2026-04-22T10:30:00-05:00",
      "summary": "Sent the revised scope and requested approval."
    }
  ]
}
```

The helper creates the note or `## Log` section, uses hidden source-and-ID markers, updates marker-matched entries, keeps chronological order, preserves source timestamps, and advances only successful checkpoints on non-dry runs.
