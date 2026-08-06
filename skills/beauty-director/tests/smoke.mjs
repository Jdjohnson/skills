#!/usr/bin/env node
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, extname, join, relative } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CATALOG = join(ROOT, "references/catalog");
const failures = [];
const forbiddenFields = new Set(["cardPath", "neighbors", "threeWords"]);

function findNamedFiles(directory, target, found = []) {
  if (!existsSync(directory)) return found;
  for (const name of readdirSync(directory)) {
    const path = join(directory, name);
    if (statSync(path).isDirectory()) findNamedFiles(path, target, found);
    else if (name === target) found.push(path);
  }
  return found;
}

function jsonFiles(directory, found = []) {
  if (!existsSync(directory)) return found;
  for (const name of readdirSync(directory)) {
    const path = join(directory, name);
    if (statSync(path).isDirectory()) jsonFiles(path, found);
    else if (name.endsWith(".json")) found.push(path);
  }
  return found;
}

function inspectForbiddenKeys(value, file, trail = []) {
  if (Array.isArray(value)) {
    value.forEach((item, index) => inspectForbiddenKeys(item, file, [...trail, String(index)]));
    return;
  }
  if (!value || typeof value !== "object") return;
  for (const [key, nested] of Object.entries(value)) {
    if (forbiddenFields.has(key)) failures.push(`${relative(ROOT, file)}: forbidden stored field ${[...trail, key].join(".")}`);
    inspectForbiddenKeys(nested, file, [...trail, key]);
  }
}

let index;
try {
  index = JSON.parse(readFileSync(join(ROOT, "references/index.json"), "utf8"));
} catch (error) {
  failures.push(`index parse: ${error.message}`);
  index = { styles: [] };
}

let ledger;
try {
  ledger = JSON.parse(readFileSync(join(ROOT, "references/image-sources.json"), "utf8"));
} catch (error) {
  failures.push(`ledger parse: ${error.message}`);
  ledger = { images: [] };
}

if (existsSync(join(ROOT, "assets/cards"))) failures.push("assets/cards must not exist");
for (const path of findNamedFiles(ROOT, "MANIFEST-REVIEW.md")) {
  failures.push(`${relative(ROOT, path)}: obsolete MANIFEST-REVIEW.md must not exist`);
}
for (const path of findNamedFiles(CATALOG, "sources.md")) {
  failures.push(`${relative(ROOT, path)}: legacy sources.md must not exist`);
}
for (const file of [...jsonFiles(CATALOG), join(ROOT, "references/index.json")]) {
  if (!existsSync(file)) continue;
  try {
    inspectForbiddenKeys(JSON.parse(readFileSync(file, "utf8")), file);
  } catch (error) {
    failures.push(`${relative(ROOT, file)} parse: ${error.message}`);
  }
}

const agentMetadata = join(ROOT, "agents/openai.yaml");
if (!existsSync(agentMetadata)) failures.push("agents/openai.yaml must exist");

const readmePath = join(ROOT, "README.md");
if (existsSync(readmePath)) {
  const readme = readFileSync(readmePath, "utf8");
  const obsoleteReadme = /\bcard images?\b|\bcard paths?\b|cardPath|card\.png|reviewed neighbor manifest|mandatory neighbors?|stored neighbors?/i;
  if (obsoleteReadme.test(readme)) failures.push("README.md contains obsolete card or neighbor-manifest references");
}

const ids = new Set(index.styles.map((style) => style.id));
if (index.styles.length !== 120) failures.push(`index: expected exactly 120 styles, found ${index.styles.length}`);

const approvedLedger = (ledger.images || []).filter(
  (image) => image.assetReview?.status === "approved" && image.assetReview?.visualFit === "strong",
);
const approvedPaths = approvedLedger.map((image) => image.localPath).sort();
const indexPaths = index.styles.flatMap((style) => style.referencePaths || []).sort();
if (JSON.stringify(indexPaths) !== JSON.stringify(approvedPaths)) {
  failures.push(`index asset set does not equal approved strong ledger set (${indexPaths.length} index, ${approvedPaths.length} approved ledger)`);
}

