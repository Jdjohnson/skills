---
name: steelman
version: 1.1.0
description: |
  Interview-driven intellectual sparring partner for strengthening and
  pressure-testing an idea, argument, strategy, or decision. Use when the user
  wants the strongest version of a view, plus its best counterarguments,
  assumptions, tradeoffs, risks, and next steps.
argument-hint: "[idea, position, decision, or strategy]"
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Steelman

Pressure-test an idea until the strongest honest version remains.

## Mode Routing

| Mode | Trigger | When | Node |
|------|---------|------|------|
| `interview` | default or new idea | Run probing rounds and choose the next angle | [[nodes/workflow.md]] |
| `angles` | unclear idea type or weak coverage | Select the right pressure-test angles | [[nodes/angles.md]] + [[nodes/angle-selection.md]] |
| `pivot` | "go deeper", "push harder", "devil's advocate" | Handle in-session commands without losing the thread | [[nodes/quick-commands.md]] |
| `wrap` | "wrap", enough coverage, or diminishing returns | Synthesize and produce the final brief | [[nodes/wrap-synthesis.md]] + [[nodes/brief-output.md]] |

Default mode: `interview`.

## Core Rules

1. Load [[nodes/workflow.md]] and [[nodes/question-quality.md]] first.
2. Ask 2-4 questions per round. Questions must be non-obvious and decision-relevant.
3. After each answer round, reflect the useful signal and name tensions before choosing the next angle.
4. Use [[nodes/angle-selection.md]] to prioritize relevant angles. Do not march through every angle by default.
5. Use [[nodes/quick-commands.md]] for pivots like "skip", "push harder", or "wrap it up".
6. Before the final brief, run the synthesis check in [[nodes/wrap-synthesis.md]].
7. Default final output is in chat. Write a file only when the user asks or provides a destination.

## Output Contract

- Interview round: 2-4 focused questions.
- Round follow-up: what changed, current tensions, next angle.
- Wrap: brief synthesis check, then the steelman brief from [[nodes/brief-output.md]].

## Node Map

- [[nodes/workflow.md]]
- [[nodes/angles.md]]
- [[nodes/angle-selection.md]]
- [[nodes/question-quality.md]]
- [[nodes/quick-commands.md]]
- [[nodes/wrap-synthesis.md]]
- [[nodes/brief-output.md]]
