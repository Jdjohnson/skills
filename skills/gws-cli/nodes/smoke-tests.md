# Smoke Tests

Keep live checks read-only and never print credentials.

## Unit tests

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s <skill-root>/tests -p 'test_*.py' -v
```

## Offline help

Run every script with `--help`; each must import and exit successfully without contacting Google.

## Optional live reads

When live access is authorized, run only the smallest useful checks:

```bash
python3 <skill-root>/scripts/google_gmail.py profile
python3 <skill-root>/scripts/google_gmail.py search "in:inbox" --max-results 3
python3 <skill-root>/scripts/google_drive.py search --page-size 3
python3 <skill-root>/scripts/google_calendar.py events --max-results 3 --single-events
```

Confirm the intended account from the profile response. Do not put account-specific expectations in the package. Mutation and credential-bootstrap commands are outside the default smoke path.
