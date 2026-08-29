# Visibility and Updates

The latest update in the coordinator task should always answer three questions:

1. What does the research currently say?
2. What meaningfully changed?
3. What is being investigated next?

Use this order:

## Executive summary

Write a short current synthesis for a decision-maker. State the bottom line first. Include meaningful uncertainty, but do not narrate internal process.

## What changed

Summarize only new findings, corrections, weakened assumptions, resolved
contradictions, or meaningful blockers. Explain research through outcomes:

> The pricing evidence weakened the original revenue assumption. The
> child-safety sources identified an age-verification decision that must be
> resolved before architecture.

Do not expose raw tool output or source dumps. Do not use internal terms such as
packet, receipt, reconciliation, escalation stage, binding generation, progress
gate, event cursor, or runtime boundary.

## What comes next

Name the next few questions and why they matter. Make clear that nothing else
will run until the user says `continue`.

Before posting an update, rewrite `executive-summary.md` so the file and the task say the same thing.

For a brief in-flight note, do not repeat the full three-part update. Use:

> **Executive summary:** [current bottom line]. This pass is checking: [active question].

This keeps the latest visible message understandable without adding another layer of reporting.
