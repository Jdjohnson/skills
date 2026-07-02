# Desktop Packet

Use this node when direct placement cannot place a ChatGPT order safely, or
the user explicitly asks for the manual packet/copy-paste method. This is the
fallback path, not the first preference.

## Required Behavior

- Create a fresh Desktop folder named
  `~/Desktop/chatgpt-<lane>-<slug>-packet-YYYY-MM-DD[-N]` for each
  fallback/manual ChatGPT order.
- Put only `PROMPT.md` plus uploadable local files at the packet root.
- `PROMPT.md` must exactly match the final `Copy/paste order` block.
- The upload-file cap is `20` local files. `PROMPT.md` does not count against
  that cap.
- Keep URLs, IDs, short notes, and other non-file context in the response or
  prompt instead of inventing support files.
- If more than `20` local upload files are candidates, keep the first `20` in
  priority order and name the omitted files in the response.

## Build Steps

1. Finalize the lane, slug, prompt text, and ordered upload-file list.
2. Write the exact prompt text to a temporary file.
3. Run:

```bash
python3 .dot-addons/jarad-pack/skills/jj-chatgpt/scripts/build_desktop_packet.py --lane <lane> --slug <slug> --prompt-file <temp-prompt> [files...]
```

4. Use the script output to fill the `Desktop packet` section with the absolute
   folder path, included upload files, and any omitted files.

## Response Rules

- Add `Required ChatGPT connectors/apps` to the live response only.
- Use required-only semantics and say `None` when no connector or app must be
  enabled.
- In `Files/context to include`, local uploadable files should match the packet
  contents exactly, while non-file context should stay clearly separate.
- In `Execution path`, say `Desktop packet` and give the concrete reason direct
  placement was not used.
