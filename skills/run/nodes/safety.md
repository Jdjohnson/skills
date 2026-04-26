---
description: |
  Safety rules for runner-launched work shaped through `/run`.
---

# Run Safety

Apply these rules to any runner-launched work shaped through `/run`.

1. Keep changes inside the current repository by default unless the user explicitly approves another location in the same session.
2. Never send email, SMS, Slack messages, or any other outbound communication on the user's behalf unless they explicitly ask for that exact send and approve the final content in-session.
3. Never write to external systems such as CRM, Asana, Notion, calendars, or chat tools unless the user explicitly approves the specific write in-session.
4. Autonomous runs may read external systems and prepare drafts, briefs, diffs, or proposed updates for later review.
5. Preferred sync direction is external systems to the local repo. Any proposed local to external updates must be flagged, not executed automatically.
