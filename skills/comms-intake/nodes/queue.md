# Queue

## Refresh

Treat each configured producer as an independent copy-only adapter. Accept success only when its exit status and response match the adapter's documented contract. On missing configuration, permission failure, malformed output, or uncertain freshness:

- continue from already-local captures;
- record one clear freshness caveat;
- keep counts unknown rather than zero;
- never expand accounts, folders, dates, or permissions to compensate.

## Preview

Report source-message, local-capture, quiet-filed, and review-item counts separately. Count a capture by its recorded batch size when available, otherwise as one.

For each review item show only:

```text
Title: <short useful title>
Link: <original reference or "No link captured">
Overview: <summary from the local capture>
Relevance: <supported project, priority, relationship, or "No clear relevance inferred">
Suggestion: <one exact next step>
```

Do not browse or live-read the original provider while preparing the preview. Default ordering is pinned/owner, known sender, then unknown/noise; oldest first within each group. Use a different order only when the workspace defines one or the user asks.
