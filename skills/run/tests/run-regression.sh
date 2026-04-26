#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
RUNNER="${REPO_ROOT}/skills/run/scripts/run.sh"
WORK_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/run-workflow-regression.XXXXXX")"

PASS_COUNT=0
FAIL_COUNT=0

cleanup() {
  rm -rf "${WORK_ROOT}"
}
trap cleanup EXIT

note() {
  printf '%s\n' "$*"
}

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  note "ok - $1"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  note "not ok - $1"
  return 1
}

assert_contains() {
  local path="$1"
  local pattern="$2"
  local label="$3"
  grep -Fq -- "$pattern" "$path" || fail "$label"
}

assert_file_exists() {
  local path="$1"
  local label="$2"
  [[ -e "$path" ]] || fail "$label"
}

create_stub_bin() {
  local dir="$1"
  mkdir -p "$dir"

  cat > "${dir}/tool-stub" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

extract_prompt() {
  local prev=""
  local arg
  for arg in "$@"; do
    if [[ "$prev" == "-p" ]]; then
      printf '%s' "$arg"
      return 0
    fi
    prev="$arg"
  done
  printf '%s' "${!#:-}"
}

prompt="$(extract_prompt "$@")"

if [[ "$prompt" == *"RUNNER_STUB_FAIL"* ]]; then
  echo "Simulated runner failure" >&2
  exit 7
fi

if [[ "$prompt" == *"Reply with OK only."* ]]; then
  echo "OK"
  exit 0
fi

echo "Stub success"
EOF

  chmod +x "${dir}/tool-stub"
  ln -sf "${dir}/tool-stub" "${dir}/claude"
  ln -sf "${dir}/tool-stub" "${dir}/codex"
  ln -sf "${dir}/tool-stub" "${dir}/gemini"
}

write_blueprint() {
  local dest="$1"
  local tool="$2"
  mkdir -p "$dest"
  python3 - "$dest" "$tool" <<'PY'
from pathlib import Path
import json
import sys

dest = Path(sys.argv[1])
tool = sys.argv[2]
data = {
    "name": "portable-run",
    "goal": "Verify the portable run runner.",
    "created": "2026-04-02T12:00:00Z",
    "context": "Use the tool stub and create a single handoff artifact.",
    "defaults": {
        "tool": tool,
        "timeout": 30,
        "max_retries": 0
    },
    "steps": [
        {
            "id": "step-01",
            "title": "Do the thing",
            "detail": "Complete the task. RUNNER_STUB_SUCCESS",
            "done_when": "The step is marked done and a handoff note exists.",
            "status": "pending"
        }
    ]
}
(dest / "blueprint.json").write_text(json.dumps(data, indent=2) + "\n")
PY
}

run_runner() {
  local stub_dir="$1"
  shift
  PATH="${stub_dir}:$PATH" "$RUNNER" "$@"
}

test_validate_and_run() {
  local stub_dir run_dir
  stub_dir="${WORK_ROOT}/bin-basic"
  run_dir="${WORK_ROOT}/basic/runs/demo"
  create_stub_bin "$stub_dir"
  write_blueprint "$run_dir" "claude-code"

  run_runner "$stub_dir" --validate "${run_dir}/blueprint.json" >/dev/null
  run_runner "$stub_dir" --launch-mode standard "${run_dir}/blueprint.json" >/dev/null

  assert_file_exists "${run_dir}/progress.md" "progress log should exist"
  assert_file_exists "${run_dir}/handoff/step-01.md" "handoff should exist"
  assert_file_exists "${run_dir}/completion-summary.txt" "completion summary should exist"
  assert_contains "${run_dir}/completion-summary.txt" "Completed Cleanly" "summary should report clean completion"
  pass "validate and standard run"
}

test_status_surface() {
  local stub_dir run_dir status_out
  stub_dir="${WORK_ROOT}/bin-status"
  run_dir="${WORK_ROOT}/status/runs/demo"
  status_out="${WORK_ROOT}/status-output.txt"
  create_stub_bin "$stub_dir"
  write_blueprint "$run_dir" "claude-code"

  run_runner "$stub_dir" --launch-mode standard "${run_dir}/blueprint.json" >/dev/null
  run_runner "$stub_dir" --status "${run_dir}/blueprint.json" >"${status_out}"

  assert_contains "${status_out}" "Completed Cleanly" "status should show terminal outcome"
  assert_contains "${status_out}" "Inspect next:" "status should include inspect hint"
  pass "status surface"
}

