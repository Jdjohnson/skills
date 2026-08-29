# SCOR Model
## Purpose
Frame the end-to-end supply chain with a standard process, metrics, and best-practice reference architecture for diagnosis and design. It gives disparate functions a common hierarchy and performance vocabulary before detailed redesign begins.
## Use
- Establishing a standard process and metrics architecture for the end-to-end supply chain
- Benchmarking performance and diagnosing which process areas drive gaps
- Scoping transformation so Plan-Source-Make-Deliver-Return workstreams share one map
## Avoid
- You already have process maps and need shop-floor waste removal—use value-stream-mapping
- The need is a single category sourcing strategy—use strategic-sourcing or kraljic-matrix
- You need risk mitigation plans rather than a reference framework—use supply-chain-risk-management
## Inputs
**Must-have:** Scope of products, channels, and geographies in the supply chain; current process inventory across plan, source, make, deliver, and return; existing KPIs and data availability for reliability, responsiveness, cost, and asset metrics; stakeholder agreement on process boundaries and ownership.

**Nice-to-have:** external benchmark ranges, partner interfaces, product complexity segments, and prior improvement initiatives.

**When data is thin:** map the process hierarchy and metric ownership first; do not invent cross-site comparisons when definitions or clocks differ.
## Procedure
1. **Set the chain boundary.** Select products, channels, geographies, customer promise point, and partner interfaces. State where the chain starts and ends so procurement, manufacturing, logistics, and returns are all applying the same scope.
2. **Classify work in the reference hierarchy.** Map current activities into the standard Plan, Source, Make, Deliver, Return, and Enable structure at the level needed for diagnosis. Mark variants by product, site, and channel rather than forcing false uniformity.
3. **Define performance attributes and metrics.** Choose measures for reliability, responsiveness, agility, cost, and asset use. Write the calculation, data owner, grain, clock, and target for each; a metric without a consistent numerator and denominator is not comparable.
4. **Assess gaps and interactions.** Compare current process capability and metric performance with the desired operating model or credible benchmark. Trace trade-offs: reducing inventory may impair reliability, while expedited freight may mask a sourcing problem.
5. **Prioritize design changes.** Build a gap register that links process changes, enabling capabilities, KPI changes, owners, and sequence. Use it to select deeper analyses, not as a substitute for them.
## Output Contract
Deliver a measurement framework and reference architecture showing the scoped supply-chain hierarchy, process ownership, selected metrics and definitions, performance gaps, and prioritized improvement themes. The result must let teams compare like with like and see which process level requires a detailed intervention.
## Evidence
Classifications and metric definitions are controlled design choices; document them. Use transaction records for measured KPI values and label external benchmarks by scope and maturity. Never combine lead-time, cost, or service figures from different channel definitions without normalization. Where partner data is unavailable, identify the blind spot instead of assigning it an internal proxy.
## Checks
- Every material flow has a mapped owner and a process classification.
- Metric definitions include unit, time window, data source, and accountable steward.
- Reliability, speed, cost, and asset measures expose their trade-offs.
- Site and channel comparisons use compatible boundaries.
- The gap register directs teams to a decision or a next-level analysis.
## Failure Modes
- Labeling a local warehouse flow as end-to-end while excluding suppliers and returns.
- Publishing a dashboard of metrics that no process owner can change.
- Comparing order-cycle time across channels with different order-start events.
- Treating a reference taxonomy as proof that the actual workflow is understood.
- Pursuing lowest cost while service penalties remain outside the scorecard.
