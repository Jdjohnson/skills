# Gather

Use the connectors, files, or local histories that the user has configured. Do not assume a particular mail, chat, notes, task, or database product.

Build a normalized payload:

- `sources`: status metadata keyed by a stable lowercase source slug.
- `items`: kept items with `source`, `source_id`, `timestamp`, and `summary`.
- Optional `end_timestamp` for ranged activity.

For every source:

1. Gather from its effective lower bound.
2. Exact-filter by source-native event time.
3. Use the source's stable event or record ID for deduplication.
4. Mark unavailable or partial sources honestly and leave their checkpoints unchanged.
5. Never replace unavailable live evidence with an unsupported inference.

Local Codex sessions can be summarized deterministically:

```bash
python3 <skill-root>/scripts/context_sweep.py codex --since "<ISO-8601>"
```
