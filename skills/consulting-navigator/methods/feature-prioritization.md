# Feature Prioritization
## Purpose
Rank product features or initiatives by scored impact, effort, and confidence so capacity is allocated to highest-value work. A transparent score and capacity cut-line turns an argument-driven backlog into an ordered set of deliberate trade-offs.
## Use
- Ranking a backlog or roadmap candidates by impact, effort, and confidence.
- Defending cut/keep decisions under capacity constraints.
- Translating research and strategy into an ordered build sequence.
## Avoid
- You need satisfaction-type categories (must/performance/delighter) first—use kano-model then score.
- You only have vague ideas with no impact or effort estimates—gather evidence via jobs-to-be-done or voice-of-the-customer first.
- The question is multi-horizon portfolio strategy across businesses—use portfolio-strategy-analysis or three-horizons-of-growth.
## Inputs
**Must-have:**
- Candidate features or initiatives with clear definitions.
- Impact estimates (reach, revenue, retention, or strategic value).
- Effort or cost estimates and confidence levels.
- Capacity or sequencing constraints for the planning horizon.

**Nice-to-have:** dependency map, customer-research evidence, technical-risk notes, and outcome metrics from similar releases.

**When data is thin:** lower confidence instead of pretending impact is known; reserve discovery work as a candidate rather than smuggling it into a build estimate.
## Procedure
1. **Normalize candidates.** Write each feature as a discrete user or business outcome with a scope boundary; split oversized concepts until a team can estimate and sequence them. Output: candidate backlog.
2. **Choose scoring logic.** Define reach, impact, confidence, and effort units for the planning period. For RICE, calculate score as reach times impact times confidence divided by effort, but adapt only with explicit approval. Output: scoring rubric.
3. **Estimate from evidence.** Assign reach from eligible users, impact from a declared outcome mechanism, confidence from evidence strength, and effort from the delivery team. Preserve ranges or disagreement instead of forcing a false single number. Output: evidence-backed score sheet.
4. **Rank and challenge.** Calculate scores, inspect outliers, and invite product, design, engineering, and commercial challengers to test assumptions. Re-score only when new evidence changes an input. Output: challenged ranking.
5. **Apply feasibility constraints.** Place dependencies, regulatory commitments, architectural enablers, and team capacity against the rank. Make exceptions visible rather than quietly overriding the order. Output: feasible build stack and cut-line.
6. **Publish decisions and refresh triggers.** State what is funded, deferred, or retired, why, and what event will trigger review. Output: decision log and next review date.
## Output Contract
An ordered feature list with candidate definitions, the scoring rubric, reach-impact-confidence-effort inputs, source or assumption for each input, calculated scores, capacity cut-line, dependencies, approved exceptions, and review triggers. It must show why one item beats another and what has deliberately not been funded.
## Evidence
Instrumented usage, experiments, and completed delivery estimates are observed evidence. Forecasted reach, monetization, and strategic uplift are assumptions unless tested. Confidence reflects quality of evidence, not stakeholder seniority. Keep separate scores for alternatives when their target user or outcome differs; a broad feature should not win simply because its reach is undefined.
## Checks
- Candidate scope is comparable enough that effort and impact are meaningful.
- Each score has units, time window, and an evidence or assumption label.
- Confidence reduces scores where data is weak rather than being ignored.
- Capacity is applied after ranking and exceptions are documented.
- The funded set has an outcome measure, not merely a release date.
## Failure Modes
- Calling every roadmap item P0 and then bypassing the ranking.
- Giving high impact to a feature with no identified user or outcome mechanism.
- Comparing a two-day experiment with a six-month platform rewrite as if their scope were equal.
- Allowing a senior stakeholder’s preference to overwrite a score without recording an exception.
- Never revisiting a rank after an experiment disproves its estimate.
