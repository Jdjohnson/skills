# Host-Supported Browser Placement

Use this node for any ChatGPT lane when the current host exposes browser control or another direct ChatGPT placement path.

## Required Behavior

- Draft the final ChatGPT order before opening or focusing ChatGPT.
- Use the host's available browser/direct-control capability only when it can complete the order without new credentials, payment, consent, or unsafe side effects.
- Open or focus ChatGPT, choose the appropriate product surface when visible, paste the finalized order, upload local files directly, and start the run.
- Respect the `20` local upload-file cap unless the user says the product limit changed; use the highest-priority `20` files and record omissions.
- Keep required connectors/apps required-only. Select already-authorized connectors/apps when safe and visible; do not force new authorization.
- Stay with the browser run until ChatGPT returns a result, clearly moves to async/background work, or blocks.
- Capture the ChatGPT thread URL or visible identifier when available, selected mode/model/tool when visible, upload list, status, raw result or artifact links, and any blocker.

## Fallback Conditions

Use [[fallback-packet.md]] when:

- browser/direct control is unavailable in the host
- ChatGPT is inaccessible, logged out, blocked by MFA, or needs new user consent
- upload fails after a bounded retry or no usable upload path is visible
- required connectors/apps cannot be selected without new authorization
- the order involves sensitive web actions that need manual user oversight
- the user explicitly asks for the manual packet/copy-paste route

## Result Handling

- Treat ChatGPT output as source material until the local agent reconciles it.
- If the run completes directly, bring back the full raw response or artifact links yourself.
- If the run remains pending or async, report the thread URL/status and the next check needed.
