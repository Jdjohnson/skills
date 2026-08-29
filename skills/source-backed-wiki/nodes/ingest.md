# Ingest and Write Workflow

## Before editing

1. Read schema, source policy, index, and recent log entries.
2. Resolve every source with:

   ```bash
   node <skill-root>/scripts/wiki-guard.mjs resolve --workspace <workspace> --source <reference> --json
   ```

3. For a multi-source operation, preview the complete source and page target set once before editing.

## Transaction

Every ingest, query-save, connect, or approved lint-fix uses one transaction:

1. Run guarded preflight. It requires a clean nested wiki repository with no remote. Use `--repair-stale-index` only when workspace policy identifies a sync handoff and the guard can prove content equals `HEAD`; never bypass a failed preflight.
2. Record `HEAD` and declare the exact page targets plus `index.md` and `log.md`.
3. Resolve all sources and retain their stable references, real paths, sizes, SHA-256 hashes, and external-policy hash for the active operation.
4. Edit the live wiki tree: declared pages, one index entry per page, and exactly one appended log entry.
5. Resolve every source again immediately before commit. Stop if any reference, path, size, content hash, or policy hash changed.
6. Run `wiki-guard audit --against-ref HEAD --json`.
7. Require exact equality between audited changed paths and declared targets. Require the appended log source set to equal the final source resolution with no missing, extra, or duplicate lines.
8. Stage only declared paths with argument-array Git calls. Verify the staged set and confirm no unstaged or untracked changes remain.
9. Commit one operation with a concise `wiki(<operation>): ...` message.
10. Refresh the workspace's configured search index when one exists.

## Failure

Before staging, a handled failure may restore only declared tracked targets from recorded `HEAD` and remove only new declared pages from this operation. If touched paths are uncertain, leave the dirty state visible. During or after staging, leave state in place and report it; never discard unknown content.

Report pages created or updated, commit ID, rejected sources, contradictions, and skipped items.
