---
name: style-guide
description: |
  Voice calibration and style enforcement skill. Use to infer a target voice
  from examples, audit drafts for style drift, provide rewrite guidance, or
  run a final publish checklist.
---

# Style Guide

Help writing stay in the intended voice instead of drifting into generic, corporate, or AI-sounding prose.

## Modes

- `calibrate`: infer voice rules from examples or a described style.
- `check`: audit a draft against the target voice.
- `rewrite`: revise text while preserving meaning.
- `redflags`: list the highest-risk style problems only.
- `checklist`: run a final pre-publish pass.

If no mode is given, choose `check` when text is present and `calibrate` when the user is preparing to write.

## Calibration

When examples are available, infer:

- sentence length and rhythm
- vocabulary and formality
- humor or warmth
- tolerance for jargon
- paragraph shape
- how directly the writer states claims
- what the writer avoids

Turn those into operational rules, not personality labels.

## Red Flags

Watch for:

- padded openings
- generic insight language
- over-explained transitions
- corporate abstraction
- fake balance
- phrases the target writer would never use
- rhythm that feels too smooth or symmetrical
- claims that sound bigger than the evidence

## Rewrite Rules

- Preserve facts, meaning, and stance.
- Prefer smaller edits when the voice is already close.
- Do not flatten strong opinions into neutral summary.
- Do not add polish that makes the piece less believable.
- Keep useful roughness when it serves the voice.

## Output

For audits, lead with the few issues that matter most. For rewrites, provide the revised copy and a short explanation of the style moves made.
