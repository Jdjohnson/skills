# ChatGPT Deep Research Order

Use this lane for non-urgent, broad-source research, synthesis, or verification
that benefits from an extra outside pass.

Read [order templates](order-templates.md), [direct placement](direct-placement.md),
and [desktop packet](desktop-packet.md), then adapt the Deep Research template
into the following user-facing shape.

## Required Output Shape

`ChatGPT Deep Research Order`

`Why this lane`
- 1-3 crisp bullets about why Deep Research is worth the extra cycle

`Execution path`
- `Direct browser placement` when direct placement is available
- `Desktop packet` plus the blocker when direct placement is unavailable,
  unsafe, unsuitable, blocked, or explicitly requested

`Files/context to include`
- exact files, notes, links, or background Dot should provide to ChatGPT
- for direct placement, list uploaded local files and non-file context separately
- for packet fallback, local uploadable files should match the Desktop packet
  contents exactly

`Required ChatGPT connectors/apps`
- required-only connector or app list, or `None`

`Direct placement run`
- ChatGPT thread URL/status, selected mode/model/tool when visible, uploaded
  files, and result or waiting state

Packet-only sections:
- `Copy/paste order`: a fenced markdown block using the Deep Research template
- `Desktop packet`: absolute folder path, `PROMPT.md`, exact upload files, and
  omitted upload files if trimmed to `20`
- `What to bring back`: full raw response when possible, highest-signal
  sections plus omission note if too large, sources, links, IDs, copied outputs,
  artifacts, and any files or decisions Dot should reconcile locally

`Result handling`
- what Dot captured from ChatGPT and how it will be reconciled locally

## Guardrails

- Do not recommend Deep Research when a normal local/web lookup is enough.
- Keep the order concrete and ready to run; do not leave half-filled scaffolds.
- Preserve the return-contract language that keeps ChatGPT output non-canonical
  until Dot reconciles it.
