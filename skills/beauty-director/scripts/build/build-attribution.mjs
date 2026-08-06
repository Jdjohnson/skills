#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "../..");
const ledger = JSON.parse(readFileSync(join(ROOT, "references/image-sources.json"), "utf8"));
const lines = [
  "# Reference Image Attribution",
  "",
  "Every bundled reference is delivered at 800x1000 pixels. Each asset's own attribution and modification note states whether its source was cropped, padded, or proportionally resized. Public-source records preserve their license and file-page evidence; generated records preserve their generator, date, prompt, and modification note.",
  "",
];

for (const record of ledger.images) {
  lines.push(
    `## ${record.styleId} — ${basename(record.localPath)}`,
    "",
    `Local file: ${record.localPath}`,
    "",
    record.attributionText,
    "",
  );
  if (record.rightsNote) lines.push(`Rights/fit note: ${record.rightsNote}`, "");
  if (record.conditions) {
    lines.push(
      `Intended-use condition: ${record.conditions.intendedUse}`,
      `Underlying-use conditions: ${[
        record.conditions.underlyingWork,
        record.conditions.trademark,
        record.conditions.peoplePrivacyPublicity,
        record.conditions.architectureProperty,
        record.conditions.culturalUse,
      ].join("; ")}`,
      "",
    );
  }
  if (record.originType === "generated" && record.generationRecord) {
    lines.push(`Generation record: ${record.generationRecord}`, "");
  }
}

writeFileSync(join(ROOT, "ATTRIBUTION.md"), `${lines.join("\n")}\n`);
console.log(`build-attribution: WROTE ATTRIBUTION.md (${ledger.images.length} images)`);
