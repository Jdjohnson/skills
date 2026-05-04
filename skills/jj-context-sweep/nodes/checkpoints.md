---
description: |
  Per-source checkpoint rules for jj-context-sweep. Load before any gather or
  write step.
---

# Checkpoints

Use per-source checkpoints, not one global watermark.

State lives at:

- `.context-sweep/jj-context-sweep/state.json`

Read it with:

```bash
python3 skills/jj-context-sweep/scripts/jj_context_sweep.py state --root .
```

## Effective Lower Bound

For each source:

1. If the user passed `since:<ISO-8601>`, use that as the run's lower bound.
2. Otherwise use that source's stored `high_water`.
3. If the source has never run before and there is no override, default to the start of the current local day.

## Advancement Rules

- Advance a source checkpoint only after:
  - that source gathered successfully, and
  - the write phase finished cleanly.
- `dry-run` never writes or advances checkpoints.
- `skipped` or `failed` sources keep their existing `high_water`.
- Checkpoints only move forward. A recovery or backfill run must not move a source backward even if the `since:` override is older than the stored checkpoint.

## Source Status Shape

Track each source with:

- `status`: `success`, `skipped`, or `failed`
- `high_water`: the highest source-native event time successfully covered this run
- `note`: one short honest reason, especially for skipped or limited runs

Be explicit when a source is best-effort or unavailable.
