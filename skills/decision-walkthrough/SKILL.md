---
name: decision-walkthrough
description: Walk through supplied feedback, research, notes, audits, plans, drafts, or links one decision at a time. Use when the user asks to decide item by item; not for brainstorming from scratch or immediate implementation.
---

# Decision Walkthrough

Turn source material into explicit decisions without overwhelming the user or silently implementing the result.

## Prepare

1. Read the supplied and authorized discoverable sources before asking for facts.
2. Reconcile conflicts and distinguish quotation, fact, inference, and material assumption.
3. Break the material into decision units, ordered by dependency.
4. Infer whether the user wants exhaustive coverage or only decisions that change action. Group duplicates and mechanical corrections without hiding them.

Before the first item, state the coverage approach and any missing source that materially limits confidence. Use `Item X of Y` only when the set is finite and the count helps orientation.

## Walk one item

For each decision:

1. State what the source says and why a decision is needed.
2. Recommend a resolution and name the main tradeoff.
3. If evidence is insufficient, recommend **Needs evidence** and the fastest responsible way to resolve it.
4. Ask one direct decision question, then stop for the user's response.

Do not invent motives, ownership, reactions, costs, or consequences. If the user challenges the premise or requests exact wording, verify and repair the item before asking again.

Record one state in a running conversational log:

- **Accepted** — the user explicitly agrees.
- **Revised** — the user chooses a changed resolution.
- **Deferred** — the user intentionally postpones it.
- **Needs evidence** — missing facts prevent a responsible decision.

Do not treat silence or “probably” as acceptance, and do not move to implementation while the walkthrough is open.

## Complete

Reconcile the log against the original source, surface deferred items and evidence gaps, and provide a short ordered implementation checklist. Ask the user to confirm the completed walkthrough before planning or executing the resulting work.

Keep the log in the conversation by default. Save it only when the user asks or approves, using any destination rules documented by the active environment.
