# ChatGPT Deep Research Order

Use this lane for non-urgent, broad-source research, synthesis, or verification that benefits from an extra outside pass.

Read [[../references/chatgpt-handoffs.md]] and adapt the Deep Research template into the following user-facing shape:

## Required Output Shape

`ChatGPT Deep Research Order`

`Why this lane`
- 1-3 crisp bullets about why Deep Research is worth the extra cycle

`Files/context to include`
- exact files, notes, links, or background the user should paste or attach

`Copy/paste order`
- a fenced markdown block using the Deep Research template from `references/chatgpt-handoffs.md`
- keep the order concrete: goal, scope, context, constraints, questions, desired deliverable, and return format

`What to bring back`
- full raw response when possible
- highest-signal sections plus omission note if too large
- sources, links, IDs, copied outputs, or artifacts
- any files or decisions the local agent should reconcile locally

## Guardrails

- Do not recommend Deep Research when a normal local/web lookup is enough.
- Keep the order copy/paste ready; do not hand the user a half-filled scaffold.
- Preserve the return-boundary language that keeps ChatGPT output non-canonical until the local agent reconciles it.
