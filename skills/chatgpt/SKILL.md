---
name: chatgpt
description: |
  Route explicit ChatGPT work: $chatgpt, ChatGPT orders, Deep Research, Agent,
  or Pro review. Decide whether the task stays local or becomes a ChatGPT
  order, then place it through host-supported browser control or prepare a
  bounded fallback packet.
---

# ChatGPT Orders

Turn ChatGPT use into an explicit order surface the local agent can route on purpose.

## Lane Routing

| Lane | Use When | Output | Node |
|------|----------|--------|------|
| `auto` | default, `$chatgpt`, or generic ChatGPT-order wording | `Keep Local` or the right ChatGPT order | [[nodes/selector.md]] |
| `deep-research` | explicit ChatGPT Deep Research request/order | `ChatGPT Deep Research Order` | [[nodes/lane-deep-research.md]] |
| `agent` | explicit ChatGPT Agent request/order | `ChatGPT Agent Order` | [[nodes/lane-agent.md]] |
| `pro-review` | explicit ChatGPT Pro review request/order | `ChatGPT Pro Review Order` | [[nodes/lane-pro-review.md]] |

## Core Routing Rules

1. Load shared controls plus the trust boundary:
   - [[shared/interaction-gates.md]]
   - [[shared/output-discipline.md]]
   - [[nodes/trust-boundary.md]]
   - [[nodes/direct-placement.md]]
   - [[nodes/fallback-packet.md]]
2. Explicit ChatGPT wording wins. `$chatgpt`, `place a ChatGPT order`, `place a Chat order`, `here is your ChatGPT order`, and explicit ChatGPT product names all invoke this skill.
3. Do not trigger on bare `order` language alone. Require `chat`, `ChatGPT`, or a ChatGPT lane name nearby.
4. Precedence:
   - `$chatgpt` and ChatGPT-order wording beat any local ambient research path.
   - Plain `deep research` without ChatGPT wording should stay with the local/default research path when available.
5. If the task is simple, local, or time-critical and the user did not insist on ChatGPT, return `Keep Local` with one sentence why.
6. Otherwise route to Deep Research, Agent, or Pro review and draft the order using [[references/chatgpt-handoffs.md]] for prompt shape and return expectations.
7. Prefer [[nodes/direct-placement.md]] when the host supports browser control and file upload. If direct placement is unavailable, blocked, unsafe, or explicitly not wanted, use [[nodes/fallback-packet.md]].
8. Keep user-facing language as `order`.

## Output Contract

- `Keep Local`: brief explanation plus the recommended local next step.
- ChatGPT lane:
  - title: `ChatGPT Deep Research Order`, `ChatGPT Agent Order`, or `ChatGPT Pro Review Order`
  - `Why this lane`
  - `Execution path`: `Host-supported browser/direct` or `Fallback order/packet`, with the reason when falling back
  - `Files/context to include`
  - `Required ChatGPT connectors/apps`
  - if direct placement is used: thread URL/status when available, selected mode/tool when visible, uploaded files, and result or waiting state
  - if direct placement is not used: `Copy/paste order`, optional `Fallback packet`, and `What to bring back`
  - `Result handling`
  - `Copy/paste order`
  - `What to bring back`

## Reference Map

- Copy/paste order templates and the return boundary live in [[references/chatgpt-handoffs.md]].
- Fallback packet helper: `scripts/build_desktop_packet.py`.

## Support Map

| File | Purpose |
|------|---------|
| [[nodes/selector.md]] | Choose Keep Local, Deep Research, Agent, or Pro review. |
| [[nodes/trust-boundary.md]] | Keep ChatGPT delegated and the local agent canonical. |
| [[nodes/direct-placement.md]] | Place an order directly when the host supports it. |
| [[nodes/fallback-packet.md]] | Build a copy/paste packet when direct placement is unavailable. |
| [[nodes/lane-deep-research.md]] | Shape a Deep Research order. |
| [[nodes/lane-agent.md]] | Shape an Agent order. |
| [[nodes/lane-pro-review.md]] | Shape a Pro review order. |
| [[shared/interaction-gates.md]] | Preserve approval and handoff gates. |
| [[shared/output-discipline.md]] | Keep outputs bounded and state-aware. |
