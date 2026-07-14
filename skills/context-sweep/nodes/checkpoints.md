# Checkpoints

Use one high-water mark per configured source.

Read or initialize state with:

```bash
python3 <skill-root>/scripts/context_sweep.py state --root .
```

For each source, use the explicit `since:` value when provided; otherwise use that source's stored high-water mark. A new source defaults to the start of the current local day.

Advance a checkpoint only when the source gathered successfully and the write completed. Dry runs, skipped sources, and failed sources never advance. Checkpoints move forward only.

Track `status` (`success`, `skipped`, or `failed`), `high_water`, and a concise `note` for each source.
