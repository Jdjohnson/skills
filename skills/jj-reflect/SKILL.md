---
name: jj-reflect
description: |
  Reflect across Jarad's journal material without taking over day planning or
  inbox intake. Reads the new Dot timeline day folders, their source journal
  files, and migrated Old Dot journal/context-sweep material when relevant.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# JJ Reflect

Standalone reflection lane migrated out of the old `jj-journal` shape.

Use this when Jarad asks for `$jj-reflect`, asks to reflect on journals, asks
what patterns show up in his writing, or uses a legacy trigger such as
`$jj-journal reflect`.

Do not use this as the owner for day planning, inbox intake, outbound drafting,
or broad context sweeps. Route those to their current owners.

## Mode Routing

| Mode | Use When | Behavior | Node |
|------|----------|----------|------|
| today | Jarad asks to reflect today, this morning, or on the current entry | Read current `MEMORY.md` pointers, current day folder, and current day source journal files before reflecting | [sources](nodes/sources.md), [workflow](nodes/workflow.md) |
| date/range | Jarad gives a date, week, month, or "last few days" | Read all matching new Dot day files and source journal files for that range, plus migrated Old Dot material if it matches | [sources](nodes/sources.md), [workflow](nodes/workflow.md) |
| theme | Jarad asks about a theme, pattern, concern, or recurring thread | Search journal/source material for the theme, then read the surrounding entries before synthesizing | [sources](nodes/sources.md), [workflow](nodes/workflow.md) |
| legacy | Jarad says `$jj-journal reflect` or references the old reflection flow | Treat it as `$jj-reflect`; do not revive old `jj-journal` intake/planning behavior | [sources](nodes/sources.md), [workflow](nodes/workflow.md) |

## Core Rules

1. Load [sources](nodes/sources.md) first for every run.
2. Load [workflow](nodes/workflow.md) before producing the reflection.
3. New Dot journal sources live under `/Users/jaradjohnson/Dot/timeline/`.
4. Always consider both the day markdown file and the day's `source/` files.
   Relevant patterns include:
   - `/Users/jaradjohnson/Dot/timeline/**/<YYYY-MM-DD>-day/<YYYY-MM-DD>-day.md`
   - `/Users/jaradjohnson/Dot/timeline/**/<YYYY-MM-DD>-day/source/*journal*.md`
   - `/Users/jaradjohnson/Dot/timeline/**/<YYYY-MM-DD>-day/source/*context-sweep*journal*.md`
   - `/Users/jaradjohnson/Dot/timeline/**/<YYYY-MM-DD>-day/source/*old-dot*.md`
5. For current-day reflection, read `/Users/jaradjohnson/Dot/MEMORY.md` first
   and follow its Today/Week pointers.
6. Read `/Users/jaradjohnson/Dot/resources/preferences/planning.md` when
   morning-reflection prompts matter.
7. Old Dot references are read-only. Check them only when relevant:
   - `/Users/jaradjohnson/Developer/ai-hub/Dot/`
   - `/Users/jaradjohnson/.cache/dot/jj-journal/`
   - `/Users/jaradjohnson/.cache/dot/jj/`
8. Treat cache files, weather files, receipts, and runtime artifacts as support
   context only, not as journals.
9. Preserve Jarad's raw words when quoting is useful, but do not overexpose
   private journal content. Prefer short paraphrases plus source file paths.
10. Do not write to timeline files, `resources/`, or external systems unless
    Jarad explicitly asks for a capture/update after the reflection.
11. Outbound sends, posts, publishing, calendar invites, and external mutations
    require explicit approval.

## Boundaries

- `$ms-plan day` owns day planning and capture.
- `$jj-intake` owns Dot comms inbox triage.
- `$jj-writer` owns Jarad-voice polishing for drafts.
- `dot-runtime/` is proof/cache, not durable journal truth.
- This skill can read broadly across journals, but it should keep the answer
  centered on the reflection Jarad asked for.

