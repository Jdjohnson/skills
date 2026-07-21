---
name: decision-walkthrough
description: Walk through supplied feedback, research, notes, audits, transcripts, plans, drafts, or links one decision at a time; keep a running decision log and finish with an implementation checklist. Use only on explicit invocation or item-by-item walkthrough language; do not use for ordinary summarization or recommendations.
---

# Decision Walkthrough

Turn a bounded body of source material into settled decisions without overwhelming the user or over-engineering the result.

## Core Contract

- Start with supplied or discoverable source material. Use a general interview or grilling workflow for an idea that starts from scratch.
- Work through one meaningful decision at a time. Ask one question, then wait.
- Research discoverable facts instead of asking the user for them.
- Give a clear recommended answer and the main tradeoff for every decision. If evidence is insufficient, recommend **Needs evidence** and the fastest practical way to resolve it. Never merely list options or say only the user can decide.
- Keep the process quick, plain, and proportionate to real small-to-midsize organization work.
- Maintain one running Markdown decision log. Do not create ADRs, glossaries, or other ceremony.
- Do not plan or implement the resulting changes until the user confirms the completed walkthrough.

## Prepare the Walkthrough

1. Read local instructions and all available source material. Follow links or connected sources when access is available.
2. Reconcile the sources before interpreting them. Distinguish quotation, fact, and inference. Do not assign a person or team motivations, priorities, or concerns the source does not state.
3. Break the material into meaningful decision units and order dependencies first.
4. Infer the requested coverage:
   - For "walk me through all this feedback," cover every item. Group duplicates or mechanical corrections, but show them and confirm their handling.
   - For "help me decide what to do based on this research," walk through the decisions and use supporting facts as evidence.
   - Ask about coverage only when the request is genuinely ambiguous.
5. Before item one, state the coverage approach, high-level categories, walkthrough decision count, and any missing decision source that materially limits confidence. If grouping changes the count, report both the source-item count and the smaller walkthrough count. Use the walkthrough count consistently for `Item X of Y`. Do not report absent general instruction files as source gaps. Do not dump the detailed analysis.

## Keep a Practical Decision Log

Create the log when the first decision is settled. Determine its destination in this order:

1. A path the user explicitly names.
2. A route defined by workspace instructions.
3. An existing log associated with the same meeting, project, opportunity, or source material.
4. A proposed filename beside the most relevant source or in the current working folder.

Preserve existing local structure. Ask only if inspection leaves two genuinely valid homes or if writing requires user approval.

Treat structure as scaffolding, not a form. Most items need only:

- **Decision**: what the user chose
- **Why**: the practical reason, when it matters
- **Action**: what this changes

Add evidence, constraints, tradeoffs, ownership, or implementation detail only when omitting them could cause a mistake. Never add empty sections.

## Walk Through One Item

Use a compact pattern:

1. `Item X of Y: <short title>`
2. What the source says
3. Why a decision is needed
4. Recommended resolution and main tradeoff
5. One direct decision question

Then stop and wait for the user's response.

If the user challenges the premise or asks for exact wording, pause, verify the evidence, and repair the item before seeking a decision. Do not present a plausible assumption or scope boundary as the resolution of a factual unknown.

A recommendation may use practical judgment, but it must not invent motivations, ownership, customer reactions, costs, or operational consequences. Label any supported assumption that materially drives it. If choosing would require filling an evidence gap with generic business assumptions, recommend **Needs evidence** instead and ask only for the single fastest missing fact; do not also ask for the final decision in that turn.

For example, if a source says Finance calls `$20k` workable and Delivery prefers `$25k` for protection, do not translate that into competitiveness versus margin. First identify what risk the extra `$5k` covers or whether `$20k` is already committed.

Record one state:

- **Accepted**: the user explicitly agrees.
- **Revised**: the user changes the recommendation; restate the result and confirm only if ambiguity remains.
- **Deferred**: the user intentionally postpones it.
- **Needs evidence**: missing facts prevent a responsible decision.

Do not move on while an item is merely "probably fine."

## Preserve Speed and Scope

- Use one meaningful decision, not one comment or sentence, as the unit.
- Group items only when they share one decision, have no independent tradeoffs, and can use one implementation rule. Say what was grouped.
- Keep separate choices with different cost, scope, risk, ownership, priority, tone, or implementation consequences.
- Prefer the smallest workable change, existing tools and processes, and reversible choices.
- Add a newly discovered item only when it is necessary to resolve the supplied material. Label it as a **source item** or **derived decision**, explain the updated count, and exclude merely adjacent improvements.
- Stop documenting when the responsible person can understand the decision quickly and act with the people, time, budget, and systems actually available.

## Handle Revisions and Resumption

When the user changes an earlier choice, update the canonical decision rather than leaving a contradiction. Preserve revision history only when it materially helps. Reopen only downstream items affected by the change.

When resuming later:

1. Reopen the log and original sources. If a matching log already exists, treat the request as a resumption even when the user does not use that word.
2. State completed items, the current item, and the remaining count.
3. Revalidate only evidence that may have changed.
4. Continue from the next unresolved item without replaying or reconfirming settled decisions unless changed evidence affects them.

## Complete the Walkthrough

1. Reconcile the log against the original source so nothing was silently missed.
2. Surface deferred items and missing evidence.
3. Finish the log with a short, ordered implementation checklist grouped by the actual destination or owner when useful.
4. Declare the decision walkthrough complete.
5. Wait for the user's explicit confirmation before planning or implementing anything, even if the initial request anticipated implementation.

The final result should be easy for the real person doing the work to understand and use. Simplify anything that does not pass that test.
