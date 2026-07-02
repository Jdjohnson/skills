# Order Templates

Use these templates for ChatGPT order prompts. Fill every relevant field; remove
empty scaffolding before creating a packet or placing the order.

## Deep Research

```md
Use ChatGPT Deep Research for this.

Goal:

Why Deep Research is useful here:

Scope:

Current context:

Files or background to include:

Constraints:

Questions to answer:

Desired deliverable:

Return format:
- Executive answer
- Repo-compatible patch or structured updates
- Supporting evidence and sources
- Recommended action
- Open questions or risks
- Source material / evidence appendix
- Full raw response
```

## Agent

```md
Use ChatGPT Agent for this. If browser setup or recovery helps inside the ChatGPT app, use it first, then switch to Agent for the web work.

Objective:

Why Agent is needed:

Sensitivity or oversight notes:

Credentials boundary:

Context or files to include:

Exact steps to take:

Stop if:

What to bring back:
- What was completed
- Structured result Dot can reconcile locally
- URLs, IDs, copied results, or artifacts
- Any copied page text, logs, or raw captures clearly marked as source material
- Blockers
- Any judgment calls to hand back to Dot or the user
```

## Pro Review

```md
Use ChatGPT Pro for a review pass on this.

Artifact or question under review:

Why a second pass is valuable:

Review mode: prep | second opinion | hardening

Files or context to include:

Stress-test these angles:

What a good answer should do:

Return format:
- Best recommendation
- Strongest objections
- Specific changes Dot should make
- Residual risks
- Source material / evidence appendix
- Full raw response
```

## Return Rule

When direct placement is the execution path, Dot should bring back the full
ChatGPT response directly, not just a summary, unless the response is too large
to capture. If it is too large, capture the highest-signal sections plus a note
about what was omitted.

When the Desktop packet path is used, the user should bring back the full ChatGPT
response, not just a summary, unless the response is too large to paste. If it
is too large, bring back the highest-signal sections plus a note about what was
omitted.

Dot is responsible for turning returned ChatGPT output into the local, durable
result. Only structured patch proposals are candidates for canonical changes.
Raw response sections, copied source text, logs, and artifacts stay in the
evidence lane unless Dot explicitly promotes them.
