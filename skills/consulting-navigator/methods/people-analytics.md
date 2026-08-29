# People Analytics
## Purpose
Apply data science and HR metrics to diagnose drivers of talent outcomes and produce evidence-backed people insights. The work connects a business question to responsible analysis and a practical intervention, rather than producing a dashboard of disconnected HR measures.
## Use
- Talent outcomes need causal or correlational explanation from data
- Leadership wants quantified drivers of attrition, engagement, or performance
- Prioritizing people investments with evidence rather than anecdote
## Avoid
- You lack basic clean HR and performance data—fix HR systems and definitions first
- The question is qualitative culture diagnosis without numbers—use culture-assessment or employee-engagement-surveying
- You need a forward workforce capacity plan rather than explanatory insight—use workforce-planning
## Inputs
**Must-have:** Clean HRIS data (tenure, role, level, location, manager); outcome data (attrition, performance, promotion, engagement); clear analytic question and success definition; privacy, legal, and ethical constraints for people data; business context for interpretation by segment.

**Nice-to-have:** Job architecture history, compensation ranges, learning activity, manager changes, employee listening data, and an ethics review partner.

**When data is thin:** Begin with a descriptive cohort analysis and a data-quality repair plan; do not fit a predictive model whose missing fields track a protected group or a business unit.
## Procedure
1. **Frame the decision question.** Define the talent outcome, affected population, intervention decision, time horizon, and what a useful answer would change. Output: analytic charter.
2. **Govern and prepare the data.** Confirm permitted use, minimize personal fields, create a data dictionary, check joins and missingness, and define the population at risk. Output: approved analysis dataset.
3. **Explore patterns and segments.** Examine rates and distributions by relevant role, tenure, location, manager, and time cohorts before modeling. Output: descriptive findings and candidate drivers.
4. **Test driver relationships.** Choose an interpretable analytical approach, examine confounders and stability, and distinguish association from a credible causal claim. Output: driver analysis with uncertainty.
5. **Translate and evaluate action.** Recommend a targeted intervention, fairness guardrails, expected measure, and follow-up design that tests whether the action improved the outcome. Output: decision brief and measurement plan.
## Output Contract
Provide a people insight brief with the business question, population definition, data lineage, descriptive patterns, model or analysis logic, driver evidence, uncertainty, fairness considerations, and a targeted action hypothesis. The brief identifies who benefits, who may be disadvantaged, and how leadership will evaluate the intervention; it is not a ranking of employees for automated treatment.
## Evidence
Use only authorized fields and restrict individual-level access to the smallest necessary group. Report denominator, observation period, and missing-data treatment for every rate. Separate correlations from causal evidence and do not infer intent from behavioral traces. Test material results across relevant groups; if sample size makes a fairness comparison unreliable, state that limit rather than calling the result neutral.
## Checks
- The outcome and population at risk are defined before variables are selected.
- Data joins, duplicate records, and missingness are checked before interpreting patterns.
- A high-performing model is rejected if it cannot be explained or used lawfully for the decision.
- Segment findings include uncertainty and avoid exposing identifiable small groups.
- Recommended action has a counterfactual or before-after evaluation design, not just a correlation story.
## Failure Modes
- Using a manager rating as ground truth when ratings vary systematically by team or level.
- Training an attrition model on past resignations and then treating its score as a reason to deny opportunities.
- Finding a tenure correlation and claiming that tenure itself causes departures.
- Publishing a small-group dashboard that reveals sensitive outcomes to managers without a legitimate need.
