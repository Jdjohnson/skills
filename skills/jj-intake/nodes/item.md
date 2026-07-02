---
description: |
  One-item five-field review format for jj-intake.
---

## Item Handling

Handle exactly one brought-forward item at a time.

Items shown to Jarad must use only this user-facing format:

```text
Title: {Dot-created short title}
Link: {URL, email/thread reference, or "No link captured"}
Overview: {Dot-created summary based on a quick review of the local intake file}
Relevance: {project, priority, relationship, or "No clear project or priority inferred"}
Suggestion: {one exact suggestion option}
```

Do not add extra headings, route menus, decision prompts, or separate rationale
sections to the item review. If the item needs caveats, include them concisely
inside `Overview` or `Relevance`.

## Field Rules

`Title` is Dot-created. Do not echo the sender or raw subject unless that is
genuinely the clearest title.

`Link` is the original URL, email/thread reference, or source reference captured
in the text/email. If no source was captured, write `No link captured`.

`Overview` is based on a quick review of the local intake file only. Do not
browse, live-read Gmail, Superhuman, Twilio, or Mailgun, or perform fresh
research while preparing the review item.

`Relevance` names the supported project, priority, relationship, or inferred
purpose. If the local capture does not support a connection, write
`No clear project or priority inferred`.

`Suggestion` must be exactly one of:

1. `Create and store an intake-sized briefing doc in the day folder.`
2. `Jarad adds context to help Dot better understand the intent.`
3. `Hand this to ms-dot-work as a Dot Work task card.`

## Quiet Filing

Before showing the review queue, quietly file obvious distractions or items that
are not tied to a project or priority.

Quiet-filed items:

- go to the current day log at
  `DOT_TARGET_WORKSPACE/timeline/.../YYYY-MM-DD-day/dot/intake-quiet-log-YYYY-MM-DD.md`;
- are recorded in the run receipt;
- are moved to the handled archive;
- are not shown to Jarad during the review unless he asks.

## Acting After Jarad Responds

Map Jarad's response to one of the current outcomes:

- `briefing-doc` for option 1 or equivalent language;
- `needs-context` for option 2 or equivalent language;
- `implement` for option 3 or equivalent language;
- `quiet-log` for pre-authorized quiet filing;
- `defer`, `drop`, or `draft-reply` when Jarad explicitly asks for that.

`implement` means the intake item becomes a real work packet and must be handed
to `ms-dot-work` capture/run. Do not execute bounded delegated work inside
`jj-intake`, and do not treat the five-field intake approval as approval of the
full Dot Work task card.

Outbound sends, publishing, inbox cleanup, or external account mutations always
need explicit Jarad approval after the draft/action is visible.

`defer` must include a reason and review date. If either is missing, ask one
targeted follow-up before moving the item.