test_external_skill_resolution() {
  local stub_dir run_dir extra_root
  stub_dir="${WORK_ROOT}/bin-skill"
  run_dir="${WORK_ROOT}/skill/runs/demo"
  extra_root="${WORK_ROOT}/extra-skills"
  create_stub_bin "$stub_dir"
  mkdir -p "${extra_root}/research-brief"
  cat > "${extra_root}/research-brief/SKILL.md" <<'EOF'
---
name: research-brief
description: Minimal test skill
allowed-tools:
  - Read
  - Bash
---

# research-brief

Do the work.
EOF

  mkdir -p "$run_dir"
  python3 - "$run_dir" <<'PY'
from pathlib import Path
import json
import sys

dest = Path(sys.argv[1])
data = {
    "name": "portable-run-workflow-skill-step",
    "goal": "Verify installed skill lookup.",
    "created": "2026-04-02T12:00:00Z",
    "context": "Resolve a skill from RUN_WORKFLOW_PATHS.",
    "defaults": {
        "tool": "claude-code",
        "skill_runner": "claude-code"
    },
    "steps": [
        {
            "id": "step-01",
            "title": "Use external skill",
            "detail": "Use the skill. RUNNER_STUB_SUCCESS",
            "done_when": "The step is marked done.",
            "tool": "skill:research-brief",
            "status": "pending"
        }
    ]
}
(dest / "blueprint.json").write_text(json.dumps(data, indent=2) + "\n")
PY

  RUN_WORKFLOW_PATHS="${extra_root}" run_runner "$stub_dir" --launch-mode standard "${run_dir}/blueprint.json" >/dev/null
  assert_file_exists "${run_dir}/handoff/step-01.md" "skill-based run should produce handoff"
  pass "external skill resolution"
}

test_legacy_skill_path_alias() {
  local stub_dir run_dir extra_root
  stub_dir="${WORK_ROOT}/bin-legacy-skill-paths"
  run_dir="${WORK_ROOT}/legacy-skill-paths/runs/demo"
  extra_root="${WORK_ROOT}/legacy-extra-skills"
  create_stub_bin "$stub_dir"
  mkdir -p "${extra_root}/research-brief"
  cat > "${extra_root}/research-brief/SKILL.md" <<'EOF'
---
name: research-brief
description: Minimal test skill
allowed-tools:
  - Read
  - Bash
---

# research-brief

Do the work.
EOF

  mkdir -p "$run_dir"
  python3 - "$run_dir" <<'PY'
from pathlib import Path
import json
import sys

dest = Path(sys.argv[1])
data = {
    "name": "portable-run-workflow-legacy-skill-path-alias",
    "goal": "Verify legacy skill path alias lookup.",
    "created": "2026-04-02T12:00:00Z",
    "context": "Resolve a skill from legacy RUN_SKILL_PATHS.",
    "defaults": {
        "tool": "claude-code",
        "skill_runner": "claude-code"
    },
    "steps": [
        {
            "id": "step-01",
            "title": "Use external skill via legacy alias",
            "detail": "Use the skill. RUNNER_STUB_SUCCESS",
            "done_when": "The step is marked done.",
            "tool": "skill:research-brief",
            "status": "pending"
        }
    ]
}
(dest / "blueprint.json").write_text(json.dumps(data, indent=2) + "\n")
PY

  RUN_SKILL_PATHS="${extra_root}" run_runner "$stub_dir" --launch-mode standard "${run_dir}/blueprint.json" >/dev/null
  assert_file_exists "${run_dir}/handoff/step-01.md" "legacy skill path alias should still produce handoff"
  pass "legacy skill path alias"
}

test_workflow_skill_path_precedence() {
  local stub_dir run_dir workflow_root legacy_root
  stub_dir="${WORK_ROOT}/bin-workflow-path-precedence"
  run_dir="${WORK_ROOT}/workflow-path-precedence/runs/demo"
  workflow_root="${WORK_ROOT}/workflow-precedence-skills"
  legacy_root="${WORK_ROOT}/legacy-precedence-skills"
  create_stub_bin "$stub_dir"
  mkdir -p "${workflow_root}/research-brief"
  cat > "${workflow_root}/research-brief/SKILL.md" <<'EOF'
---
name: research-brief
description: Minimal test skill
allowed-tools:
  - Read
  - Bash
---

# research-brief

Do the work.
EOF

  mkdir -p "$run_dir"
  python3 - "$run_dir" <<'PY'
from pathlib import Path
import json
import sys

dest = Path(sys.argv[1])
data = {
    "name": "portable-run-workflow-path-precedence",
    "goal": "Verify RUN_WORKFLOW_PATHS takes precedence over RUN_SKILL_PATHS.",
    "created": "2026-04-02T12:00:00Z",
    "context": "Resolve a skill from RUN_WORKFLOW_PATHS when both vars are set.",
    "defaults": {
        "tool": "claude-code",
        "skill_runner": "claude-code"
    },
    "steps": [
        {
            "id": "step-01",
            "title": "Use external skill via precedence rule",
            "detail": "Use the skill. RUNNER_STUB_SUCCESS",
            "done_when": "The step is marked done.",
            "tool": "skill:research-brief",
            "status": "pending"
        }
    ]
}
(dest / "blueprint.json").write_text(json.dumps(data, indent=2) + "\n")
PY

  RUN_WORKFLOW_PATHS="${workflow_root}" RUN_SKILL_PATHS="${legacy_root}" run_runner "$stub_dir" --launch-mode standard "${run_dir}/blueprint.json" >/dev/null
  assert_file_exists "${run_dir}/handoff/step-01.md" "workflow skill path should win when both env vars are set"
  pass "workflow skill path precedence"
}

test_validate_and_run
test_status_surface
test_external_skill_resolution
test_legacy_skill_path_alias
test_workflow_skill_path_precedence

note ""
note "Passed: ${PASS_COUNT}"
note "Failed: ${FAIL_COUNT}"
[[ "${FAIL_COUNT}" -eq 0 ]]
