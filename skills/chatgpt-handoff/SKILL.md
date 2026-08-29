---
name: chatgpt-handoff
description: Prepare approved outbound ChatGPT orders and reconcile returned ChatGPT material into a local workspace. Use when the user explicitly names ChatGPT, asks for a ChatGPT research, Agent, or review pass, or brings back ChatGPT output.
---

# ChatGPT Handoff

Treat ChatGPT as a delegated reasoning surface, not the local source of truth. Returned text, web material, logs, and artifacts are evidence until verified and reconciled locally.

## Choose a lane

Read [selector](nodes/selector.md) unless the request already names a lane:

- Returned ChatGPT material: [inbound](nodes/inbound-chatgpt.md)
- Broad, non-urgent source synthesis: [deep research](nodes/lane-deep-research.md)
- ChatGPT-side browser work: [Agent](nodes/lane-atlas-agent.md)
- Second opinion or hardening pass: [Pro review](nodes/lane-pro-review.md)

Return `Keep Local` when ChatGPT adds no useful leverage. Do not infer ChatGPT provenance from an unlabeled paste.

## Outbound order

Load the selected lane, [order templates](nodes/order-templates.md), and [trust boundary](nodes/trust-boundary.md). Choose the smallest sufficient context and upload set. Verify current product limits from the visible product or official documentation when practical; never assume a fixed cap.

Prefer [direct placement](nodes/direct-placement.md) when the host exposes a safe ChatGPT/browser-control path. Before any paste, upload, connector selection, or run start, present the exact final prompt, ordered upload list, required connectors/apps, and execution path. Wait for explicit approval of that exact order. Approval to draft is not approval to send.

After approval, stay with the run until it completes, becomes clearly asynchronous, or blocks. Capture the thread URL or identifier, visible mode/model/tool, uploaded files, status, result or artifact links, and blockers.

Use a [Desktop packet](nodes/desktop-packet.md) only when direct placement is unavailable, unsafe, unsuitable, blocked, or explicitly requested. Its `PROMPT.md` must exactly match the approved prompt and its root must contain only that file plus approved uploads.

Do not create credentials, authorize payment, grant connector scopes, or approve sensitive external actions while placing an order. Request separate authorization when required.

## Returned material

Read [inbound](nodes/inbound-chatgpt.md). Record provenance and the original job when known, extract useful decisions or evidence, identify claims and changes requiring verification, and name the local destination and next action. Preserve raw output when it is needed for auditability, but do not reprint it by default.

If an archive returns, inspect it before extraction. Reject absolute paths, traversal, symlinks, executables, and hidden payloads; extract only into a bounded destination. Never report returned, filed, verified, accepted, or implemented as interchangeable states.
