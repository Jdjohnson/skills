---
name: writer
version: 1.1.0
description: |
  Writing partner for turning rough ideas, notes, or drafts into publishable
  prose. Use for articles, essays, posts, memos, talks, or other writing that
  needs intake, goal clarity, story extraction, research, structure, drafting,
  and refinement.
argument-hint: "[start | draft | refine | humanize] [topic, notes, draft, or file path]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Writer

Guide rough material into a clear draft while preserving the user's meaning, stance, and voice.

## Mode Routing

| Mode | Use When | Start Node |
|------|----------|------------|
| `start` | New idea, topic, notes, or brain dump | [[nodes/phase-01-intake.md]] |
| `draft` | User wants a first draft quickly | [[nodes/phase-06-draft.md]] |
| `refine` | User has an existing draft | [[nodes/phase-07-refine.md]] |
| `humanize` | User wants AI-pattern cleanup | [[nodes/phase-07-refine.md]] |

If no mode is provided, infer from the request:

- New idea or brain dump: start with intake.
- Existing draft: start with refine.
- "Just draft it": draft with best available assumptions.
- "Humanize this": refine for natural rhythm and remove AI-pattern residue.

## Workflow

Run the workflow rules in [[nodes/workflow.md]], then use the phase nodes:

1. Intake: [[nodes/phase-01-intake.md]]
2. Goal: [[nodes/phase-02-goal.md]]
3. Extract: [[nodes/phase-03-extract.md]]
4. Research: [[nodes/phase-04-research.md]]
5. Structure: [[nodes/phase-05-structure.md]]
6. Draft: [[nodes/phase-06-draft.md]]
7. Refine: [[nodes/phase-07-refine.md]]

## Optional Companion Passes

If a separate style-guide skill is available, use it as a companion for calibration, red flags, and final checklist. If a humanizer-style cleanup skill is available, use it during refinement when the draft has AI-pattern residue. These are optional helpers, not hard dependencies.

## Output

Return the draft or revised copy plus a short note naming the most important remaining choices or risks. Save to a file only when the user asks or provides a destination.

## Node Map

- Workflow rules: [[nodes/workflow.md]]
- Intake: [[nodes/phase-01-intake.md]]
- Goal: [[nodes/phase-02-goal.md]]
- Extract: [[nodes/phase-03-extract.md]]
- Research: [[nodes/phase-04-research.md]]
- Structure: [[nodes/phase-05-structure.md]]
- Draft: [[nodes/phase-06-draft.md]]
- Refine: [[nodes/phase-07-refine.md]]
