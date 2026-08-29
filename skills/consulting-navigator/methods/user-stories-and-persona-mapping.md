# User Stories & Persona Mapping
## Purpose
Decompose researched user needs into persona-linked, testable user stories that drive development tasks. The mapping keeps each slice tied to a real context and a verifiable user outcome.
## Use
- Translating researched needs and personas into backlog-ready, testable user stories.
- Connecting who the user is to what gets built next in agile delivery.
- Creating a shared language among product, design, and engineering for incremental delivery.
## Avoid
- Personas and needs are not yet researched—use customer-persona-development, jobs-to-be-done, or voice-of-the-customer first.
- You need multi-horizon strategy, not delivery decomposition—use product-roadmap-development.
- The work is pure process redesign without a product backlog—use process-mapping or service-blueprinting.
## Inputs
**Must-have:** Persona or segment definitions grounded in research; user goals, pains, and context of use; product scope or epic themes to decompose; definition of ready/done and acceptance-criteria standards.

**Nice-to-have:** journey maps, usability evidence, analytics, accessibility needs, technical constraints, and support-ticket themes.

**When data is thin:** limit work to hypotheses marked for research validation; do not invent a persona’s motivations to fill a sprint.
## Procedure
1. **Frame the outcome and persona context.** Select an epic, the persona, their starting condition, and the outcome they seek. Tie the work to a research finding, journey moment, or measurable problem.
2. **Write outcome-oriented story candidates.** Express who needs to do what and why, while avoiding solution detail. Capture alternate personas, permissions, and failure paths separately rather than stuffing them into one oversized story.
3. **Add observable acceptance criteria.** Specify examples, rules, data, accessibility, and negative cases that prove the behavior works. Use concrete examples to align product, design, engineering, and QA.
4. **Slice vertically.** Split by workflow step, happy path, rules, persona, or data scope so each slice produces usable value and can be tested independently. Preserve traceability from slice to persona need.
5. **Refine and prioritize.** Check readiness with the delivery team, estimate uncertainty, identify dependencies, and order the backlog using user value, risk, learning, and release constraints.
## Output Contract
The backlog contains each persona-linked story, research trace, acceptance criteria, priority, dependency, sizing confidence, and definition-of-ready status. It includes a map from personas and journey moments to stories so neglected users are visible. It must be actionable for a sprint while retaining the customer outcome; it is not a set of UI tickets or an unranked wish list.
## Evidence
Research interviews, observed behavior, analytics, and validated journey findings are evidence. A proposed benefit, workflow preference, or edge case without evidence is a hypothesis and should have a validation step. State product-policy and technical constraints instead of disguising them as user needs. Do not use an archetype as a factual substitute for an individual user, and do not claim a story is accepted until its observable criteria are tested.
## Checks
- Every story names a persona and a meaningful outcome, not a screen control.
- Acceptance criteria include at least one success condition and one relevant exception.
- A story is independently demonstrable within the intended delivery increment.
- Splits preserve value rather than moving all usefulness into the final ticket.
- Priority reflects user impact and learning risk, with dependencies visible.
## Failure Modes
- Writing “build dashboard” with no actor or decision outcome.
- Treating a persona slide as proof of unresearched requirements.
- Combining three roles, six workflows, and every exception into one story.
- Accepting a ticket because the interface exists, though the user cannot complete the task.
- Prioritizing the loudest stakeholder’s feature above a critical journey failure.
