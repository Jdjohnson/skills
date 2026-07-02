# ChatGPT Pro Review Order

Use this lane when a hard question, draft, architecture, or decision would
benefit from a second pass, prep pass, or hardening review and there is time for
it.

Read [order templates](order-templates.md), [direct placement](direct-placement.md),
and [desktop packet](desktop-packet.md), then adapt the Pro review template into
the following user-facing shape.

## Required Output Shape

`ChatGPT Pro Review Order`

`Why this lane`
- 1-3 bullets on why another model pass is worth it here

`Execution path`
- `Direct browser placement` when direct placement is available
- `Desktop packet` plus the blocker when direct placement is unavailable,
  unsafe, unsuitable, blocked, or explicitly requested

`Files/context to include`
- exact artifacts, files, excerpts, or constraints Dot should provide to ChatGPT
- for direct placement, list uploaded local files and non-file context separately
- for packet fallback, local uploadable files should match the Desktop packet
  contents exactly

`Required ChatGPT connectors/apps`
- required-only connector or app list, or `None`

`Direct placement run`
- ChatGPT thread URL/status, selected mode/model/tool when visible, uploaded
  files, and result or waiting state

Packet-only sections:
- `Copy/paste order`: a fenced markdown block using the Pro review template
- `Desktop packet`: absolute folder path, `PROMPT.md`, exact upload files, and
  omitted upload files if trimmed to `20`
- `What to bring back`: best recommendation, strongest objections, specific
  changes Dot should make, residual risks, source material / evidence appendix,
  and full raw response when possible

`Result handling`
- what Dot captured from ChatGPT and how it will be reconciled locally

## Guardrails

- Do not use Pro review when immediate execution matters more than extra
  thinking.
- Keep the order concrete and adversarial enough to produce a useful
  counterweight, not generic agreement.
