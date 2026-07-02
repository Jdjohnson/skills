# ChatGPT Agent Lane

Use this lane when ChatGPT Agent or ChatGPT-side browser reach is needed beyond
Dot's normal local tools. Direct placement is the preferred mechanism for
placing the ChatGPT order when a safe ChatGPT/browser-control path is available;
ChatGPT Agent is the product lane being ordered.

## Decide Browser Control vs Agent

- Browser control only:
  - local ChatGPT app control
  - reopen/focus the right chat
  - recover the app into the right place before a handoff
- Agent:
  - interactive browsing
  - forms, logins, and key retrieval
  - sensitive or judgment-heavy web work the user should oversee
- Browser control plus Agent:
  - browser control can help set up or recover the right ChatGPT chat first,
    then direct placement should place the Agent order when available

## Output Rules

- If browser control alone is enough:
  - return `Use browser control next`
  - explain why browser control is sufficient
  - explicitly name the available browser/Atlas/Chrome skill to use for app
    control details
- If Agent is required:
  - return `ChatGPT Agent Order`
  - include a `Browser assist` line only when app/browser control should be used
    first

## Required Agent Order Shape

Read [order templates](order-templates.md), [direct placement](direct-placement.md),
and [desktop packet](desktop-packet.md), then adapt the Agent template into this
user-facing shape.

`ChatGPT Agent Order`

`Why this lane`
- why Agent is needed instead of local tooling

`Execution path`
- `Direct browser placement` when direct placement is available
- `Desktop packet` plus the blocker when direct placement is unavailable,
  unsafe, unsuitable, blocked, or explicitly requested

`Files/context to include`
- exact context Dot should provide to ChatGPT
- for direct placement, list uploaded local files and non-file context separately
- for packet fallback, local uploadable files should match the Desktop packet
  contents exactly

`Required ChatGPT connectors/apps`
- required-only connector or app list, or `None`

`Direct placement run`
- ChatGPT thread URL/status, selected mode/model/tool when visible, uploaded
  files, and result or waiting state

Packet-only sections:
- `Copy/paste order`: a fenced markdown block using the Agent template
- `Desktop packet`: absolute folder path, `PROMPT.md`, exact upload files, and
  omitted upload files if trimmed to `20`
- `What to bring back`: structured result Dot can reconcile locally; URLs, IDs,
  copied page text, logs, artifacts, blockers, and judgment calls

`Result handling`
- what Dot captured from ChatGPT and how it will be reconciled locally
