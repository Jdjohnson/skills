# GWS CLI Smoke Tests

Read-only verification for the migrated `gws-cli` personal skill. Run from the
Dot workspace root. Do not print tokens or credential file contents.

## Prerequisites

- `gws` installed and on `PATH`
- Canonical token bundle at `~/.config/gws/token_full.json` (never copy into Dot)

## 1. Auth Status

```bash
gws auth status
```

Pass: command exits 0 and reports authenticated state without dumping secrets.

Fail: missing token, insufficient scopes, or auth errors — follow re-auth steps in
`google_oauth.py` error output (do not print `token_full.json`).

## 2. Wrapper Help

Each script must import and print help without contacting Google:

```bash
python3 .dot-skills/gws-cli/scripts/google_gmail.py --help
python3 .dot-skills/gws-cli/scripts/google_calendar.py --help
python3 .dot-skills/gws-cli/scripts/google_drive.py --help
python3 .dot-skills/gws-cli/scripts/google_sheets_read.py --help
python3 .dot-skills/gws-cli/scripts/google_token_export.py --help
python3 .dot-skills/gws-cli/scripts/google_token_from_adc.py --help
```

Pass: all exit 0.

## 3. Drive Read

```bash
python3 .dot-skills/gws-cli/scripts/google_drive.py search --page-size 3
```

Pass: JSON listing of recent Drive files (may be empty). Read-only.

## 4. Calendar Read

```bash
python3 .dot-skills/gws-cli/scripts/google_calendar.py events --max-results 3 --single-events
```

Pass: JSON event list for primary calendar. Read-only.

## 5. Gmail Read

```bash
python3 .dot-skills/gws-cli/scripts/google_gmail.py search --max-results 3
```

Pass: JSON message summaries. Read-only.

## Out of Scope for Default Smoke

Do not run these in the default smoke path without explicit user approval:

- `google_gmail.py draft`, `archive`, `modify-labels`
- `google_drive.py create-native`
- `gws sheets spreadsheets values update` or any other write/mutation
- `google_token_export.py` without `--help` — every execution mode prints an
  access token (`shell` default, `json`, and `token`). Use only
  `google_token_export.py --help` in the default smoke path.
