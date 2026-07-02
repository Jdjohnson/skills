---
name: jj-chatgpt
description: >
  ChatGPT escalation router for Dot. Use when the user says `$chatgpt`, asks for
  a ChatGPT order, explicitly mentions ChatGPT Deep Research, ChatGPT Agent, or
  ChatGPT Pro review, or brings back an explicit ChatGPT return for Dot to
  digest. Decide whether the work should stay local, become a ChatGPT order, or
  be treated as inbound ChatGPT source material to reconcile through Dot's local
  skills. Do not use for plain `deep research` without ChatGPT wording.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
---

# JJ ChatGPT Orders And Returns

Turn ChatGPT use into an explicit order and return surface Dot can route on purpose.

This is a JJ Pack skill. The canonical product source lives under
`addons/jarad-pack/skills/jj-chatgpt/` in Dot Core; installed workspace and
agent-home copies are derived.

## Lane Routing

| Lane | Use When | Output | Node |
|------|----------|--------|------|
| `auto` | default, `$chatgpt`, or generic ChatGPT-order wording | `Keep Local` or the right ChatGPT order | [selector](nodes/selector.md) |
| `inbound` | explicit ChatGPT result/return, Chat order result, ChatGPT Pro said, or Dot Daily packet | `ChatGPT Inbound Digest` | [inbound](nodes/inbound-chatgpt.md) |
| `deep-research` | explicit ChatGPT Deep Research request/order | `ChatGPT Deep Research Order` | [deep research](nodes/lane-deep-research.md) |
| `agent` | explicit ChatGPT Agent request/order | `ChatGPT Agent Order` or browser-control note | [agent](nodes/lane-atlas-agent.md) |
| `pro-review` | explicit ChatGPT Pro review request/order | `ChatGPT Pro Review Order` | [pro review](nodes/lane-pro-review.md) |

## Core Routing Rules

1. Load shared local controls first:
   - [local guardrails](nodes/local-guardrails.md)
   - [trust boundary](nodes/trust-boundary.md)
   - `ROUTES.md` when durable local handling is needed
2. If the user explicitly brings back ChatGPT output, route to
   [inbound](nodes/inbound-chatgpt.md) before any outbound order lane. Inbound
   ChatGPT wording includes `ChatGPT returned`, `from ChatGPT`,
   `Chat order result`, `ChatGPT Pro said`, and `Dot Daily packet`.
3. Do not infer ChatGPT provenance from a long paste alone. If provenance is
   unclear and it changes handling, ask one targeted question; otherwise route
   by the normal local skill.
4. For outbound ChatGPT orders, also load:
   - [direct placement](nodes/direct-placement.md)
   - [desktop packet](nodes/desktop-packet.md)
   - [order templates](nodes/order-templates.md)
5. Explicit ChatGPT wording wins. `$chatgpt`, `place a Chat order`,
   `place a ChatGPT order`, and explicit ChatGPT product names all invoke this
   skill.
6. Do not trigger on bare `order` language alone. Require `chat`, `ChatGPT`, or
   a ChatGPT lane name nearby.
7. Precedence:
   - explicit inbound ChatGPT returns beat outbound ChatGPT-order routing
   - `$chatgpt` and ChatGPT-order wording route here
   - plain `deep research` without ChatGPT wording should stay local unless
     the user asks for a ChatGPT order
   - direct browser-control requests can use a browser/Atlas/Chrome skill by
     itself; inside this skill, browser control is only the setup/helper lane
     for ChatGPT work
8. If the task is simple, local, or time-critical and the user did not insist on
   ChatGPT, return `Keep Local` with one sentence why.
9. Otherwise route to Deep Research, Agent, or Pro review and draft the order
   using [order templates](nodes/order-templates.md).
10. Prefer a safe direct ChatGPT/browser-control path when available, but treat
    browser paste, file upload, connector selection, and run start as an
    external send. Present the exact final prompt and upload list first, then
    wait for explicit user approval before placing the order in ChatGPT. Use
    Desktop packet / copy-paste only when direct placement is unavailable,
    unsafe, unsuitable, blocked, or explicitly requested.
11. If direct placement is approved and succeeds, capture the ChatGPT thread URL/status,
    uploaded files, result or waiting state, and any raw output needed for Dot
    to reconcile locally.
12. Keep user-facing language as `order`; keep bridge language such as
    `HANDOFF PATCH` unchanged when a returned artifact uses it.
13. When Dot uploads files through direct placement or prepares fallback files
    for ChatGPT upload, respect the current product upload cap:
    - default assumption: ChatGPT Pro allows at most `20` uploaded local files
      per batch unless the user says otherwise
    - direct uploads should use the highest-priority `20` local files when more
      candidates exist
    - fallback packets include `PROMPT.md`, which must exactly match the final
      copy/paste order
    - fallback packets use one flat upload folder with `PROMPT.md` plus `20` or
      fewer upload files at its root
    - if more than `20` upload files are candidates, include the highest-priority
      `20` and name omitted files in the response
14. When the user brings back a ChatGPT context-sweep result, treat it as an
    incoming sweep packet that still requires local Codex follow-up for CRM,
    local `sales/` reconciliation, and Codex chat/session sweeps.

## Context Sweep Returns

Incoming ChatGPT context-sweep output is source material, not complete local
coverage. Accept ChatGPT-managed connector findings, then do the Codex-owned
follow-up for CRM deal-state checks, approved local `sales/` reconciliation, and
local Codex chat/session sweeps. Report plainly:

`ChatGPT covered its available connectors; Dot still needs to handle CRM and local Codex follow-up.`

## Output Contract

- `Keep Local`: brief explanation plus the recommended local next step.
- ChatGPT inbound:
  - title: `ChatGPT Inbound Digest`
  - `Source/provenance`
  - `What ChatGPT was doing`
  - `Best local Dot lane`
  - `What to accept`
  - `What needs verification`
  - `Canonical handling`
  - `Next local action`
- ChatGPT lane:
  - title: `ChatGPT Deep Research Order`, `ChatGPT Agent Order`, or
    `ChatGPT Pro Review Order`
  - `Why this lane`
  - `Execution path`: `Direct browser placement` or `Desktop packet`, with the
    reason when using the packet
  - `Files/context to include`
  - `Required ChatGPT connectors/apps`
  - `Direct placement run` when direct placement is used: ChatGPT thread
    URL/status, selected mode/model/tool when visible, uploaded files, and
    result or waiting state
  - `Approval needed` when direct placement has not yet been explicitly
    approved: final prompt summary, exact upload list, and requested approval to
    place the order in ChatGPT
  - packet-only sections when direct placement is not used: `Copy/paste order`,
    `Desktop packet`, and `What to bring back`
  - `Result handling`: how Dot will reconcile the ChatGPT output locally
- Browser-control setup-only case:
  - say `Use browser control next` and name the available browser/Atlas/Chrome
    skill instead of inventing a user-run Agent order.

## Node Map

- [selector](nodes/selector.md)
- [local guardrails](nodes/local-guardrails.md)
- [trust boundary](nodes/trust-boundary.md)
- [inbound](nodes/inbound-chatgpt.md)
- [direct placement](nodes/direct-placement.md)
- [desktop packet](nodes/desktop-packet.md)
- [order templates](nodes/order-templates.md)
- [deep research](nodes/lane-deep-research.md)
- [agent](nodes/lane-atlas-agent.md)
- [pro review](nodes/lane-pro-review.md)
