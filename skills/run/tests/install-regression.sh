#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
INSTALLER="${REPO_ROOT}/scripts/install.py"
WORK_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/run-workflow-install-regression.XXXXXX")"

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

assert_exists() {
  local path="$1"
  local label="$2"
  [[ -e "$path" ]] || fail "$label"
}

assert_missing() {
  local path="$1"
  local label="$2"
  [[ ! -e "$path" ]] || fail "$label"
}

assert_contains() {
  local path="$1"
  local pattern="$2"
  local label="$3"
  grep -Fq -- "$pattern" "$path" || fail "$label"
}

test_install_preserves_host_shared() {
  local home_dir stdout_path stderr_path help_primary help_legacy
  home_dir="${WORK_ROOT}/preserve-shared-home"
  stdout_path="${WORK_ROOT}/preserve-shared.stdout"
  stderr_path="${WORK_ROOT}/preserve-shared.stderr"
  help_primary="${WORK_ROOT}/preserve-shared.help.primary"
  help_legacy="${WORK_ROOT}/preserve-shared.help.legacy"

  mkdir -p "${home_dir}/.claude/skills/_shared"
  cat > "${home_dir}/.claude/skills/_shared/existing.txt" <<'EOF'
host shared content
EOF

  HOME="${home_dir}" python3 "${INSTALLER}" --host claude >"${stdout_path}" 2>"${stderr_path}"

  assert_exists "${home_dir}/.claude/skills/run/SKILL.md" "run planner should install for Claude"
  assert_exists "${home_dir}/.claude/skills/_shared/existing.txt" "existing shared skill content should remain"
  assert_contains "${home_dir}/.claude/skills/_shared/existing.txt" "host shared content" "existing shared content should remain unchanged"
  assert_exists "${home_dir}/.claude/commands/run.md" "Claude command wrapper should install"
  assert_exists "${home_dir}/.local/bin/run-workflow" "primary workflow runner should install"
  assert_exists "${home_dir}/.local/bin/run-skill" "runner shim should install"
  [[ -L "${home_dir}/.local/bin/run-workflow" ]] || fail "primary workflow runner should remain a symlink"
  [[ -L "${home_dir}/.local/bin/run-skill" ]] || fail "legacy runner alias should remain a symlink"
  "${home_dir}/.local/bin/run-workflow" --help >"${help_primary}"
  "${home_dir}/.local/bin/run-skill" --help >"${help_legacy}"
  assert_contains "${help_primary}" "run-workflow [options]" "primary runner help should advertise the canonical command"
  assert_contains "${help_legacy}" "run-workflow [options]" "legacy alias help should still advertise the canonical command"
  assert_contains "${help_legacy}" "run-skill remains supported as a legacy alias." "legacy alias help should explain compatibility"
  pass "install preserves host-level shared directory"
}

test_preflight_blocks_partial_install() {
  local home_dir stdout_path stderr_path rc
  home_dir="${WORK_ROOT}/preflight-home"
  stdout_path="${WORK_ROOT}/preflight.stdout"
  stderr_path="${WORK_ROOT}/preflight.stderr"

  mkdir -p "${home_dir}/.claude/commands"
  cat > "${home_dir}/.claude/commands/run.md" <<'EOF'
existing command wrapper
EOF

  rc=0
  if HOME="${home_dir}" python3 "${INSTALLER}" --host claude >"${stdout_path}" 2>"${stderr_path}"; then
    rc=0
  else
    rc=$?
  fi

  [[ "${rc}" -eq 1 ]] || fail "install should fail when command target exists"
  assert_missing "${home_dir}/.claude/skills/run" "run planner should not be installed after preflight failure"
  assert_missing "${home_dir}/.local/bin/run-workflow" "primary workflow runner should not be installed after preflight failure"
  assert_missing "${home_dir}/.local/bin/run-skill" "runner shim should not be installed after preflight failure"
  assert_contains "${stderr_path}" "Refusing to overwrite existing file" "preflight should report command wrapper conflict"
  pass "preflight prevents partial install"
}

test_install_is_idempotent_for_existing_run_paths() {
  local home_dir stdout_path stderr_path
  home_dir="${WORK_ROOT}/idempotent-home"
  stdout_path="${WORK_ROOT}/idempotent.stdout"
  stderr_path="${WORK_ROOT}/idempotent.stderr"

  HOME="${home_dir}" python3 "${INSTALLER}" --host both >/dev/null 2>/dev/null
  HOME="${home_dir}" python3 "${INSTALLER}" --host both >"${stdout_path}" 2>"${stderr_path}"

  assert_exists "${home_dir}/.codex/skills/run/SKILL.md" "Codex run planner should still exist after reinstall"
  assert_exists "${home_dir}/.claude/skills/run/SKILL.md" "Claude run planner should still exist after reinstall"
  assert_exists "${home_dir}/.claude/commands/run.md" "Claude command wrapper should still exist after reinstall"
  assert_exists "${home_dir}/.local/bin/run-workflow" "primary workflow runner should still exist after reinstall"
  assert_exists "${home_dir}/.local/bin/run-skill" "runner shim should still exist after reinstall"
  [[ -L "${home_dir}/.local/bin/run-workflow" ]] || fail "primary workflow runner should remain a symlink after reinstall"
  [[ -L "${home_dir}/.local/bin/run-skill" ]] || fail "runner shim should remain a symlink after reinstall"
  assert_contains "${stdout_path}" "Installed run-workflow." "reinstall should complete successfully"
  [[ ! -s "${stderr_path}" ]] || fail "reinstall should not emit stderr"
  pass "install is idempotent for existing run-owned paths"
}

test_install_preserves_host_shared
test_preflight_blocks_partial_install
test_install_is_idempotent_for_existing_run_paths

note ""
note "Passed: ${PASS_COUNT}"
note "Failed: ${FAIL_COUNT}"
[[ "${FAIL_COUNT}" -eq 0 ]]
