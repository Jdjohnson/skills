# ChatGPT Agent Order

Use this lane when ChatGPT-side browser reach is needed beyond the local agent's normal tools.

## Use Cases

- interactive browsing
- forms, logins, and key retrieval
- sensitive or judgment-heavy web work that benefits from user oversight
- multi-step web tasks that are awkward to do locally

Read [[../references/chatgpt-handoffs.md]] and adapt the Agent template into this user-facing shape:

## Required Output Shape

`ChatGPT Agent Order`

`Why this lane`
- why Agent is needed instead of local tooling

`Execution path`
- `Host-supported browser/direct` when [[direct-placement.md]] can be used, otherwise `Fallback order/packet` with the reason

`Files/context to include`
- exact context the user should provide

`Required ChatGPT connectors/apps`
- required-only list; say `None` when no connector or app is required

`Copy/paste order`
- a fenced markdown block using the Agent template from `references/chatgpt-handoffs.md`
- include objective, oversight notes, credentials boundary, exact steps, stop conditions, and what to bring back

`Fallback packet`
- include only when [[fallback-packet.md]] is used

`What to bring back`
- structured result the local agent can reconcile locally
- URLs, IDs, copied page text, logs, or artifacts clearly marked as source material
- blockers and any judgment calls that need to come back to the local agent or user

`Result handling`
- say how the local agent should treat the return as source material and reconcile it locally
