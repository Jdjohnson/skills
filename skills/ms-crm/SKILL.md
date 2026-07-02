---
name: ms-crm
description: Create new MSCRM deals with a mandatory Jarad Johnson approval packet and Slack notification. Use when adding a new sales lead, opportunity, or CRM deal to MSCRM from Dot; do not use for CRM updates, deletes, bulk sync, or general pipeline reporting.
---

# MSCRM New Deal Creation

Use this skill only for creating a new MSCRM deal. Do not update, delete, bulk import, or sync CRM records with this skill.

## Required Flow

1. Collect the new-deal details in a JSON file.
2. Run preview mode only:

```bash
node .dot-skills/ms-crm/scripts/create-deal.mjs preview --input /path/to/deal.json
```

3. Present the approval packet to Jarad Johnson, including the `approval_id`, deal fields, company behavior, contact/note behavior, duplicate warnings, and Slack route. Make clear that creating the CRM deal also sends the required Slack notification.
4. Stop unless Jarad explicitly approves the presented packet. Approval may be either the exact packet text or natural language that clearly approves the current packet, such as `approved`, `this is approved`, `create it`, `go ahead`, `post it to Slack`, or `add it to MSCRM`:

```text
I approve creating MSCRM deal <approval_id>
```

If multiple approval packets are pending or the approval could refer to something else, ask which packet Jarad means before creating anything.

5. If approved, run create mode with the saved packet and Jarad's approval text as written:

```bash
node .dot-skills/ms-crm/scripts/create-deal.mjs create \
  --packet /path/to/approval-packet.json \
  --approved-by "Jarad Johnson" \
  --approval-text "<Jarad's approval text>"
```

6. Report approval status, CRM creation status, Slack notification status, created IDs/URL, and any blocker.

## Non-Negotiable Rules

- Never create/post a new MSCRM deal without explicit approval from Jarad Johnson after the approval packet has been presented.
- Natural language approval is allowed when it clearly approves the current packet. Do not treat unrelated acknowledgement, brainstorming, or ambiguous discussion as approval.
- If more than one packet is pending, natural language approval is not enough; ask Jarad to identify the packet or use the exact packet approval text.
- Never bypass `SLACK_DEAL_WEBHOOK_URL`. Create mode must block before the CRM insert if the Slack webhook is not configured.
- Trigger Slack only after successful CRM creation/readback.
- Do not log credentials, webhook URLs, Supabase keys, or sensitive internal notes.

## Deal JSON

Required fields:

```json
{
  "dealName": "AI Inquiry + Quote Readiness POC",
  "companyName": "Positronic",
  "stage": "discovery",
  "divisionName": "MSAI",
  "sourceName": "REFERRAL",
  "sourceDetail": "JMARK referral",
  "ownerEmail": "jarad.johnson@mostlyserious.io"
}
```

Optional fields:

- `companyId`
- `createCompany`: set to `true` only when the approval packet should allow creating the company if no match exists.
- `valueMin`, `valueMax`, `expectedCloseDate`
- `primaryContact`: `{ "name": "...", "email": "...", "phone": "...", "title": "..." }`
- `note`: initial deal note body

## Output Expectations

Preview mode writes a canonical approval packet as JSON to stdout. Save it before asking for approval.

Create mode writes a concise JSON receipt to stdout:

- `approval.status`
- `crm.status`
- `crm.dealId`
- `crm.dealUrl`
- `slack.status`
- `errors` or `blockers`
