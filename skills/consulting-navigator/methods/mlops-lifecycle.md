# MLOps Lifecycle
## Purpose
Plan the end-to-end machine learning operations lifecycle so models can be deployed, monitored, retrained, and governed like production software. It manages the changing data, model, and decision behavior that ordinary software delivery controls do not cover.
## Use
- Production models lack reliable release, monitoring, retraining, or ownership practices
- Teams can train models but cannot reproduce or safely deploy them
- Model performance or data drift creates operational, regulatory, or customer risk
## Avoid
- You still need the AI opportunity portfolio and business case—use ai-strategy-and-roadmap first
- The work is classic analytics methodology without production ML systems—use crisp-dm
- You only need ethical policy without delivery lifecycle design—use ai-ethics-and-governance
## Inputs
**Must-have:** business decision and model use case; training and serving data sources; model performance and risk criteria; current deployment architecture; named owners for data, model, platform, and business outcomes.

**Nice-to-have:** feature-store capability, model registry, incident history, bias evaluations, and expected data refresh cadence.

**When data is thin:** begin with a model inventory and a reproducibility test on the highest-risk deployed model; avoid promising automated retraining before the data lineage is known.
## Procedure
1. **Inventory the decision system.** Map the business decision, prediction consumer, training data, feature transformations, model artifact, serving path, and human override. Establish accountable owners for each link.
2. **Make training reproducible.** Version code, data snapshots or references, feature definitions, parameters, environment, evaluation set, and approval record. A model should be rebuildable from a named run.
3. **Design release gates.** Define offline metrics, robustness and fairness checks, security review, latency limits, rollback conditions, and approval authority. Compare a candidate against the current champion before promotion.
4. **Operate the serving system.** Instrument request volume, feature freshness, schema failures, latency, prediction distribution, business outcomes, and overrides. Set alerts for drift and decision harm, not just server uptime.
5. **Close the retraining loop.** Specify who investigates alerts, how labels return, what triggers retraining, how a challenger is evaluated, and when a model must be retired. Rehearse rollback and incident communication.
## Output Contract
An MLOps operating design with a model inventory, lineage map, versioning standards, release-gate checklist, monitoring dashboard specification, alert thresholds, retraining policy, incident playbook, and RACI across data, platform, model, and business owners. It must cover the model after release, not stop at a deployment diagram.
## Evidence
Log model and data metrics with timestamps, population filters, and code versions. Separate data drift from performance drift; the latter requires delayed ground truth. Label proxy outcomes and model-risk thresholds as assumptions. Never claim a model has improved because offline accuracy rose when the serving population changed. Retain approval and rollback evidence for regulated or high-impact decisions.
## Checks
- A deployed prediction can be traced to a model version, features, and release approval.
- Training and serving transformations are tested for parity.
- Alerts distinguish pipeline outage, schema break, drift, and outcome degradation.
- A named owner can approve rollback outside business hours.
- Retraining has a validation gate, not an automatic overwrite of the incumbent.
## Failure Modes
- Versioning model code while leaving training data and feature logic mutable.
- Monitoring CPU use but not whether predictions harm decisions.
- Retraining on feedback contaminated by the model’s own prior recommendations.
- Promoting the best offline model despite unacceptable latency or subgroup behavior.
- Leaving a retired model in a hidden batch job after its owner departs.
