# Commands

Use `<skill-root>` as the installed `gws-cli` package path.

```bash
python3 <skill-root>/scripts/google_gmail.py profile
python3 <skill-root>/scripts/google_gmail.py search "in:inbox" --max-results 25
python3 <skill-root>/scripts/google_gmail.py thread <thread-id>
python3 <skill-root>/scripts/google_gmail.py count "in:inbox"

python3 <skill-root>/scripts/google_calendar.py calendars
python3 <skill-root>/scripts/google_calendar.py events --max-results 25 --single-events
python3 <skill-root>/scripts/google_calendar.py freebusy primary

python3 <skill-root>/scripts/google_drive.py search <term>
python3 <skill-root>/scripts/google_drive.py get <file-id-or-url>
python3 <skill-root>/scripts/google_sheets_read.py <sheet-id-or-url> --a1 "Sheet1!A1:C10"
```

## Gmail mutations

Create a threaded draft only with the real thread and message headers:

```bash
python3 <skill-root>/scripts/google_gmail.py draft \
  --to <recipient> --subject "Re: <subject>" --body <text> \
  --thread-id <thread-id> --in-reply-to '<message-id>' \
  --references '<references plus message-id>'
python3 <skill-root>/scripts/google_gmail.py draft-read <draft-id>
```

List real draft resources before sending or discarding; a message or thread ID is not a draft ID. Archive targets threads unless `--target message` is explicitly selected.

Use `gws --help` and service-level help for an uncovered operation. Do not guess API shapes.
