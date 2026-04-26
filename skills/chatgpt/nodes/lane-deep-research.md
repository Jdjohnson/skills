# ChatGPT Deep Research Order

Use this lane for non-urgent, broad-source research, synthesis, or verification that benefits from an extra outside pass.

Read [[../references/chatgpt-handoffs.md]] and adapt the Deep Research template into the following user-facing shape:

## Required Output Shape

`ChatGPT Deep Research Order`

`Why this lane`
- 1-3 crisp bullets about why Deep Research is worth the extra cycle

`Execution path`
- `Host-supported browser/direct` when [[direct-placement.md]] can be used, otherwise `Fallback order/packet` with the reason

`Files/context to include`
- exact files, notes, links, or background the user should paste or attach

`Required ChatGPT connectors/apps`
- required-only list; say `None` when no connector or app is required

`Copy/paste order`
- a fenced markdown block using the Deep Research template from `references/chatgpt-handoffs.md`
- keep the order concrete: goal, scope, context, constraints, questions, desired deliverable, and return format

`Fallback packet`
- include only when [[fallback-packet.md]] is used

`What to bring back`
- full raw response when possible
- highest-signal sections plus omission note if too large
- sources, links, IDs, copied outputs, or artifacts
- any files or decisions the local agent should reconcile locally

`Result handling`
- say how the local agent should treat the return as source material and reconcile it locally

## Guardrails

- Do not recommend Deep Research when a normal local/web lookup is enough.
- Keep the order copy/paste ready; do not hand the user a half-filled scaffold.
- Preserve the return-boundary language that keeps ChatGPT output non-canonical until the local agent reconciles it.
