# Journal Source Map

Use this node to gather the minimum complete set of journal files for the
requested reflection. "All relevant journals" means all matching journal
sources for the requested date, range, or theme, not every private note by
default.

## Current Dot Home

Installed Dot home:

- `/Users/jaradjohnson/Dot`

Read first for current context:

- `/Users/jaradjohnson/Dot/MEMORY.md`
- `/Users/jaradjohnson/Dot/resources/preferences/planning.md`

New Dot day folders:

- `/Users/jaradjohnson/Dot/timeline/<year>/week-<WW>_<YYYY-MM-DD>_to_<YYYY-MM-DD>/<YYYY-MM-DD>-day/`

Inside each day folder, check:

- `<YYYY-MM-DD>-day.md`
- `source/*journal*.md`
- `source/*context-sweep*journal*.md`
- `source/*old-dot*.md`
- `source/*context-sweep*.json` only when the markdown journal is absent or the user asks for the raw import

The day file can contain journal sections such as:

- `Morning Journal`
- `Family`
- `Best Thing Yesterday`
- `Day Plan - Dot synthesis`
- `Log`
- `Memory Sweep`

For reflection, prefer the human/raw journal sections and `source/` files over
Dot synthesis. Use Dot synthesis only to understand context, constraints, or
follow-through.

## Old Dot And Migration References

Old Dot root, read-only reference:

- `/Users/jaradjohnson/Developer/ai-hub/Dot/`

Possible legacy locations may or may not exist:

- `/Users/jaradjohnson/Developer/ai-hub/Dot/journal/`
- `/Users/jaradjohnson/Developer/ai-hub/Dot/journals/`
- `/Users/jaradjohnson/Developer/ai-hub/Dot/knowledge/`
- `/Users/jaradjohnson/Developer/ai-hub/Dot/.dot/context/`
- `/Users/jaradjohnson/Developer/ai-hub/Dot/state.md`

Migration/runtime cache, support-only:

- `/Users/jaradjohnson/.cache/dot/jj-journal/`
- `/Users/jaradjohnson/.cache/dot/jj/`

Do not treat weather JSON or runtime cache files as journal entries. They can
explain the day environment if Jarad asks for that context.

## Search Patterns

Use `rg --files` or `find` to discover sources. Useful filters:

- `timeline/**/<YYYY-MM-DD>-day/<YYYY-MM-DD>-day.md`
- `timeline/**/<YYYY-MM-DD>-day/source/*journal*.md`
- `timeline/**/<YYYY-MM-DD>-day/source/*context-sweep*`
- `timeline/**/<YYYY-MM-DD>-day/source/*old-dot*`

For a theme search, search first, then read surrounding source files:

- `rg -n "<theme words>" /Users/jaradjohnson/Dot/timeline`
- `rg -n "<theme words>" /Users/jaradjohnson/Developer/ai-hub/Dot`

If a search path does not exist, note it briefly only when it affects coverage.
Do not fail the reflection because an old legacy path has already been retired.

## Source Priority

1. User-authored raw journal/source files in the requested date/range.
2. Journal sections inside day markdown files.
3. Nearby day logs and Dot synthesis for context.
4. Migrated context-sweep journal files.
5. Old Dot read-only references, if they still exist.
6. Runtime/cache files only as supporting context.

