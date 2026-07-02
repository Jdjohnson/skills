# Selector

Use this node first when the lane is not already explicit.

## Decision Sequence

1. If the user explicitly invoked `$chatgpt` or used ChatGPT-order language, stay
   inside this skill even if the task might also fit a local skill.
2. If the user explicitly brings back ChatGPT output, route to
   [inbound](inbound-chatgpt.md) before any outbound order lane. If he explicitly
   asks to send something back to ChatGPT, digest the inbound result first, then
   choose the outbound lane.
3. If the request already names a lane, route directly:
   - `ChatGPT inbound`, `ChatGPT returned`, `from ChatGPT`,
     `Chat order result`, `ChatGPT Pro said`, or `Dot Daily packet` ->
     [inbound](inbound-chatgpt.md)
   - `ChatGPT Deep Research` -> [deep research](lane-deep-research.md)
   - `ChatGPT Agent` -> [agent](lane-atlas-agent.md)
   - `ChatGPT Pro review` -> [pro review](lane-pro-review.md)
4. If the task needs broad-source synthesis, external verification, or
   non-urgent research work beyond a quick local/web lookup, choose
   [deep research](lane-deep-research.md).
5. If the task needs ChatGPT-side browser reach beyond Dot's local tools, choose
   [agent](lane-atlas-agent.md).
6. If the task needs a second opinion, prep pass, counterarguments, or hardening
   review and there is time for another model pass, choose
   [pro review](lane-pro-review.md).
7. If local tools or subagents can finish faster and safer, return `Keep Local`.
8. For any selected outbound ChatGPT lane, use direct placement when a safe
   ChatGPT/browser-control path is available; use the Desktop packet only when
   direct placement is unavailable, unsafe, unsuitable, blocked, or explicitly
   requested.

## Keep Local Rule

Use `Keep Local` when ChatGPT is clearly the wrong tool, not just because the
task is doable locally. If the user explicitly asked for a ChatGPT order and
ChatGPT is merely optional, still pick the best ChatGPT lane.

Unlabeled pasted material is not inbound ChatGPT material. Route it by the
normal local skill unless the user explicitly identifies it as a ChatGPT return.

## Output

- `Keep Local`
  - one sentence why ChatGPT is unnecessary here
  - one sentence stating the recommended local next step
  - do not create a Desktop packet
- or route to the selected lane node and follow its order schema
