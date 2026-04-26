# ChatGPT Pro Review Order

Use this lane when a hard question, draft, architecture, or decision would benefit from a second pass, prep pass, or hardening review and there is time for it.

Read [[../references/chatgpt-handoffs.md]] and adapt the Pro review template into the following user-facing shape:

## Required Output Shape

`ChatGPT Pro Review Order`

`Why this lane`
- 1-3 bullets on why another model pass is worth it here

`Files/context to include`
- exact artifacts, files, excerpts, or constraints the user should provide

`Copy/paste order`
- a fenced markdown block using the Pro review template from `references/chatgpt-handoffs.md`
- include artifact/question under review, review mode, stress-test angles, and what a good answer should do

`What to bring back`
- best recommendation
- strongest objections
- specific changes the local agent should make
- residual risks
- source material / evidence appendix
- full raw response when possible

## Guardrails

- Do not use Pro review when immediate execution matters more than extra thinking.
- Keep the order concrete and adversarial enough to produce a real counterweight, not generic agreement.
