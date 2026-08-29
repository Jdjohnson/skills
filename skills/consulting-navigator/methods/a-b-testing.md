# A/B Testing
## Purpose
Compare two live variants of one intervention under randomized exposure to identify the statistically better performer. It uses observed behavior under control and treatment to support a causal choice, not stated preferences or a design review.
## Use
- You can randomly split comparable traffic or users across two variants of one change.
- A decision hinges on which of two concrete treatments drives a measurable outcome.
- You need a statistically defensible winner before scaling a change.
## Avoid
- You need to estimate willingness-to-pay across many attribute combinations—use conjoint-analysis.
- Traffic is too thin for significance in the decision window—use pilot-and-scale-methodology or expert judgment first.
- The question is exploratory preference language, not live performance—use focus-groups or survey-design-methodology.
## Inputs
**Must-have:** A single primary metric and secondary guardrail metrics; two fully specified variants differing on one controlled factor; random assignment mechanism and sample-size / power assumptions; exposure window long enough to capture the outcome behavior; instrumentation that records assignment, exposure, and conversion events.

**Nice-to-have:** Pre-experiment baseline, segment analysis plan, novelty-risk assessment, and a rollback mechanism.

**When data is thin:** Calculate the minimum detectable effect and either extend the test or decide that only a large effect could justify rollout.
## Procedure
1. **Write the decision and hypothesis.** Specify the exact change, primary outcome, acceptable downside, target population, and what result would cause rollout, hold, or reversal.
2. **Freeze the variants.** Create Control and Treatment that differ only in the intended factor. Verify that copy, eligibility, price, page speed, and tracking are otherwise equivalent.
3. **Plan assignment and sample.** Randomize at user, account, or session level as appropriate; prevent cross-over; calculate required sample from baseline rate, minimum meaningful lift, power, and false-positive threshold.
4. **Instrument and validate.** Log assignment before exposure, exposure before conversion, and guardrails such as errors, refund, or latency. Run an A/A check or pre-launch QA to detect broken randomization.
5. **Run without peeking-driven decisions.** Monitor safety and data quality, but respect the planned stopping rule. Pause only for material harm or instrumentation failure.
6. **Analyze the contrast.** Compare primary metric rates or means, estimate lift and uncertainty interval, assess guardrails, and inspect pre-specified segments cautiously. Decide whether the evidence clears the rollout rule.
## Output Contract
An experiment readout containing the decision, hypothesis, population, assignment unit, variants, planned sample and duration, exposure counts, primary result with lift and uncertainty, guardrail results, data-quality exceptions, and rollout recommendation. It must say whether a difference is both statistically credible and practically worthwhile.
## Evidence
Logged assignment, exposure, and outcome events are observed. Causal interpretation requires the assumption that randomization and instrumentation held. Treat post-hoc segment stories as exploratory unless planned in advance. Exclude records only with a pre-specified or documented technical reason. Never claim “no effect” merely because an underpowered test is inconclusive.
## Checks
- One primary metric is named before traffic is split.
- Assignment is random, persistent, and balanced across meaningful cohorts.
- The variants differ on one interpretable factor.
- Required sample and stopping rule were set before reading results.
- Guardrails prevent a conversion win from hiding customer or operational harm.
## Failure Modes
- Changing headline, price, and checkout flow together, making lift uninterpretable.
- Stopping after a favorable daily fluctuation.
- Randomizing sessions when users can encounter both variants repeatedly.
- Declaring a winner from a tiny sample with a wide uncertainty interval.
- Optimizing click-through while returns, support contacts, or latency worsen.
