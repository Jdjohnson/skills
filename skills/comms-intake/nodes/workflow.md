# Workflow

1. Create a unique run receipt and update it throughout the pass.
2. Run configured copy-only refresh producers in their declared order. Validate each producer's documented success schema; record failure without broadening scope or retrying against other sources.
3. Read the active local queue once. Capture path, source metadata, sender, time, routing hints, original reference, useful excerpt, and batch size when present. Flag malformed captures instead of discarding them.
4. Classify every capture before presenting the queue. Apply only explicit quiet-filing policy.
5. Show counts and a scan-friendly preview using [queue](queue.md). Then handle one item at a time using [item](item.md).
6. After each terminal outcome, update the receipt and move the local source to handled or deferred storage using [record](record.md).
7. Continue until the queue is empty or the user stops after the current item.

When an item becomes real work, end intake and hand off a bounded packet containing the original ask, sources, context, ambiguity, acceptance checks, allowed and forbidden actions, write route, and required tools. The receiving task obtains any further authority; intake does not execute it.
