# Local Guardrails

Use these controls before selecting a ChatGPT lane.

## Dot Workspace Setup

- Read `AGENTS.md`, `ASSISTANT.md`, `MEMORY.md`, and
  `ROUTES.md` when normal Dot work is required.
- Read `resources/profile/PROFILE.md` when
  collaboration defaults, the user's role, communication style, or personal context
  matter.
- Keep installed Dot workspace files, Dot Core source, add-ons, personal skills,
  and `dot-runtime/` proof/cache separate.
- For durable writes, follow `ROUTES.md`; do not guess a write location.

## Interaction Gates

- Draft before any outbound send, publish, calendar invite, external post, or
  external mutation.
- Sending or external mutation requires explicit approval.
- Do not create new credentials, approve payments, grant new connector scopes,
  or authorize sensitive permissions while placing a ChatGPT order.
- Ask one targeted question only when the missing answer changes the route or
  mutation boundary.

## Output Discipline

- Start with the useful answer, not process narration.
- Use plain English and keep the response easy to scan.
- Preserve confidence boundaries: facts, interpretation, recommendation, and
  unknowns should not collapse into one blob.
- Do not paste long raw ChatGPT output back to the user unless they ask for the raw
  record. Summarize, extract, and route.
