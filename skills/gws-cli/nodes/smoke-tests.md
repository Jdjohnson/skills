# Google Workspace CLI Smoke Tests

Default smoke tests are read-only. Never print tokens or credential-file contents.

## Local checks

```bash
gws auth status
python3 <skill-root>/scripts/google_gmail.py --help
python3 <skill-root>/scripts/google_calendar.py --help
python3 <skill-root>/scripts/google_drive.py --help
python3 <skill-root>/scripts/google_sheets_read.py --help
python3 <skill-root>/scripts/google_token_export.py --help
python3 <skill-root>/scripts/google_token_from_adc.py --help
```

All help commands must exit successfully without contacting Google.

## Optional live reads

Run only when live verification is requested and authentication is configured:

```bash
python3 <skill-root>/scripts/google_drive.py search --page-size 3
python3 <skill-root>/scripts/google_calendar.py events --max-results 3 --single-events
python3 <skill-root>/scripts/google_gmail.py search --max-results 3
```

Do not run write, send, archive, label, create, update, move, permission, or token-export operations in the default smoke path.
