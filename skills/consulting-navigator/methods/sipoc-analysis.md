# SIPOC Analysis
## Purpose
Define process improvement scope by naming suppliers, inputs, high-level steps, outputs, and customers on one page.
## Use
- Scoping a process improvement effort before detailed mapping or DMAIC.
- Aligning stakeholders on suppliers, inputs, outputs, and customers of a process.
- Establishing a common high-level process definition for cross-functional teams.
## Avoid
- You already need timed material and information flow with waste callouts—use value-stream-mapping.
- The need is a detailed step-level workflow with decision logic—use process-mapping.
- You are mapping multi-layer service delivery roles and customer visibility—use service-blueprinting.
## Inputs
**Must-have:** Named process and business purpose; known or hypothesized process start and end events; list of major process steps at a high level (typically 4–7); suppliers and inputs for the process; customers and outputs the process must deliver.

**Nice-to-have:** Existing procedures, customer requirements, defect records, and representatives from upstream and downstream teams.

**When data is thin:** Draft the table in a working session, mark uncertain cells, and validate only the boundary and major outputs before investigating detail.
## Procedure
1. State the process name, trigger, and end event in plain language. Choose one product or service family; a map that starts with “customer request” and ends with “customer happy” is too broad.
2. Write four to seven verb-noun process steps across the center row from left to right. Keep them at the same altitude, such as receive order, verify credit, pick goods, ship order, and confirm delivery.
3. Work rightward to identify outputs from each process as a whole, then name the internal or external customers that receive, use, or regulate those outputs.
4. Work leftward to identify the inputs required to create those outputs, including information, material, approvals, and specifications. Name the supplying role or system for each material input.
5. Review the complete table with suppliers and customers. Circle disputed boundaries, requirements, or ownership; these become the opening questions for detailed diagnosis.
6. Publish the one-page scope with exclusions and a short problem statement. Do not add timings, decision diamonds, or root causes until a subsequent method needs them.
## Output Contract
Produce a single-page SIPOC table with a named process, explicit start and end points, four to seven high-level process steps, suppliers, inputs, outputs, customers, scope exclusions, and unresolved boundary questions. The artifact must let a cross-functional team agree what process is being improved and who is affected. It is a framing device, not evidence of a detailed current-state workflow or a defect analysis.
## Evidence
Use contracts, specifications, system records, and observation to confirm inputs and outputs where available. Identify workshop claims as provisional, particularly customer requirements asserted by an upstream team. Do not list a department as a customer unless it receives a usable output. When several products follow different routes, document the chosen family and create separate tables rather than hiding variation in a long process row.
## Checks
- Steps are verbs at a consistent level of detail.
- Each named output has at least one customer.
- Inputs are things the process consumes or needs, not activities.
- The start and end points rule out adjacent processes.
- The central row has enough detail to orient work but not more than seven steps.
## Failure Modes
- Starting with suppliers and producing a procurement inventory instead of a process boundary.
- Putting “quality” in the output column without a deliverable or recipient.
- Listing every substep until the table becomes a process map.
- Calling an internal approval a customer when it is actually an input constraint.
