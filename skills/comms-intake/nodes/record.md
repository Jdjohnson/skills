# Record and Archive

The run receipt records, for each capture:

- source metadata and original local path;
- the five review fields;
- user response or authorized filing rule;
- outcome, action, destination, pending approval, and archive path;
- producer status and any freshness uncertainty.

Move handled and deferred files to separate configured local archives. Preserve filenames; on collision, add the run timestamp. Never delete a local source capture.

Deferred items include a reason and review date and leave the active queue. Quiet-filed items include their durable destination and the applied rule.

Close with counts for handled, completed locally, filed, pending approval, deferred, and remaining, plus one freshness line when needed.
