import test from "node:test";
import assert from "node:assert/strict";
import {
  appendFileSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { execFileSync } from "node:child_process";

import {
  auditWiki,
  preflightWiki,
  resolveSource,
} from "../scripts/wiki-guard.mjs";

function write(path, content) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, content, "utf8");
}

function git(wikiDir, ...args) {
  return execFileSync("git", args, { cwd: wikiDir, encoding: "utf8" }).trim();
}

function createWorkspace({ policyRoot = "/definitely/missing/source-backed-wiki-test-root" } = {}) {
  const workspace = mkdtempSync(join(tmpdir(), "source-backed-wiki-test-"));
  const wikiDir = join(workspace, "wiki");
  mkdirSync(join(wikiDir, "pages"), { recursive: true });
  write(join(wikiDir, ".gitignore"), ".stversions/\n");
  write(join(wikiDir, "sources.md"), `# Wiki Sources\n\n\`\`\`json\n[\n  {\n    "alias": "optional-root",\n    "root": ${JSON.stringify(policyRoot)},\n    "access": "read-only"\n  }\n]\n\`\`\`\n`);
  return { workspace, wikiDir };
}

function initRepo(wikiDir) {
  git(wikiDir, "init", "-q");
  git(wikiDir, "config", "user.name", "Source Wiki Test");
  git(wikiDir, "config", "user.email", "source-wiki-test@example.invalid");
}

function commitAll(wikiDir, message) {
  git(wikiDir, "add", "--", ".");
  git(wikiDir, "commit", "-q", "-m", message);
  return git(wikiDir, "rev-parse", "HEAD");
}

test("neutral canonical source root ignores an unrelated missing external root", () => {
  const { workspace } = createWorkspace();
  const reference = "sources/2026/test.md";
  write(join(workspace, reference), "# Canonical source\n");

  const resolved = resolveSource(workspace, reference);

  assert.equal(resolved.kind, "canonical");
  assert.equal(resolved.reference, reference);
  assert.match(resolved.sha256, /^[0-9a-f]{64}$/);
});

test("workspace-specific source roots require configuration", () => {
  const { workspace } = createWorkspace();
  write(join(workspace, "timeline", "2026", "test.md"), "# Unconfigured source\n");

  assert.throws(
    () => resolveSource(workspace, "timeline/2026/test.md"),
    (error) => error.code === "not-ingestible" && error.message.includes("under sources/"),
  );
});

test("an external reference still requires its own configured root", () => {
  const { workspace } = createWorkspace();

  assert.throws(
    () => resolveSource(workspace, "optional-root: note.md"),
    (error) => error.code === "policy-root" && error.message === 'alias "optional-root" root does not exist',
  );
});

test("whole-wiki audit validates an existing external reference without mounting its optional root", () => {
  const { workspace, wikiDir } = createWorkspace();
  write(join(wikiDir, "pages", "Optional Source.md"), `---\nkind: concept\naliases: []\ntags: ["test"]\nupdated: 2026-08-10\n---\n\n# Optional Source\n\n## Current understanding\n\nThis page preserves a previously resolved external reference.\n\n## Sources\n\n- optional-root: note.md\n`);
  write(join(wikiDir, "index.md"), `# Wiki Index\n\n## Concepts\n\n- [[Optional Source]] | kind=concept | updated=2026-08-10 | A test page with an optional external source.\n\n## Entities\n\n## Syntheses\n`);
  write(join(wikiDir, "log.md"), "# Wiki Log\n\nEntries are append-only.\n");

  const result = auditWiki(workspace);

  assert.equal(result.ok, true, JSON.stringify(result.errors));
});

test("preflight explicitly repairs the exact stale-index state produced by a synced new commit", () => {
  const { workspace, wikiDir } = createWorkspace();
  initRepo(wikiDir);
  write(join(wikiDir, "index.md"), "version one\n");
  const oldCommit = commitAll(wikiDir, "initial");

  write(join(wikiDir, "index.md"), "version two\n");
  write(join(wikiDir, "pages", "New Page.md"), "new page\n");
  const newCommit = commitAll(wikiDir, "synced update");
  git(wikiDir, "read-tree", oldCommit);
  assert.notEqual(git(wikiDir, "status", "--porcelain"), "");

  const result = preflightWiki(workspace, { repairStaleIndex: true });

  assert.equal(result.indexRefreshed, true);
  assert.equal(result.head, newCommit);
  assert.equal(result.previousIndexCommit, oldCommit);
  assert.equal(git(wikiDir, "status", "--porcelain"), "");
  assert.equal(readFileSync(join(wikiDir, "pages", "New Page.md"), "utf8"), "new page\n");
});

test("preflight preserves and blocks on a real working-tree edit", () => {
  const { workspace, wikiDir } = createWorkspace();
  initRepo(wikiDir);
  write(join(wikiDir, "index.md"), "committed\n");
  commitAll(wikiDir, "initial");
  appendFileSync(join(wikiDir, "index.md"), "human edit\n", "utf8");

  assert.throws(
    () => preflightWiki(workspace),
    (error) => error.code === "repo-dirty" && error.message.includes("content differs from HEAD"),
  );
  assert.equal(readFileSync(join(wikiDir, "index.md"), "utf8"), "committed\nhuman edit\n");
});

test("preflight preserves and blocks on extra untracked content", () => {
  const { workspace, wikiDir } = createWorkspace();
  initRepo(wikiDir);
  write(join(wikiDir, "index.md"), "committed\n");
  commitAll(wikiDir, "initial");
  write(join(wikiDir, "notes.md"), "do not discard\n");

  assert.throws(
    () => preflightWiki(workspace),
    (error) => error.code === "repo-dirty" && error.message.includes("extra untracked content"),
  );
  assert.equal(readFileSync(join(wikiDir, "notes.md"), "utf8"), "do not discard\n");
});

test("preflight refuses a repository with a remote", () => {
  const { workspace, wikiDir } = createWorkspace();
  initRepo(wikiDir);
  write(join(wikiDir, "index.md"), "committed\n");
  commitAll(wikiDir, "initial");
  git(wikiDir, "remote", "add", "origin", "https://example.invalid/wiki.git");

  assert.throws(
    () => preflightWiki(workspace),
    (error) => error.code === "repo-remote",
  );
});
