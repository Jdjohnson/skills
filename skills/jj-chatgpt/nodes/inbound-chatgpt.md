# ChatGPT Inbound Digest

Use this node when the user explicitly brings back material from ChatGPT for Dot to
digest, route, or incorporate locally.

## Trigger

Route here only when provenance is explicit, including:

- `ChatGPT returned`
- `from ChatGPT`
- `Chat order result`
- `ChatGPT Pro said`
- `Dot Daily packet`
- other clear wording that the pasted material came from ChatGPT

Do not infer ChatGPT provenance from a long paste alone. If provenance is unclear
and it changes handling, ask one targeted question; otherwise route by the
normal local skill.

## Required Output Shape

`ChatGPT Inbound Digest`

`Source/provenance`
- name the ChatGPT surface or return type the user identified

`What ChatGPT was doing`
- infer the original job from the return when safe
- say what is missing if the prompt or task is not visible

`Best local Dot lane`
- pick the downstream Dot skill or route that should reconcile the material
- use the routing map below when the label is clear

`What to accept`
- extract only useful decisions, drafts, claims, tasks, summaries, evidence, or
  proposed changes
- avoid echoing the full ChatGPT return unless the user needs the raw text preserved

`What needs verification`
- name claims, dates, links, code changes, source citations, or task-state
  updates Dot should verify before canonizing

`Canonical handling`
- state where the material should go next and what must remain evidence-only
- do not write durable records from this node alone unless the user explicitly asks

`Next local action`
- name the immediate local step, usually invoking or following the selected
  downstream skill

## Routing Map

| Inbound label | Local Dot lane |
|---------------|----------------|
| Briefs, brief, executive brief | `jj-brief` |
| Brainstorm, ideation | `jj-brainstorm` |
| Context Sweep, sweep, daily context | local context-sweep follow-up; do not treat as CRM/Codex proof |
| Dot Daily, morning journal, morning packet | `ms-plan` day-planning lane |
| Meeting prep, meeting recap, meeting closeout | `ms-meeting` |
| Writing, draft, article, post | `jj-writing`; use `jj-writer` for personal voice polishing |
| Steelman, pressure-test, stress-test | `jj-steelman` |
| Sales, CRM, deal, opportunity | `ms-sales` or `ms-crm`, depending on whether the next step is analysis or CRM mutation |
| Docs, agreements, reports | `ms-docs` |

If no label matches, choose the local skill from the content and the user's intent.
If multiple lanes are plausible and the next write would be durable, ask one
targeted question.

## Guardrails

- Dot stays canonical. Treat the ChatGPT return as delegated source material
  until the selected local skill reconciles it.
- Inbound returns do not use [direct placement](direct-placement.md),
  [desktop packet](desktop-packet.md), or outbound lane nodes unless the user
  explicitly asks to send something back to ChatGPT.
- Preserve the token-saving purpose: summarize, extract, and route instead of
  reprinting the return.
- For `Dot Daily packet`, route through `ms-plan` day planning before doing
  extra local sweeps.
