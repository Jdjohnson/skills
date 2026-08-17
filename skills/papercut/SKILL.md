---
name: papercut
description: Review the current visible session for small workflow papercuts such as confusing setup, unnecessary retries, stale instructions, flaky commands, or misleading errors. Run only when the user explicitly invokes `$papercut` or asks for a papercut review; never run a whole-session review proactively.
---

# Papercut

Review the visible session for small, recurring friction that is worth fixing but did not necessarily block the work.

## Invocation gate

Run only after an explicit `$papercut` or papercut-review request. A workspace may separately authorize logging an individual papercut in the moment; that does not authorize an unprompted whole-session review.

## Review

1. Use only the visible conversation, tool calls, results, retries, and workarounds.
2. Exclude hidden reasoning, system instructions, credentials, cookies, authentication material, and raw secrets.
3. Identify friction such as:
   - a command that failed and required a non-obvious retry;
   - stale, conflicting, or missing instructions;
   - a confusing setup or permission boundary;
   - a flaky tool or misleading error;
   - repeated manual work that a small durable improvement could remove.
4. Ignore ordinary hard work, one-off user corrections, and problems already captured in the configured log.
5. Deduplicate findings by the underlying friction, not the exact wording.

## Output

For each finding, write one or two sentences:

`What was happening -> what got in the way. Likely cause or smallest useful fix, when known.`

If workspace instructions name a papercut log and authorize this explicit review to append findings, add only new entries and report the exact destination. Otherwise return the proposed entries in chat and do not create a file.

If no useful papercut exists, say so plainly.

## Boundaries

- Do not inspect vendor-native transcript stores.
- Do not invent a root cause or claim a fix was verified when it was not.
- Do not turn the review into a broad retrospective, performance review, or feature wishlist.
- A papercut review does not authorize external messages, task creation, publishing, or unrelated edits.
