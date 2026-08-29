# Root Cause Analysis
## Purpose
Identify and evidence-validate the underlying cause chain of a defined operational problem so fixes address the true driver, not symptoms. Starting from a realized failure, it establishes what condition must change to prevent recurrence.
## Use
- A recurrent defect, incident, or performance gap needs a validated underlying cause before solution design
- Multiple plausible causes exist and must be structured and tested against evidence
- Leaders will only fund fixes once the true cause chain is clear
## Avoid
- You already know the cause and need prevention design—use poka-yoke or fmea for control planning
- The need is predictive risk ranking of potential failures before they occur—use fmea
- The problem is unstructured strategic ambiguity rather than an operational failure mode—use issue-tree or hypothesis-driven-problem-solving
## Inputs
**Must-have:**
- Clear problem statement with defect definition, magnitude, and when/where it occurs
- Process map or event timeline around the failure
- Evidence from the process (data, samples, observations, maintenance logs)
- Cross-functional knowledge of methods, machines, materials, and people factors
- Criteria for what counts as a verified root cause vs a contributing factor

**Nice-to-have:** retained samples, comparable non-failure cases, control-chart data, and a safe setting for direct observation.

**When data is thin:** preserve the competing hypotheses, collect the next discriminating observation, and avoid declaring an individual error to be the cause.
## Procedure
1. Define the defect precisely: what failed, how often, where, when, and against what standard. Freeze the statement before collecting explanations.
2. Reconstruct the event timeline and conditions for failure and non-failure cases. Protect logs, settings, and samples that may distinguish causes.
3. Generate candidate causal paths with people closest to the work, using a fishbone across method, machine, material, measurement, environment, and people. This generates hypotheses, not proof.
4. Use five-whys only while each link is supported by a mechanism and evidence. Stop at a controllable condition explaining recurrence, not “operator error.”
5. Test leading paths with data, observation, comparison samples, or a controlled change. Eliminate explanations contradicted by timing or evidence, and separate contributing conditions from the necessary driver.
6. Write the verified cause statement, evidence chain, confidence, and scope of applicability. Recommend a corrective action test and a recurrence metric, then hand control design to the next method.
## Output Contract
Produce a diagnosis pack containing the defect definition, process boundary, timeline, candidate-cause diagram, evidence log, rejected hypotheses, verified causal chain, contributing conditions, confidence, and the causation test. The root-cause statement must connect a controllable condition to the observed defect and state its scope. Include corrective-action experiments, but do not present a prospective RPN table as the diagnosis.
## Evidence
Tag samples, timestamps, settings, and direct observations as observed. Mark a causal link inferred until a test, comparison, or mechanism validates it. State missing data and changed operating conditions. Interview testimony generates hypotheses but does not verify a root cause, especially where blame affects recall.
## Checks
- The defect has a measurable baseline and an explicit time/place boundary.
- Timeline evidence supports the proposed sequence of causes.
- At least one discriminating test separates the leading explanation from alternatives.
- The root cause is a system condition that can be changed, not a personality label.
- Contributing factors are not mislabeled as the sole cause.
## Failure Modes
- Beginning with a favored explanation and arranging the fishbone to confirm it.
- Stopping the why-chain at training or attention instead of examining the condition that made error likely.
- Combining failures from different process states into one causal story.
- Destroying samples or overwriting logs before the timeline is reconstructed.
- Declaring success after a short-term patch without measuring recurrence.
