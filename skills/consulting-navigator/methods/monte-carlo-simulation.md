# Monte Carlo Simulation
## Purpose
Propagate input uncertainty through a quantitative model by repeated random sampling, producing a distribution of outcomes rather than a single point estimate. The job: answer "What is the chance we hit cost, schedule, margin, or service targets?" when multiple uncertain drivers interact—probabilities instead of false precision.
## Use
- Inputs are uncertain, the model is multi-variable, and you need a full outcome distribution (NPV, duration, capacity, cost).
- Executives ask for the probability of hitting a threshold, not only a mean or base case.
- Risks interact, so one-at-a-time sensitivity or a single tornado chart is insufficient.
- Options must be compared under joint uncertainty that deterministic scenarios cannot quantify.
## Avoid
- Uncertainty is deep and meaningful probabilities cannot be assigned—use scenario planning.
- You only need one-factor or tornado sensitivity on a stable model—use sensitivity analysis.
- Model structure or data quality is too weak to justify distributions—repair the model first.
- The decision reduces to a few discrete branches better handled by a decision tree.
## Inputs
**Must-have:** a quantitative model linking inputs to the decision KPI; probability distributions or justified ranges for uncertain inputs; decision thresholds; a trial count sufficient for stable results.
**Nice-to-have:** correlation structure where material; historical calibration data; alternative model structures.
Document the rationale for judgment-based distributions and test sensitivity to their shape; do not invent narrow distributions to look scientific.
## Procedure
1. **Establish the mathematical model.** Define the KPI and the deterministic mapping from inputs to it. Output: model equation or workbook structure.
2. **Assign input distributions.** Give each uncertain input a distribution grounded in data or expert judgment; note material correlations. Output: input distribution table.
3. **Set trial count and sampling plan.** Choose trial count M and sampling approach so the output distribution is stable. Output: simulation design.
4. **Run repeated random sampling.** Draw inputs, evaluate the model each trial, store outcomes. Output: raw trial results.
5. **Form the output distribution and decision metrics.** Compute the central estimate, spread, coverage interval, and probability of meeting thresholds; compare options if relevant. Output: probabilistic forecast package.
## Output Contract
A forecast package containing: (1) model definition and KPI, (2) input distributions and correlation assumptions, (3) trial count and method notes, (4) outcome distribution (histogram or equivalent), (5) central estimate and uncertainty measures, (6) probabilities of crossing decision thresholds, (7) limitations. It must support a go / no-go, contingency, or option-ranking decision—not merely a prettier base case.
## Evidence
Treat historical data as observed, fitted distributions as inferred, expert ranges as assumptions, and missing correlation as an unknown that may bias results. When evidence is thin, widen distributions and report bands rather than claiming unsupported precision. Never present one percentile as "the answer" without the full distribution. If the model cannot represent a known risk pathway, fix the structure before simulating.
## Checks
- Model validated on a deterministic base case before random sampling.
- Every material input has an explicit distribution, not a hidden fixed value.
- Correlations stated where dependence is material, or their omission justified.
- Trial count sufficient for stable threshold probabilities at the precision claimed.
- Results include P(hit target) or coverage intervals, not only the mean.
- Limitations and judgment-based inputs disclosed to decision makers.
## Failure Modes
- Monte Carlo theater: sampling over a broken or incomplete model.
- False precision from overly narrow input distributions.
- Ignoring dependence among inputs—real "best cases" move together.
- Reporting only the mean when the decision hinges on tail risk.
- Treating software defaults as a substitute for model and distribution design.
