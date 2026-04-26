---
description: Optional file output rules for brief artifacts.
---

## File Output

Save a brief only when the user asks or provides a destination.

If the user asks for a file but gives no path, ask for the destination or use the host's normal artifact mechanism if one exists.

## Rules

- Do not overwrite an existing file without confirmation.
- Use Markdown unless the user requests another format.
- Keep the same required section headers in the saved file.
- Do not create tasks, send messages, or update external systems unless explicitly asked.
