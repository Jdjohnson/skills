# AI Ethics & Governance
## Purpose
Design enforceable ethical rules, roles, and controls so AI systems are fair, transparent, and accountable in production. It turns broad principles into lifecycle decisions, evidence, escalation, and ownership for each use case.
## Use
- Establishing accountable AI decision rules before models reach production
- Designing approval gates, fairness, transparency, and human-oversight controls
- Aligning legal, risk, product, and data-science owners around model risk
## Avoid
- You only need a prioritized list of AI use cases—use ai-strategy-and-roadmap
- The issue is pure cyber control design without AI-specific decision risk—use cybersecurity-framework
- You need enterprise IT governance across all systems, not AI model risk—use cobit
## Inputs
**Must-have:** Inventory of AI/ML use cases by risk tier and data sensitivity; existing privacy, security, and model-risk policies; stakeholder map of legal, risk, product, and data-science owners; regulatory or industry constraints relevant to automated decisions.

**Nice-to-have:** Model cards, data lineage, incident history, impact assessments, and performance or drift monitoring.

**When data is thin:** Prohibit irreversible automated decisions until the missing impact evidence is collected; establish a temporary human-review control rather than assigning a falsely low risk tier.
## Procedure
1. **Inventory and tier use cases.** Record the decision affected, affected people, data types, model role, deployment status, and potential harm. Separate drafting assistance from eligibility, pricing, hiring, or safety decisions.
2. **Map harms and obligations.** For each tier, identify fairness, privacy, security, explainability, reliability, contestability, and human-oversight concerns, plus relevant legal or policy obligations.
3. **Set governance roles and decision gates.** Define who may approve development, pilot, production, material changes, and retirement. Give product, model risk, legal, and operational owners distinct accountabilities.
4. **Specify controls and evidence.** Attach tests, documentation, threshold criteria, access controls, human review, notices, monitoring, and incident response to the identified risk. A policy statement alone is not a control.
5. **Assess residual risk and decide.** Record inherent risk, control effectiveness, residual risk, exceptions, sign-offs, and escalation. Reject, constrain, or approve use cases based on stated appetite.
6. **Operate the register.** Review incidents, performance changes, complaints, and control evidence on a defined cadence; trigger reassessment when data, model, audience, or use changes.
## Output Contract
Deliver a governance structure and control register that lists each use case, risk tier, impacted population, harm scenarios, owners, approval gates, required controls, evidence artifacts, residual-risk decision, monitoring metric, review date, and escalation route. It must enable a real approval or stop decision for a system, not offer an aspirational ethics charter.
## Evidence
System logs, test results, data lineage, user notices, and incident records are observed. Risk ratings and harm likelihood are judgments that must name their assessor and rationale. Do not use aggregate model accuracy as evidence that outcomes are fair across affected groups. Where demographic testing is infeasible or inappropriate, document the limitation and substitute a justified monitoring approach.
## Checks
- Every production use case has an accountable business owner and control owner.
- Higher-impact decisions have stricter approval and evidence requirements.
- Controls cover the actual model, data, and decision context, not only a generic policy.
- Exception approvals expire and have compensating controls.
- Monitoring includes a route for users or operators to raise harms.
## Failure Modes
- Publishing principles without translating them into release gates and test evidence.
- Assigning a low tier because a model is technically simple while its decision consequence is high.
- Treating human review as meaningful when reviewers lack authority, time, or an escalation path.
- Testing performance before launch but ignoring drift, complaints, and changed use after launch.
