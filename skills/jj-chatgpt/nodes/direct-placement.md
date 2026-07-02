# Direct Placement

Use this node for every ChatGPT lane that is not `Keep Local` when the current
host exposes a safe direct ChatGPT/browser-control path.

## Required Behavior

- Draft the final ChatGPT order prompt before opening or focusing ChatGPT.
- Before any browser paste, upload, or run start, present the finalized prompt,
  ordered local upload-file list, required connectors/apps, and execution path
  to the user.
- Wait for explicit user approval to place that exact prompt and upload list in
  ChatGPT. Approval to draft or prepare an order is not approval to send it.
- After approval, open or focus ChatGPT, choose the appropriate product surface
  when visible, paste the approved order, upload the approved local files
  directly, and start the run.
- Respect the `20` local upload-file cap unless the user says the product limit
  changed; when more files are candidates, use the highest-priority `20` and
  record the omissions.
- Keep required connectors/apps required-only. Select already-authorized
  connectors/apps when safe and visible; do not force new credentials, payment,
  consent, or sensitive permissions.
- Stay with the browser run until ChatGPT returns a result, clearly moves to an
  async/background state, or blocks.
- Capture the ChatGPT thread URL or visible identifier, selected mode/model/tool
  when visible, upload list, status, raw result or artifact links, and any
  blocker.

## Fallback Conditions

Use [desktop packet](desktop-packet.md) when direct placement is unavailable,
blocked, unsafe, unsuitable, or explicitly requested.

Fallback conditions:

- No safe direct ChatGPT/browser-control path is available in the current host.
- ChatGPT is inaccessible, logged out, blocked by MFA, or otherwise requires
  the user's credentials or consent.
- Required file upload fails after a bounded retry, or the product does not
  expose a usable upload path.
- Required connectors/apps cannot be selected without the user authorizing a new
  connection or permission.
- The order involves sensitive web actions where the user explicitly needs manual
  oversight.
- the user explicitly asks for the manual packet/copy-paste method.

When falling back, say why in `Execution path`. Use `Desktop packet` for the
manual packet path.

## Result Handling

- Treat ChatGPT output as source material until Dot reconciles it locally.
- If the run completes through direct placement, bring back the full raw
  response or artifact links yourself instead of asking the user to paste them.
- If the run remains pending or async, report the thread URL/status and the next
  check needed.
