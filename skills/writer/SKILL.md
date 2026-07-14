---
name: writer
description: |
  Writing partner for turning rough ideas, notes, or drafts into publishable
  prose. Use for articles, essays, posts, memos, talks, or other writing that
  needs intake, goal clarity, story extraction, research, structure, drafting,
  and refinement.
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

## Voice and refinement

Use samples, a style brief, or workspace instructions supplied by the user as optional calibration. During refinement, remove formulaic AI-writing patterns without erasing the writer's meaning or natural cadence. The skill has no required voice profile or companion skill.

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
