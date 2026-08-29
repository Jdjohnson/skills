# Service Blueprinting
## Purpose
Decompose end-to-end service delivery into customer, frontstage, backstage, and support layers to expose handoff failures and redesign points.
## Use
- Designing or diagnosing a multi-touch service that spans customer, frontstage, and backstage work.
- Exposing failure points and wait times that pure customer journey maps hide.
- Aligning operations, IT, and CX on a single delivery architecture before process redesign.
## Avoid
- The problem is purely manufacturing material flow with no customer interaction—use value-stream-mapping.
- You only need a high-level process boundary, not layered delivery roles—use sipoc-analysis.
- You need emotional experience moments without operational wiring—use customer-journey-mapping.
## Inputs
**Must-have:** Defined service offering and customer segment or scenario; observed or documented customer actions across touchpoints; frontstage employee actions and scripts for the same episodes; backstage processes, systems, and support roles that enable delivery; evidence of wait times, failure points, or recovery steps.

**Nice-to-have:** Call recordings, service-level data, policy exceptions, and an event log linking customer contacts to operational work.

**When data is thin:** Mark lanes or links as hypothesized and validate them in short observation sessions with frontline staff and customers.
## Procedure
1. Select one representative service episode with a clear trigger and completion condition, such as a customer changing a delivery address. Avoid combining several customer types on the first map.
2. Lay out customer actions chronologically, including waits, self-service attempts, contact points, and visible outcomes. Put the moments of truth on the timeline.
3. Add frontstage actions directly below each customer action: staff conversation, portal response, notification, or physical interaction. Draw the line of interaction between the two lanes.
4. Add backstage work beneath the line of visibility: verification, fulfillment, case handling, approvals, and system updates. Add support processes, vendors, data stores, and rules that enable each backstage step.
5. Trace handoffs vertically and identify fail points, rework loops, queues, and recovery actions. Measure elapsed time and ownership at the troublesome links rather than averaging the whole journey.
6. Redesign the selected links and publish both current and target blueprints with changes, controls, and validation measures.
## Output Contract
Provide a layered current-state and target-state diagram for one scoped service episode. It must show customer actions, frontstage actions, backstage actions, support processes, the line of visibility, dependencies, failure points, recovery paths, and owners. Attach a ranked redesign list with the observed evidence and intended service effect. The artifact must make an invisible operational dependency visible; it is not only an emotional journey map or a single-lane flowchart.
## Evidence
Observe actual episodes where possible and record dates, channels, and customer segment. Distinguish a written procedure from work as performed. Label inferred backstage steps when systems or vendors cannot be observed. Do not infer customer emotion from a queue time alone; capture direct feedback separately. For sensitive cases, anonymize customer details while keeping the sequence and timing intact.
## Checks
- Every visible promise has a responsible frontstage or backstage action.
- The line of visibility separates what the customer can and cannot see.
- Handoffs name both sending and receiving roles.
- Failure points specify a recovery path instead of a red warning icon alone.
- Target changes preserve compliance, system, and capacity constraints.
## Failure Modes
- Mapping the happy path and excluding the exception that generates most contacts.
- Putting a backend database in the frontstage lane because staff use it.
- Treating a long customer wait as one delay without locating the queueing handoff.
- Designing a recovery email while leaving the underlying fulfillment error unchanged.
