---
description: |
  Conservative keep/skip rules for context-sweep. Load after gathering and
  before writing.
---

# Classify

Default to conservative logging. Keep an item only when it is:

- work-related
- decision-relevant
- likely to matter when reconstructing context later
- meaningfully additive versus what is already in the daily note

Skip:

- trivial acknowledgements
- low-signal chatter
- pure logistics with no decision value
- repeated follow-ups that add no new context
- duplicates already represented in the daily note or in the current sweep payload

## Source-Specific Notes

- Superhuman: keep substantive outbound work mail that moves work, clarifies direction, or captures meaningful commitments.
- Slack: keep messages that contain decisions, coordination, asks, status moves, or useful working context. Skip emoji-only or quick-thanks traffic.
- Notion: keep pages/edits that clearly represent meeting notes, working doctrine, planning artifacts, or records likely to matter later.
- CRM: keep real deal-state movement, new notes, or noteworthy value/stage changes. Skip rows that add no meaningful state change.
- Codex: keep sessions only when the user prompts or resulting work clearly represent real progress, decisions, or meaningful investigation.

## Output Standard

Every kept item should be a short clean summary that reads well in the daily note:

- no raw dumps
- no connector jargon
- no invented facts
- no pretending certainty when the source is partial

If a source is partial, say so in the source-status note, not in every bullet.
