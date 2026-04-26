# Selector

Use this node first when the lane is not already explicit.

## Decision Sequence

1. If the user explicitly invoked `$chatgpt` or used ChatGPT-order language, stay inside this skill even if the task might also fit a local skill.
2. If the request already names a lane, route directly:
   - `ChatGPT Deep Research` -> [[lane-deep-research.md]]
   - `ChatGPT Agent` -> [[lane-agent.md]]
   - `ChatGPT Pro review` -> [[lane-pro-review.md]]
3. If the task needs broad-source synthesis, external verification, or non-urgent research work beyond a quick local/web lookup, choose [[lane-deep-research.md]].
4. If the task needs browser reach beyond the local agent's tools, choose [[lane-agent.md]].
5. If the task needs a second opinion, prep pass, counterarguments, or hardening review and there is time for another model pass, choose [[lane-pro-review.md]].
6. If local tools or subagents can finish faster and safer, return `Keep Local`.

## Keep Local Rule

Use `Keep Local` when ChatGPT is clearly the wrong tool, not just because the task is doable locally. If the user explicitly asked for a ChatGPT order and ChatGPT is merely optional, still pick the best ChatGPT lane.

## Output

- `Keep Local`
  - one sentence why ChatGPT is unnecessary here
  - one sentence stating the recommended local next step
- or route to the selected lane node and follow its order schema
