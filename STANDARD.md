# Skill standard

Every skill is a complete folder at `skills/<name>/`.

- `SKILL.md` starts with `name` and `description`; the name matches the folder.
- The description says what the skill does and when it applies.
- Keep the entrypoint short. Put conditional detail in linked references.
- Add scripts only when deterministic execution improves the work.
- Keep tests only for executable behavior or important safety invariants. Do not
  test generated wording, headings, or prompt snapshots.
- Include no credentials, personal paths, generated caches, or unfinished
  placeholders.
- Preserve the whole package when publishing or installing it.

Run `python3 scripts/validate.py` and `bash scripts/test.sh` before release.
