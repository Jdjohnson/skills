---
name: work-log
description: Reconcile and close out the active work thread across the workspace's relevant authoritative and current-facing records. Use only when the user explicitly asks to log, close out, or record proven outcomes, decisions, lifecycle changes, source artifacts, next moves, and bounded updates to exact existing external records.
---

# Work Log

Treat closeout as one bounded state-reconciliation transaction. Do not call work closed merely because one daily entry was written.

## Governing rule

Make each relevant authoritative or current-facing surface agree with the proven outcome while preserving raw and historical evidence.

"Relevant" means a surface whose present state would otherwise be false or materially incomplete. It does not mean every file that mentions the subject.

Read the workspace's routing and write instructions before editing.

## Invocation authority

Run only after an unambiguous request such as `$work-log`, `log this work`, or `close out this thread`.

The invocation authorizes:

- local writes needed to reconcile proven state under workspace instructions; and
- routine, reversible synchronization of an exact existing external record when the verified outcome directly determines its status, comment, or date.

It does not authorize creating external records, sending email or chat, changing calendars, publishing, purchasing, signing, deleting, or another difficult-to-reverse action. Mark an exact existing task complete only when the user states it is complete or the evidence proves full completion. Ending a thread is not completion evidence.

## Workflow

### 1. Establish proven changes

Extract only source-backed facts from the active task:

- outcome and decision;
- exact lifecycle transition, such as `drafted`, `sent`, `delivered`, `merged`, `deployed`, or `validated`;
- date, owner, and next move;
- exact user-provided source material; and
- external or tool readback evidence.

Do not infer a later lifecycle state from an earlier one. If evidence is incomplete, preserve the narrower state and name the gap.

### 2. Resolve the subject home

Use paths and identifiers already present in the task, workspace instructions, and a bounded local search to find the existing project, client, meeting, timeline, or skill home. Do not invent a parallel home or guess an external record.

Inspect only candidate surfaces that exist and whose present state the outcome affects, such as:

- the current-day log and its matching task row;
- the project's current-state file;
- exact source folders and source ledgers;
- drafts or deliverables involved in the outcome;
- current-facing indexes or READMEs;
- an existing relevant memory entry when workspace rules permit it; and
- exact existing external records already identified by URL or stable ID.

### 3. Classify before editing

Classify each candidate as canonical current state, raw or historical source, agent-created artifact, derived current-facing index, protected human material, or unrelated.

Build the intended change set before writing. If two homes remain genuinely ambiguous after inspection, update only unambiguous surfaces and report the unresolved choice.

### 4. Reconcile local state

Apply only changes supported by the proven outcome:

1. Add or update one concise current-day progress entry and change an existing matching task row only when its state is proven.
2. Update the canonical current record's status, decision, and next move.
3. Save exact user-provided source material in the configured source location and update an existing source ledger. Never reconstruct missing raw source from a summary.
4. Update lifecycle metadata on involved agent-created drafts or artifacts and link the fulfilled outcome. Preserve the original body.
5. Refresh current-facing indexes only when they assert a now-false state.
6. Update memory only when workspace instructions allow it and the fact materially improves re-entry or continuity.

Preserve dated research and historical statements that were accurate when written. Add a dated note or link when later context is useful; do not rewrite history into the latest state.

### 5. Synchronize exact external records

Use the external platform's approved tool or owner workflow. The target must already exist and be unambiguous. Make only the routine reversible update proved by the outcome, then read it back.

Before adding a comment or progress entry, check whether the same outcome is already recorded. If the platform cannot be inspected safely, skip the mutation and report the blocked readback rather than risk a duplicate.

### 6. Verify the transaction

Re-read every changed local file and every mutated external record. Run a bounded contradiction check across the resolved subject home using the exact stale state, new state, artifact name, or external ID.

Closeout is complete only when:

- every required local write succeeded;
- authorized external updates were read back;
- no current-authoritative contradiction remains;
- raw and historical evidence was preserved; and
- repeating the closeout would not create a duplicate.

If any required surface remains stale, ambiguous, or inaccessible, report `partial` rather than `complete`.

## Receipt

Return a short receipt with the proven lifecycle transition, local surfaces updated, external readback evidence, relevant surfaces intentionally preserved, skipped or blocked surfaces, and the remaining next move. Do not list generic targets that were never relevant.
