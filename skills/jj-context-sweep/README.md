# JJ Context Sweep

`jj-context-sweep` is a best-effort daily context collector. It helps an AI assistant gather the useful traces from a workday across email, Slack, Notion, CRM activity, and local Codex sessions, then write only the high-signal items into a markdown daily note.

The skill is meant for people who work across too many surfaces and want a durable end-of-day record without dumping every notification into their notes.

## What It Does

- Reads per-source checkpoints so each source can move forward independently.
- Gathers recent activity from supported tools when the current host exposes them.
- Keeps only context that is likely to matter later.
- Writes timestamped bullets into a `## Log` section.
- Uses hidden stable markers so reruns update existing bullets instead of duplicating them.
- Advances checkpoints only after a successful non-dry-run write.

## What It Does Not Do

- It does not assume a private assistant workspace, Obsidian, a private daily-note tree, or any specific workspace.
- It does not provide full Notion or CRM coverage unless the current host exposes connectors with enough data.
- It does not send messages, post updates, or mutate source systems. The only normal mutation is the markdown journal file and checkpoint state.

## Invocation

```text
jj-context-sweep
jj-context-sweep dry-run
jj-context-sweep since:2026-04-22T09:00:00-05:00
jj-context-sweep since:2026-04-22T09:00:00-05:00 dry-run
```

## Runtime Files

By default, the helper writes portable local state under the workspace root:

```text
.context-sweep/jj-context-sweep/state.json
.context-sweep/journal/YYYY-MM-DD.md
```

To use your own journal file:

```bash
python3 skills/jj-context-sweep/scripts/jj_context_sweep.py write \
  --root . \
  --journal-file path/to/today.md \
  --payload-file /tmp/context-sweep-payload.json
```

You can also set:

```bash
export CONTEXT_SWEEP_JOURNAL_FILE=path/to/today.md
export CONTEXT_SWEEP_JOURNAL_DIR=path/to/journal
```

Use `--state-path` if you want checkpoint state somewhere else.

## Helper Commands

Show state:

```bash
python3 skills/jj-context-sweep/scripts/jj_context_sweep.py state --root .
```

Initialize state:

```bash
python3 skills/jj-context-sweep/scripts/jj_context_sweep.py state --root . --init
```

Summarize local Codex sessions since a timestamp:

```bash
python3 skills/jj-context-sweep/scripts/jj_context_sweep.py codex \
  --since "2026-04-22T09:00:00-05:00"
```

Dry-run a write:

```bash
python3 skills/jj-context-sweep/scripts/jj_context_sweep.py write \
  --root . \
  --payload-file /tmp/context-sweep-payload.json \
  --dry-run
```

## Payload Shape

The assistant gathers and classifies source items, then passes a normalized payload to the helper:

```json
{
  "sources": {
    "superhuman": {
      "status": "success",
      "high_water": "2026-04-22T11:18:00-05:00",
      "note": "2 kept"
    },
    "crm": {
      "status": "skipped",
      "high_water": null,
      "note": "CRM connector unavailable in this session"
    }
  },
  "items": [
    {
      "source": "superhuman",
      "source_id": "18fabc123",
      "timestamp": "2026-04-22T10:30:00-05:00",
      "summary": "Sent work email to Andy re component wizard next steps."
    }
  ]
}
```

Valid sources are `superhuman`, `slack`, `notion`, `crm`, and `codex`.

## Testing

Run the unit tests from the repo root:

```bash
python3 -m unittest skills/jj-context-sweep/tests/test_jj_context_sweep.py
```
