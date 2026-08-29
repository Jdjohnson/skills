# Cybersecurity Framework
## Purpose
Assess and target cyber risk reduction using a structured identify–protect–detect–respond–recover control framework. The framework turns technical control gaps into a business-risk profile and funded sequence of control improvements.
## Use
- Assessing and improving cyber risk management against a recognized control outcome model
- Building a current vs. target security profile and investment roadmap
- Aligning security, IT, and risk leadership on shared cyber language and priorities
## Avoid
- You need enterprise IT governance beyond security—use cobit
- The need is disaster recovery runbooks only—use disaster-recovery-planning or business-continuity-planning
- You are embedding security into CI/CD pipelines specifically—use devsecops-framework
## Inputs
**Must-have:** Asset, system, and data criticality inventory; Current security controls and known gaps or incidents; Threat and regulatory context for the organization; Risk appetite and resource constraints for remediation.

**Nice-to-have:** Penetration-test findings, vendor assessments, incident exercises, data-flow diagrams, and control evidence from audits.

**When data is thin:** Establish a preliminary profile for crown-jewel systems, record unverified control claims, and validate them through evidence sampling before reporting maturity.
## Procedure
1. **Set organizational scope and risk language.** Identify critical services, data, dependencies, legal obligations, and risk tolerance. Define the profile boundary so a corporate rating does not hide a weak business unit or cloud environment.
2. **Build the current profile.** Map existing practices and evidence against Govern, Identify, Protect, Detect, Respond, and Recover outcomes. Rate outcome achievement, not the existence of a policy document.
3. **Describe credible cyber scenarios.** Link material gaps to threat actors, attack paths, affected assets, business interruption, safety, or data consequences. Identify control dependencies and third parties.
4. **Define the target profile.** Select outcomes that materially reduce the stated scenarios within appetite. Specify required control capability, accountable executive, implementation evidence, and residual risk acceptance path.
5. **Prioritize the uplift portfolio.** Sequence measures by risk reduction, prerequisite, cost, operating burden, and time to deploy. Establish metrics and review cadence for exceptions and changing threats.
## Output Contract
A current and target profile showing outcome status, evidence, gap, scenario linkage, accountable owner, and remediation priority. The accompanying roadmap states investment, dependency, milestone, verification method, and residual-risk decision for each material gap. It must let leadership see cyber risk reduction, not just receive a list of security tools.
## Evidence
Treat configuration evidence, test results, incident records, and access reviews as observed. A control owner’s assertion is a claim until sampled. Document assumptions about asset completeness, threat likelihood, and vendor responsibility. Where recovery capability has not been exercised, call it unproven rather than effective.
## Checks
- Critical assets and business services are covered before low-value systems.
- Each profile rating cites evidence current enough for the operating environment.
- Gaps connect to a credible scenario and a control outcome, not a generic maturity score.
- Target outcomes fit risk appetite and regulatory obligations.
- Roadmap owners can operate the control after implementation, not only purchase it.
## Failure Modes
- Scoring every framework outcome equally while ignoring the internet-facing payment platform.
- Mistaking a written incident plan for demonstrated response capability.
- Assigning cloud-provider responsibilities that remain with the customer.
- Buying detection tooling before asset inventory and log coverage make detection usable.
