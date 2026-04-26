# Fallback Order Packet

Use this node when direct ChatGPT placement is unavailable, blocked, unsafe, or explicitly not wanted.

## Required Behavior

- Always provide the copy/paste order in chat.
- Create a fallback packet only when local file upload handoff would help.
- Put only `PROMPT.md` plus uploadable local files at the packet root.
- `PROMPT.md` must exactly match the final `Copy/paste order` block.
- The upload-file cap is `20` local files. `PROMPT.md` does not count against that cap.
- Keep URLs, IDs, short notes, connector requirements, and non-file context in the response or prompt instead of inventing support files.
- If more than `20` local upload files are candidates, keep the first `20` in priority order and name omitted files in the response.

## Build Steps

1. Finalize the lane, slug, prompt text, and ordered upload-file list.
2. Write the exact prompt text to a temporary prompt file.
3. Run:
   ```bash
   python3 skills/chatgpt/scripts/build_desktop_packet.py --lane <lane> --slug <slug> --prompt-file <temp-prompt> [files...]
   ```
4. Use the script output to fill the `Fallback packet` section with the folder path, included upload files, and omitted files.

## Response Rules

- Add `Required ChatGPT connectors/apps` to the live response only.
- Use required-only semantics and say `None` when no connector or app must be enabled.
- In `Files/context to include`, local uploadable files should match the packet contents exactly, while non-file context stays separate.
- In `Execution path`, say `Fallback order/packet` and give the concrete reason direct placement was not used.
