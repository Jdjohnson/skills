---
description: |
  Local queue refresh, source-of-truth, display, and ordering rules for
  jj-intake.
---

## Queue Refresh

Refresh first, but keep it safe.

Preferred local command:

```bash
cd /Users/jaradjohnson/Developer/projects/dot-comms
DOT_COMMS_HOME=/Users/jaradjohnson/Developer/projects/dot-comms DOT_TARGET_WORKSPACE=/Users/jaradjohnson/Dot node integrations/comms-mcp/sync-inbox.mjs
```

If the command fails because comms env vars are missing or relay access is down,
continue from the existing `DOT_COMMS_HOME/inbox/` files and report reduced
freshness.

If a comms MCP tool is already available in the host, `comms_promote_inbound`
is an acceptable equivalent because it writes local files before acknowledging
remote relay items.

## Source Of Truth

After refresh, `DOT_COMMS_HOME/inbox/*.md` is the active queue. Default
`DOT_COMMS_HOME` is `/Users/jaradjohnson/Developer/projects/dot-comms`. Do not
live-read Gmail, Superhuman, Twilio, or Mailgun as part of the triage
conversation unless Jarad explicitly asks for investigation.

Read each file enough to capture:

- file path
- source metadata from the `<!-- intake:{...} -->` comment
- sender/source/time
- sender class
- route
- Dot-created title
- original link or source reference from the text/email, when present
- Dot-created overview based on a quick review of the local capture
- relevance to an active project, priority, or inferred purpose when apparent
- suggested next step
- useful excerpt from Context, Brief, Media, or Message

## Preview

Before handling items, show one scan-friendly queue preview for the items that
were not quietly filed. Use this format for each listing:

```text
Dot intake: N items after refresh.

1. Title: {Dot-created short title}
   Link: {URL, email/thread reference, or "No link captured"}
   Overview: {Dot-created summary based on a quick review of the item}
   Relevance: {project, priority, relationship, or "No clear project or priority inferred"}
   Suggestion: {one exact suggestion option from the list below}
```

`Suggestion` must be exactly one of these strings:

1. `Create and store an intake-sized briefing doc in the day folder.`
2. `Jarad adds context to help Dot better understand the intent.`
3. `Hand this to ms-dot-work as a Dot Work task card.`

For `Title`, do not echo the sender or raw subject unless that is genuinely the
best title. Create a short, useful title from the local capture.

For `Link`, prefer the original URL or email/thread/source reference captured in
the text/email. If there is no captured link, write `No link captured`.

For `Overview`, use the local inbox item only. Do not browse, live-read Gmail,
Superhuman, Twilio, or Mailgun, or perform fresh research for the preview.

For `Relevance`, tie the item to a known project, priority, relationship, or
likely intent when the local capture supports it. If the connection is weak,
write `No clear project or priority inferred`.

For `Suggestion`, choose the single best exact option based on the local
capture. Do not execute it from the preview.

Option 3 is a handoff, not in-intake execution. If Jarad chooses it, preserve
the `ms-dot-work` task-card approval gate before any bounded delegated work is
run.

Then begin item 1 unless Jarad picks a different item.

The preview and item review use the same five-field format. Do not switch to an
expanded readback style before Jarad responds.

## Ordering

Default sort:

1. owner or pinned items
2. known senders
3. unknown/noise

Within each group, oldest first.
