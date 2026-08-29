# Selector

Use this node when the request does not already name a lane.

1. Explicit ChatGPT return or result → [inbound](inbound-chatgpt.md).
2. Explicit ChatGPT Deep Research or broad, non-urgent source synthesis → [deep research](lane-deep-research.md).
3. ChatGPT-side browsing, forms, or interactive web work → [Agent](lane-atlas-agent.md).
4. Second opinion, counterargument, prep, or hardening pass → [Pro review](lane-pro-review.md).
5. If ChatGPT adds no useful leverage, return `Keep Local` with the recommended local next step.

An explicit request for ChatGPT stays in this skill even when local work is possible. An unlabeled paste is not a ChatGPT return. Every outbound lane uses direct placement when safe and available, otherwise the Desktop packet.
