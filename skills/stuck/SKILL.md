---
name: stuck
description: |
  Practical coaching skill for moments when the user feels stuck, scattered,
  avoidant, or out of rhythm. Use to run a one-question-at-a-time reset that
  surfaces the real tension, identifies the primary blocker, and ends with a
  small plan for today and tomorrow. Not for crisis or clinical care.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
---

# Stuck

Help the user get unstuck without turning the session into therapy, a lecture, or a giant plan.

## Mode Routing

| Mode | Trigger | When | Node |
|------|---------|------|------|
| `reset` | default or a stuck/scattered opener | Run the full mirror-first reset | [[nodes/fit-and-safety.md]] + [[nodes/context-lock.md]] |
| `diagnose` | context is confirmed | Pick one primary blocker | [[nodes/diagnosis.md]] |
| `avoidance` | user is dodging a concrete thing | Name the avoided thing without shame | [[nodes/avoidance.md]] |
| `start` | user is foggy or overloaded | Find the smallest honest move | [[nodes/starting-move.md]] |
| `habit` | user keeps breaking the same way | Interrupt the main loop | [[nodes/interfering-habit.md]] |
| `wrap` | enough signal exists | Produce the compact reset | [[nodes/wrap.md]] |

Default mode: `reset`.

## Core Rules

1. Load [[nodes/tone.md]] first.
2. Start with [[nodes/fit-and-safety.md]]. Do not coach past a crisis, immediate danger, or a request for diagnosis/treatment.
3. Use [[nodes/context-lock.md]] to mirror before reframing. Ask one question at a time by default.
4. Use [[nodes/diagnosis.md]] to force one primary thread.
5. Route into the needed branch nodes only; do not make the session bigger than the user's energy can support.
6. End with [[nodes/wrap.md]].
7. File output, reminders, task creation, and external commitments are opt-in only.

## Output Contract

- Intake: mirror-only context lock plus explicit confirmation.
- Diagnosis: one primary blocker.
- Reset: `Primary blocker`, `Next 30 minutes`, `Win today`, `Setup for tomorrow`, `Ignore for now`.

## Node Map

- [[nodes/tone.md]]
- [[nodes/fit-and-safety.md]]
- [[nodes/context-lock.md]]
- [[nodes/diagnosis.md]]
- [[nodes/avoidance.md]]
- [[nodes/starting-move.md]]
- [[nodes/three-wins.md]]
- [[nodes/interfering-habit.md]]
- [[nodes/wrap.md]]
