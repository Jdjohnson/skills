# Quality Function Deployment
## Purpose
Translate weighted customer requirements into technical characteristics and design targets via a structured requirements-to-specifications matrix. It makes trade-offs explicit by showing which design choices contribute most to customer value.
## Use
- You must translate prioritized customer requirements into technical characteristics, process controls, and design targets
- Cross-functional teams disagree on which specs deliver customer value
- A new or redesigned product/service needs a traceable requirements-to-design matrix
## Avoid
- You do not yet know what customers want—use voice-of-the-customer, jobs-to-be-done, or kano-model first
- You only need to rank a backlog of known features—use feature-prioritization
- The problem is post-launch defect root cause, not requirements translation—use root-cause-analysis
## Inputs
**Must-have:** Structured customer requirements (Whats) with importance weights; competitive or baseline performance on those requirements where available; candidate technical characteristics (Hows) controllable by design or process; correlation judgments between Whats and Hows from cross-functional experts; constraints on cost, technology, and regulatory limits.

**Nice-to-have:** engineering benchmark data, achievable tolerance ranges, design failure modes, supplier capability, and prototype-test results.

**When data is thin:** limit the matrix to the most important requirements, separate tentative relationships from validated ones, and use a prototype plan to test the technical characteristics with highest weighted uncertainty.
## Procedure
1. **Prepare the customer requirements.** De-duplicate and clarify the Whats in customer language, assign importance weights, and retain the segment or use context. Do not let engineering rewrite a need into a preferred solution.
2. **Select measurable Hows.** Identify technical characteristics the team can influence: dimensions, response time, material property, error rate, or process capability. Define units and direction of improvement for each one.
3. **Build the relationship matrix.** For every What–How pair, have experts score the relationship as strong, medium, weak, or none, with a rationale. Compute each How’s weighted priority from customer importance and relationship strength.
4. **Create the roof.** Mark positive and negative correlations among Hows. Surface design conflicts, such as a faster response that raises energy use, before teams independently optimize incompatible targets.
5. **Benchmark and set targets.** Compare customer perception and technical performance with alternatives where evidence exists. Convert the highest-priority Hows into numeric targets, limits, and verification methods while honoring cost and regulatory constraints.
6. **Deploy and maintain traceability.** Assign each target to design, process, or supplier owners; flow the relevant relationships into downstream specifications and test plans; revise the matrix when customer weights or feasible technology change.
## Output Contract
A House of Quality or equivalent matrix containing weighted customer Whats, measurable technical Hows, relationship scores and rationales, correlation roof, baseline comparison, weighted technical priorities, targets, constraints, owners, and verification methods. It must trace a design target back to customer value, not simply rank features.
## Evidence
Customer weights and benchmark results must retain the segment and collection method. Relationship scores are expert judgments, so record participants and disagreements rather than presenting them as measurements. A target is an engineering commitment only after feasibility evidence supports it. Do not multiply arbitrary scores into a precise-looking rank without sensitivity testing the weights.
## Checks
- Every What is expressed as a customer outcome rather than a technical solution.
- Every How is controllable, measurable, and has a defined direction of improvement.
- Relationship ratings have a documented basis and include cross-functional input.
- The roof identifies material trade-offs before targets are approved.
- High-priority Hows receive targets and verification methods, not just large scores.
## Failure Modes
- Filling the left side with feature requests that already dictate the technical answer.
- Using relationship scores from one function and calling the result customer-led.
- Ignoring a negative roof correlation until prototype testing exposes the conflict.
- Setting an aggressive target without checking manufacturing or supplier capability.
- Treating the matrix as a one-time workshop artifact after requirements change.
