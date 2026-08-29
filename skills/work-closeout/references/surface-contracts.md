# Surface Contracts

## Relevance

A surface is relevant when it is the subject's current authority, the exact source or generated artifact involved, a current-facing index made stale by the outcome, an exact existing tracker for the work, or the active period record materially affected by it.

## Treatment

| Class | Treatment |
|---|---|
| Canonical current | Update only supported status, decision, owner, and next move. |
| Active period | Record one concise outcome and update an existing matching row rather than duplicating it. |
| Raw source | Preserve exact content and provenance; create a distinct file for different material. |
| Source ledger | Add one idempotent entry for new exact source material. |
| Generated artifact | Preserve the body; update lifecycle metadata and link the fulfilled outcome. |
| Current-derived index | Refresh only claims that are now false or incomplete. |
| Historical | Preserve what was true then; add a dated correction or link only when needed. |
| Protected human material | Do not edit without authority for that exact human-owned change. |
| Runtime proof | Use as evidence, never as the only durable current record. |
| Unrelated | Leave untouched. |

Never reconstruct raw source from a summary. If an intended source filename exists, reuse identical content, add provenance without rewriting the supplied body when safe, or create a distinct dated filename.

## External records

An external update is eligible only when the object already exists, its exact identifier is available, the active evidence proves the new value, the requested action is authorized, and the approved tool can read it before and after mutation.

Do not create objects, send messages, publish, deploy, purchase, sign, delete, archive, merge, or guess a target as a closeout side effect. Completion status requires proof of the whole tracked task, not merely the end of the current thread.

## Lifecycle and idempotency

Keep workflow states distinct. Typical content states are `prepared`, `drafted`, `approved`, `sent`, `acknowledged`, `delivered`, and `validated`; code states may include `implemented`, `tested`, `committed`, `pushed`, `merged`, `deployed`, and `user-validated`.

Before writing, look for the same date, outcome, source header, artifact path, or external comment. A repeat run should produce no material change unless new evidence appears.

Minimum verification is readback of every changed surface plus a literal search for the old state across the resolved subject home. Historical and raw matches may remain; current-authoritative contradictions may not.
