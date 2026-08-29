---
name: work-closeout
description: Reconcile a proven work outcome across the relevant current records, source artifacts, generated deliverables, and exact existing trackers. Use explicitly when a task needs an evidence-backed, idempotent closeout rather than a simple activity note.
---

# Work Closeout

Treat closeout as one bounded state-reconciliation transaction.

## Governing rule

Make every relevant current surface agree with the proven outcome while preserving raw and historical evidence. A surface is relevant only when its present state would otherwise be false or materially incomplete; a keyword match is not enough.

Read the workspace's authority and routing instructions before writing. Read [surface contracts](references/surface-contracts.md) for multi-surface work, source artifacts, external trackers, or ambiguous classification.

## Workflow

1. **Establish proof.** Extract only supported outcomes, decisions, lifecycle transitions, dates, owners, next moves, exact supplied source material, and readback evidence. Preserve the narrowest accurate state when proof is incomplete.
2. **Resolve the subject home.** Use identifiers and routes already present in the task plus bounded search. Do not invent a parallel home or guess an external object.
3. **Inventory and classify.** Inspect affected current records, period logs, source ledgers, generated artifacts, current-facing indexes, protected material, and exact existing trackers. For a multi-surface closeout, resolve `<skill-root>` to this skill's installed folder and run `<skill-root>/scripts/closeout_inventory.py` with explicit roots, literal terms, and ordered `--class-rule CLASS=GLOB` values supplied by workspace routing or the user.
4. **Build the change set.** Separate current, raw, historical, generated, protected, derived, external, and unrelated surfaces before editing. Leave ambiguous surfaces unchanged and report them.
5. **Reconcile locally.** Update only claims made false or incomplete by the proven outcome. Preserve original source and historical prose. Reuse identical records and update existing entries instead of duplicating them.
6. **Synchronize externally only when authorized.** An invocation does not grant external mutation authority. The exact existing object must be identified, the requested change must be proved and within scope, and the platform must support before/after readback. Otherwise skip it.
7. **Verify.** Re-read every changed surface and run a bounded contradiction search for the exact old state, new state, artifact, or identifier.

Report `partial` when any required current surface remains stale, ambiguous, inaccessible, or unverified.

## Completion contract

Closeout is complete only when required writes succeeded, authorized external updates were read back, no current-authoritative contradiction remains, raw and historical evidence survived, and repeating the same closeout would create no duplicate.

Return a short receipt with the proven transition, local updates, external readbacks, intentionally preserved surfaces, blockers, and remaining next move.