const approvedByStyle = new Map();
for (const image of approvedLedger) {
  if (!approvedByStyle.has(image.styleId)) approvedByStyle.set(image.styleId, []);
  approvedByStyle.get(image.styleId).push(image.localPath);
}

for (const style of index.styles) {
  if (!Array.isArray(style.cues) || style.cues.length < 3) {
    failures.push(`${style.id}: fewer than three cues for derived display words`);
  }
  if (!Array.isArray(style.referencePaths) || style.referencePaths.length < 1 || style.referencePaths.length > 3) {
    failures.push(`${style.id}: expected 1-3 approved referencePaths`);
  }
  for (const referencePath of style.referencePaths || []) {
    const path = join(ROOT, referencePath);
    if (!existsSync(path)) {
      failures.push(`${style.id}: missing ${referencePath}`);
      continue;
    }
    const bytes = readFileSync(path).subarray(0, 12);
    const extension = extname(referencePath).toLowerCase();
    const valid =
      ([".jpg", ".jpeg"].includes(extension) && bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) ||
      (extension === ".png" && bytes.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) ||
      (extension === ".webp" && bytes.subarray(0, 4).toString("ascii") === "RIFF" && bytes.subarray(8, 12).toString("ascii") === "WEBP");
    if (!valid) failures.push(`${style.id}: ${referencePath} does not match its image extension`);
  }

  const evidencePath = join(CATALOG, "styles", style.id, "evidence.json");
  if (!existsSync(evidencePath)) {
    failures.push(`${style.id}: missing evidence.json`);
    continue;
  }
  const evidence = JSON.parse(readFileSync(evidencePath, "utf8"));
  if (evidence.humanVisualReview?.status === "approved") {
    const lead = evidence.humanVisualReview.leadImage;
    if (style.referencePaths?.[0] !== lead) failures.push(`${style.id}: approved leadImage is not first in index`);
    const expected = [lead, ...(approvedByStyle.get(style.id) || []).filter((path) => path !== lead).sort()];
    if (JSON.stringify(style.referencePaths) !== JSON.stringify(expected)) {
      failures.push(`${style.id}: index reference order does not match approved lead-first ledger order`);
    }
  }
}

const aliases = JSON.parse(readFileSync(join(CATALOG, "aliases.json"), "utf8")).aliases || [];
const expectedAliases = new Map(index.styles.map((style) => [style.id, new Set()]));
for (const alias of aliases) {
  for (const target of alias.targets || []) {
    if (target.kind === "style") {
      if (!ids.has(target.id)) failures.push(`alias ${alias.phrase}: unknown style ${target.id}`);
      else expectedAliases.get(target.id).add(alias.phrase);
    }
  }
}
for (const style of index.styles) {
  const actual = new Set(style.aliasPhrases || []);
  for (const phrase of actual) {
    if (!expectedAliases.get(style.id).has(phrase)) failures.push(`${style.id}: unmapped aliasPhrase ${phrase}`);
  }
  for (const phrase of expectedAliases.get(style.id)) {
    if (!actual.has(phrase)) failures.push(`${style.id}: missing aliasPhrase ${phrase}`);
  }
}

for (const validator of ["validate-catalog.mjs", "validate-authorship.mjs", "validate-image-sources.mjs"]) {
  const result = spawnSync(process.execPath, [join(ROOT, "scripts/build", validator)], {
    cwd: ROOT,
    encoding: "utf8",
  });
  if (result.status !== 0) failures.push(`${validator}: exit ${result.status}\n${result.stderr || result.stdout}`);
}

if (failures.length) {
  console.error(`smoke: FAIL (${failures.length} failure(s))`);
  for (const failure of failures) console.error(`  - ${failure}`);
  process.exit(1);
}

console.log("smoke: OK");
console.log(`  index entries: ${index.styles.length}`);
console.log("  references: approved strong ledger assets only, lead first, 1-3 per style");
console.log("  obsolete cards, manifests, sources, neighbors, and stored three-word fields: absent");
console.log("  agent metadata, aliases, documentation, and validators: verified");
