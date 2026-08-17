# Continuity and Stop

## Pause or interruption

Stop the current pass and set `executive-summary.md` to `Paused`. Record:

- the current bottom line;
- what was completed;
- the next useful questions;
- any blocker that must be cleared.

Do not leave research running through a hidden shell, scheduler, detached
process, worker thread, or another task.

On re-entry after an interruption, treat a stale `Running` label as `Paused`
and reconcile the working artifacts before resuming.

## Resume

Prefer the task where research began. Read `brief.md`, `executive-summary.md`,
and `research-notes.md`; set status to `Running`; post the current summary;
then run only the next bounded pass.

Treat controller-backed projects as read-only legacy archives. For a legacy project containing `findings.md`, `sources.md`, `frontier.md`, `questions.md`, `research_log.md`, or `final_report.md`, read those files once and consolidate only their supported content into new `brief.md`, `executive-summary.md`, and `research-notes.md` files alongside them. Leave every legacy file untouched, including the underscore-named `final_report.md`. Do not restart the retired controller or runner.

## Stop

Stop means compile, not merely shut down:

1. Do not begin another research pass.
2. Reconcile findings and sources.
3. Set the summary status to `Stopped and compiled`.
4. Write `final-report.md`.
5. Return the bottom line and report link in the current task.

If there are no supported findings, the report must still include:

- a direct no-findings statement;
- what was attempted;
- why it did not produce supported findings;
- remaining questions;
- the most useful restart path.

If the user explicitly says to stop without compiling because they are taking over,
mark the work paused and do not create or overwrite a report.
