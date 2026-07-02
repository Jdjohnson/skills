---
name: meeting-doc
description: |
  Meeting document skill for creating one useful prep, closeout, history, or
  review document from supplied context. Use when the user wants a practical
  meeting artifact without setting up a meeting database or workflow system.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Meeting Doc

Create one useful meeting document from supplied context, reachable files, URLs, transcripts, notes, or a short user debrief.

## Mode Routing

| Mode | Trigger | When | Node |
|------|---------|------|------|
| `prep` | before a meeting, "get me ready" | Build a practical prep brief | [[nodes/prep.md]] |
| `close` | after a meeting, "close this out" | Capture outcomes and follow-up suggestions | [[nodes/close.md]] |
| `history` | "what happened before", prior notes | Summarize supplied prior context | [[nodes/history.md]] |
| `review` | patterns across notes or range | Synthesize repeated themes and adjustments | [[nodes/review.md]] |

Default mode: infer from the request.

## Core Rules

1. Load [[nodes/input-handling.md]] and [[nodes/writing-standards.md]] first.
2. Use only supplied context or host-supported retrieval that is clearly available from the request.
3. Do not assume a calendar, transcript app, mail inbox, chat workspace, local meeting database, or durable history system.
4. Ask only when the meeting target, mode, or intended output is genuinely ambiguous.
5. Ground claims in the available evidence. Say when the record is too thin.
6. Keep one document as the primary output.
7. Use [[nodes/file-output.md]] only when the user asks to save or provides a destination.

## Output Contract

- Prep: `What This Is`, `What Matters`, `Talking Points / Decisions`, `Context`, `Watchouts`.
- Close: `What Happened`, `Decisions`, `Commitments`, `Open Questions`, `Suggested Follow-Up`.
- History: relevant prior meetings or notes, why they matter, and unresolved threads.
- Review: repeated pattern, what is improving, what is stuck, recurring decisions, recommended adjustment.

## Node Map

- [[nodes/input-handling.md]]
- [[nodes/prep.md]]
- [[nodes/close.md]]
- [[nodes/history.md]]
- [[nodes/review.md]]
- [[nodes/writing-standards.md]]
- [[nodes/file-output.md]]
