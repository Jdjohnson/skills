# CRISP-DM
## Purpose
Structure a data-mining engagement through business understanding, data prep, modeling, evaluation, and deployment phases. Its iterative phase logic keeps a technically plausible model tied to a decision and usable in operations.
## Use
- Standing up or governing an analytics/data-mining engagement from problem to deployment
- Teams need a shared lifecycle with explicit business understanding and evaluation gates
- You must plan data preparation, modeling, and rollout as one managed effort
## Avoid
- The need is general software delivery governance rather than data mining—use sdlc-methodology
- You only need a one-off hypothesis structure, not a full mining lifecycle—use hypothesis-driven-problem-solving
- Production ML operations and monitoring are the core problem—use mlops-lifecycle
## Inputs
**Must-have:**
- Business objectives and success criteria for the analytics effort
- Inventory of available data sources, quality, and access constraints
- Modeling and evaluation criteria tied to business KPIs
- Resource plan for data prep, modeling, and deployment stakeholders
- Decision rights for go/no-go between CRISP-DM phases

**Nice-to-have:** prior model results, data lineage, deployment constraints, adoption owners, and a baseline process performance measure.

**When data is thin:** end data understanding with a feasibility decision; do not promise a model before coverage, labels, and access have been inspected.
## Procedure
1. **Establish business understanding.** Convert the sponsor’s objective into a data-mining problem, success criteria, constraints, and project plan. Output: business objective and analytic success definition.
2. **Conduct data understanding.** Acquire initial data, describe fields and granularity, explore distributions, and verify data quality. Output: data description and quality findings.
3. **Prepare the modeling dataset.** Select records, clean defects, construct features, integrate sources, and document the repeatable preparation pipeline. Output: modeling dataset and preparation specification.
4. **Model iteratively.** Choose techniques compatible with the objective and data, configure experiments, and compare candidate models against the agreed criteria. Output: candidate model results.
5. **Evaluate in business context.** Test model quality, leakage, bias, operational feasibility, and whether the original objective has been met; return to an earlier phase when it has not. Output: go/no-go evaluation.
6. **Plan deployment.** Define how results enter decisions or processes, who maintains them, what is monitored, and how lessons are reviewed. Output: deployment and monitoring plan.
## Output Contract
A phase-artifact package containing the business objective, data description, preparation specification, modeling experiments, evaluation decision, and deployment plan. It must preserve the links between business success, model metrics, and operational use. A notebook or model score without its preparation and evaluation trail is incomplete.
## Evidence
Record source-system extracts, missingness, label definitions, transformations, and split dates as observed facts. State assumptions about target definition, future data availability, and decision behavior. Keep exploratory findings separate from validated model performance. If historical data leaks information unavailable at decision time, remove it even if accuracy declines.
## Checks
- Business success criteria are measurable and not replaced by a convenient technical metric.
- Training, validation, and test treatment respects time and entity leakage.
- Feature construction can be reproduced from documented inputs.
- Evaluation includes operational cost of false positives and false negatives.
- Deployment has an owner, refresh logic, monitoring signal, and retirement condition.
## Failure Modes
- Starting with an algorithm before defining the decision it will improve.
- Cleaning data differently in experimentation and deployment.
- Declaring a high validation score successful despite target leakage.
- Stopping at a model artifact with no user, workflow, or monitoring plan.
