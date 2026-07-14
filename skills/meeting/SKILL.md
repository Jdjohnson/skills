---
name: meeting
description: Prepare for a meeting, close it out, find meeting history, or review patterns across meetings using available source material. Use for prep, debriefs, decisions, open loops, or source-backed meeting reviews.
---

# Meeting

Help the user prepare, close the loop, find history, and review patterns. Keep the work concise, source-backed, and compatible with the user's workspace conventions.

## Modes

| Mode | Result |
|---|---|
| `prep` | A practical brief for an upcoming meeting |
| `close` | A recap with decisions, open questions, and proposed follow-ups |
| `history` | A small source-backed list or summary of past meetings |
| `review` | Patterns across a date range, person, account, project, or topic |

Infer the mode when it is clear. Ask one targeted question when ambiguity would change the work.

## Resolve the meeting

Use the lightest useful source set:

1. The path, link, title, attendee, date, or source named by the user.
2. Calendar context when available.
3. Existing meeting history in the workspace.
4. Linked notes, transcripts, documents, chat, or email.
5. Project context only when it materially improves the answer.

Preserve direct source links. If content is inaccessible, keep the link and label that limitation. Label summaries supplied by the user as user-provided.

## Durable records

Follow an explicit workspace route when one exists. Otherwise propose this portable structure before creating it:

`meetings/YYYY/MM/YYYY-MM-DD-HHMM-slug/`

| Item | Route |
|---|---|
| Canonical record | `meeting.md` |
| Generated prep, closeout, review, or draft | `generated/` |
| Raw notes, transcript, export, or link index | `source/` |

Keep only the canonical record at the meeting-folder root. Do not place meeting records in unrelated project folders or the workspace root.

## Prep

Classify depth from the stakes. Routine meetings get a flash brief; high-stakes, one-to-one, client, sales, or decision meetings get deeper prior context.

Include: what this is, what matters, specific talking points or decisions, useful prior context, real watchouts, and sources. Never manufacture an agenda item just to fill a section.

## Close

Prefer real capture: transcript or notes, linked documents, user-provided notes, then a short guided debrief. If capture is strong, do not ask questions for the sake of interactivity. If it is thin, ask only what is needed to avoid fabricating outcomes.

Include: concise summary, decisions, proposed tasks or delegations, open questions, requested follow-up draft, and sources. Proposed tasks remain proposals.

## History and review

Search canonical meeting records first and return the smallest useful result set with dates, titles, source links, and paths. Read generated or raw sources only when the canonical record is thin or the user asks for deeper evidence.

For reviews, synthesize repeated decisions, open loops, risks, changes over time, and useful next questions. Save a review only when the user asks for a durable artifact.

## Integrity rules

- Never invent decisions, commitments, attendees, quotes, or source links.
- Label uncertainty and unavailable sources plainly.
- Do not create tasks directly from proposed follow-ups without approval.
- Draft outbound follow-ups only when asked; never send without explicit approval.
- Do not assume any particular calendar, notes, mail, or chat provider is installed.
