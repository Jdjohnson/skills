---
name: style-guide
version: 1.1.0
description: |
  Voice calibration and style enforcement skill. Use to infer a target voice
  from examples, audit drafts for style drift, provide rewrite guidance, or
  run a final publish checklist.
argument-hint: "[calibrate | check | rewrite | redflags | checklist] [text, file path, or excerpt]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - AskUserQuestion
---

# Style Guide

Help writing stay in the intended voice instead of drifting into generic, corporate, or AI-sounding prose.

## Modes

| Mode | Use When | Output | Node |
|------|----------|--------|------|
| `calibrate` | Starting a draft or building a reusable voice profile | Operational voice rules | [[nodes/calibrate.md]] |
| `check` | Auditing a draft against a known or inferred voice | Red flags plus checklist verdict | [[nodes/red-flags.md]] + [[nodes/checklist.md]] |
| `rewrite` | Revising copy while preserving meaning and stance | Revised copy plus style notes | [[nodes/rewrite.md]] |
| `redflags` | Fast triage of likely style violations | Highest-risk style problems only | [[nodes/red-flags.md]] |
| `checklist` | Final pre-publish pass | Pass/revise verdict | [[nodes/checklist.md]] |

If no mode is given, choose `check` when text is present and `calibrate` when the user is preparing to write.

## Routing

1. Load [[nodes/source-of-truth.md]].
2. Determine whether the user supplied pasted text, a file path, source examples, a style description, or only an intent.
3. Route to the selected mode.
4. If `check`, `rewrite`, `redflags`, or `checklist` has no usable draft, ask for the draft or excerpt.
5. If no style target exists, ask for examples or infer a temporary target from the user's description. Mark it as provisional.

Do not invent a voice profile from nothing. A style guide is allowed to infer from evidence, not pretend.

## Output

For audits, lead with the few issues that matter most. For rewrites, provide the revised copy first, then a short explanation of the style moves made.

## Node Map

- Core rules: [[nodes/source-of-truth.md]]
- Calibration: [[nodes/calibrate.md]]
- Red flags: [[nodes/red-flags.md]]
- Rewrite: [[nodes/rewrite.md]]
- Checklist: [[nodes/checklist.md]]
