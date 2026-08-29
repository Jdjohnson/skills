---
name: session-friction-review
description: Review the current visible session for small, non-blocking workflow friction and append validated, deduplicated findings through a configured local reviewer. Use only when explicitly invoked.
---

# Session Friction Review

Mine the current visible session for recurring friction without exposing hidden or secret material.

## Workflow

1. Resolve the workspace's configured review command, output log, temporary root, source harness/model label, and failed-trace retention no longer than 24 hours. If any required value is missing, stop without writing.
2. Reject symlinked or untrusted temporary roots. Create one unique run directory with mode `0700` and one Markdown trace with mode `0600`, containing only evidence needed for review, in order:
   - user messages;
   - assistant updates and final responses;
   - tool purpose, sanitized arguments, result, error, retry, and workaround.
3. Exclude hidden reasoning, system or developer instructions, credentials, cookies, authentication material, and raw secrets. Preserve useful private task context when it is safe and needed.
4. Run the configured reviewer once with the trace and source label. Do not substitute another reviewer or infer findings yourself after failure.
5. Accept success only when the command returns its documented valid result and confirms which deduplicated entries were appended. Report those entries or that none were found.
6. After confirmed success, delete the trace and empty run directory. On failure, preserve the trace only until the configured deadline; report its path, deletion deadline, and actionable error. Delete it immediately if private modes or bounded cleanup cannot be guaranteed.

## Boundaries

- Review only the visible session; never read vendor-native transcript stores.
- Record small workflow friction, not major bugs, accomplishments, tasks, or unsupported speculation.
- Invalid or failed review output must leave the log unchanged.
- This whole-session workflow is explicit-only. Separate workspace policy may still authorize logging an individual friction item when it occurs.
