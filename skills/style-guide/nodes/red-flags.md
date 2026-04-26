---
description: Find the highest-risk style drift in a draft.
---

## Red-Flag Scan

Load [[source-of-truth.md]] first. If a calibrated voice profile exists in the conversation, use it. If not, infer only from available examples or explicit instructions.

Lead with the problems most likely to make the writing sound wrong for the target voice.

## What To Flag

- padded openings or throat-clearing
- generic insight language
- over-explained transitions
- corporate abstraction or brand-speak
- fake balance that weakens the real position
- rhythm that feels too smooth, symmetrical, or model-shaped
- claims that sound bigger than the evidence
- words or phrases the target writer would not use
- paragraph shape that does not fit the channel
- loss of useful roughness, edge, humor, warmth, or directness

## Severity

- **Critical**: meaning or voice identity breaks.
- **High**: strong style drift that likely needs revision.
- **Medium**: noticeable issue, easy to fix.
- **Low**: polish-level friction.

## Output

```markdown
## Red Flags

| Severity | Problem | Evidence | Fix Direction |
|---|---|---|---|
| High | ... | "..." | ... |

## Priority Fix Order
1. ...
2. ...
3. ...
```

Quote the smallest span needed to prove the issue. Do not turn a red-flag scan into a full rewrite unless asked.
