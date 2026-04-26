---
name: meeting-doc
description: |
  Meeting document skill for creating one useful prep, closeout, history, or
  review document from supplied context. Use when the user wants a practical
  meeting artifact without setting up a meeting database or workflow system.
---

# Meeting Doc

Create one useful meeting document from the context available in the chat, files, calendar details, transcript, notes, or user debrief.

## Modes

- `prep`: get ready before a meeting.
- `close`: capture what happened after a meeting.
- `history`: summarize prior meeting context supplied by the user.
- `review`: synthesize patterns across multiple supplied meeting notes.

Infer the mode from the request. Ask only when the target meeting or intended output is ambiguous.

## Prep Document

Use this shape:

```markdown
# Prep Brief: [Meeting Title]

## What This Is

## What Matters

## Talking Points / Decisions

## Context

## Watchouts
```

Keep routine meetings short. Do not pad with fake strategy.

## Closeout Document

Use this shape:

```markdown
# Meeting Closeout: [Meeting Title]

## What Happened

## Decisions

## Commitments

## Open Questions

## Suggested Follow-Up
```

Separate commitments from suggestions. Do not create tasks or send follow-ups unless the user asks.

## Review Document

Use this shape:

```markdown
# Meeting Review: [Range or Topic]

## Pattern

## What Is Improving

## What Is Stuck

## Recurring Decisions

## Recommended Adjustment
```

## Rules

- Ground talking points and decisions in evidence.
- Say when the record is too thin.
- Keep one document as the output.
- Save to a file only if the user asks or provides a destination.
- Do not manage durable meeting history unless the user's environment already has that system and they explicitly ask you to use it.
