# Supply Chain Risk Management
## Purpose
Identify, score, and mitigate supply chain disruption risks across suppliers, nodes, and logistics paths. It creates a maintained operating view of exposure and response, rather than a one-time network-resilience diagnosis.
## Use
- Identifying, scoring, and mitigating end-to-end supply chain disruption risks
- Building multi-tier visibility and response playbooks for critical materials and nodes
- Prioritizing investments in dual source, inventory, and continuity controls
## Avoid
- You need product design failure modes on a component—use fmea
- The question is enterprise-wide risk appetite and board reporting—use enterprise-risk-management or iso-31000
- You need structural resilience redesign of the network after risk ID—pair with supply-chain-resilience-analysis or logistics-network-design
## Inputs
**Must-have:** Bill of materials and critical node map for products and lanes; supplier concentration, lead times, and single-source exposures; historical disruption and near-miss data; risk appetite, service commitments, and recovery time objectives; existing continuity, insurance, and inventory buffers.
## Procedure
1. **Trace the flow to the decision point.** Connect finished goods to components, tier-one suppliers, known upstream sites, plants, warehouses, and transport lanes. Flag a node wherever several products converge.
2. **Describe disruption scenarios.** For each critical node, state the event, trigger, exposed demand, time to detect, and plausible consequence. Separate a supplier insolvency from a port closure even when both delay the same part.
3. **Score inherent exposure.** Rate likelihood, operational impact, customer impact, financial impact, and recovery time on defined scales. Record concentration and substitutability alongside the score so a low-frequency, line-stopping event is visible.
4. **Design and cost treatments.** Compare qualified second source, inventory buffer, alternate lane, supplier recovery plan, contractual protection, and demand allocation. Assign an accountable owner, activation trigger, and residual score to each chosen control.
5. **Install monitoring and response.** Put leading indicators such as supplier liquidity alerts, on-time delivery deterioration, border delay, or inventory days against each material scenario. Specify who convenes, what is decided, and which playbook starts at each threshold.
## Output Contract
A supply-chain risk register with a node-and-lane exposure map, scenario-level inherent and residual ratings, owners, early-warning indicators, funded mitigation actions, and response playbooks. Each record must identify the affected material or flow, the time until customer service is threatened, and the decision required when an indicator trips. It is not a generic corporate register or a redesigned network blueprint.
## Evidence
Treat purchase history, shipment events, supplier confirmations, and inventory records as observed evidence. Label a sub-tier relationship, recovery estimate, or alternate-source capacity as inferred unless it has been validated directly. State assumptions behind scoring scales and demand allocation; score uncertainty separately when it could change priority. A supplier's assurance that capacity exists is not proof of qualified capacity at the required specification.
## Checks
- Reconcile critical materials and sites to the current bill of materials and sourcing records.
- Test whether one disruption can create correlated failures across products, suppliers, or lanes.
- Ensure every high residual exposure has an owner, trigger, and time-bound treatment decision.
- Run one tabletop response for the highest-ranked scenario and correct unusable escalation steps.
## Failure Modes
- Treating tier-one supplier questionnaires as visibility into upstream foundries or raw materials.
- Scoring a sole source as safe because it has never failed, while ignoring its replacement lead time.
- Counting the same alternate supplier as mitigation for several simultaneous shortages without reserving capacity.
- Leaving risk scores untouched after a supplier merger, geopolitical event, or product redesign changes exposure.
