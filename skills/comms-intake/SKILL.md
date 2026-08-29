---
name: comms-intake
description: Triage a configured local queue of normalized email, SMS, or other message captures. Refresh copy-only producers, preserve freshness uncertainty, review actionable items, archive handled source files, and return a receipt without touching the original inboxes.
---

# Comms Intake

Triage local message captures without becoming a general inbox-cleanup or work-execution workflow.

## Configuration

Resolve these values from the workspace's instructions or adapter:

- active local queue;
- ordered copy-only refresh producers;
- handled, deferred, and receipt destinations;
- durable route for approved local briefs or logs;
- any explicitly authorized quiet-filing rules.

If the queue or lifecycle destinations are unresolved, stop before moving files. A missing optional producer reduces freshness but does not invalidate existing local captures.

## Workflow

Read [workflow](nodes/workflow.md), then use [queue](nodes/queue.md), [item](nodes/item.md), and [record](nodes/record.md) as needed.

Core invariants:

- Refresh producers may copy into the local queue; they never send, archive, edit, or delete at the source.
- After refresh attempts, the configured local queue is the source of truth for this pass.
- Producer failure never proves its source was empty. Preserve existing captures and report reduced freshness.
- Classify all active captures before review. Quiet-file only categories the workspace explicitly pre-authorizes; otherwise bring the item forward.
- Review one item at a time and keep source-message, local-capture, filed, review, deferred, and remaining counts distinct.
- Intake may create approved local briefs or drafts. It does not execute the resulting work or authorize outbound actions.
- Move handled and deferred captures to their configured local archives; never delete source files.
- Finish with a concise receipt.

Outbound sends, publishing, account mutations, and work in another system require separate authority for the exact action.
