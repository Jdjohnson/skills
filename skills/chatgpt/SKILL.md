---
name: chatgpt
version: 1.0.0
description: |
  ChatGPT escalation router. Use when the user says `$chatgpt`, asks for a
  ChatGPT order, or explicitly mentions ChatGPT Deep Research, ChatGPT Agent,
  or ChatGPT Pro review. Decide whether the work should stay local or become a
  ChatGPT order, then draft the right order with the context to include and
  what should come back.
argument-hint: "[deep-research | agent | pro-review]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - AskUserQuestion
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
2. Explicit ChatGPT wording wins. `$chatgpt`, `place a ChatGPT order`, `place a Chat order`, `here is your ChatGPT order`, and explicit ChatGPT product names all invoke this skill.
3. Do not trigger on bare `order` language alone. Require `chat`, `ChatGPT`, or a ChatGPT lane name nearby.
4. Precedence:
   - `$chatgpt` and ChatGPT-order wording beat any local ambient research path.
   - Plain `deep research` without ChatGPT wording should stay with the local/default research path when available.
5. If the task is simple, local, or time-critical and the user did not insist on ChatGPT, return `Keep Local` with one sentence why.
6. Otherwise route to Deep Research, Agent, or Pro review and draft the order using [[references/chatgpt-handoffs.md]] for prompt shape and return expectations.
7. Keep user-facing language as `order`.

## Output Contract

- `Keep Local`: brief explanation plus the recommended local next step.
- ChatGPT lane:
  - title: `ChatGPT Deep Research Order`, `ChatGPT Agent Order`, or `ChatGPT Pro Review Order`
  - `Why this lane`
  - `Files/context to include`
  - `Copy/paste order`
  - `What to bring back`

## Reference Map

- Copy/paste order templates and the return boundary live in [[references/chatgpt-handoffs.md]].

## Node Map

- [[nodes/selector.md]]
- [[nodes/trust-boundary.md]]
- [[nodes/lane-deep-research.md]]
- [[nodes/lane-agent.md]]
- [[nodes/lane-pro-review.md]]

## Shared Dependencies

- Interaction gates: [[shared/interaction-gates.md]]
- Output discipline: [[shared/output-discipline.md]]
