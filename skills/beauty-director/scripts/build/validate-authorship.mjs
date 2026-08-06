#!/usr/bin/env node
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "../..");
const STYLES_DIR = join(ROOT, "references/catalog/styles");
const errors = [];
const evidencePlaceholders = /\b(?:placeholder|unsourced|tbd|todo)\b|canonical design-history references|comparative formal analysis/i;

function hexToRgb(hex) {
  const value = String(hex).replace("#", "").trim();
  if (!/^[0-9a-fA-F]{6}$/.test(value)) return null;
  return {
    r: parseInt(value.slice(0, 2), 16),
    g: parseInt(value.slice(2, 4), 16),
    b: parseInt(value.slice(4, 6), 16),
  };
}

function rgbDistance(a, b) {
  return Math.hypot(a.r - b.r, a.g - b.g, a.b - b.b);
}

function hue(rgb) {
  const r = rgb.r / 255;
  const g = rgb.g / 255;
  const b = rgb.b / 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const delta = max - min;
  if (delta < 0.02) return null;
  let result;
  if (max === r) result = ((g - b) / delta) % 6;
  else if (max === g) result = (b - r) / delta + 2;
  else result = (r - g) / delta + 4;
  result *= 60;
  return result < 0 ? result + 360 : result;
}

function hueSpan(values) {
  if (values.length <= 1) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  let largestGap = sorted[0] + 360 - sorted.at(-1);
  for (let index = 0; index < sorted.length - 1; index += 1) {
    largestGap = Math.max(largestGap, sorted[index + 1] - sorted[index]);
  }
  return 360 - largestGap;
}

function arithmeticProgression(colors) {
  if (colors.length < 3 || colors.some((color) => !color)) return false;
  const deltas = colors.slice(1).map((color, index) => ({
    r: color.r - colors[index].r,
    g: color.g - colors[index].g,
    b: color.b - colors[index].b,
  }));
  const first = deltas[0];
  return deltas.every((delta) =>
    Math.abs(delta.r - first.r) <= 1 &&
    Math.abs(delta.g - first.g) <= 1 &&
    Math.abs(delta.b - first.b) <= 1
  );
}

function meanSortedDistance(a, b) {
  const left = [...a].map((value) => value.toUpperCase()).sort().map(hexToRgb);
  const right = [...b].map((value) => value.toUpperCase()).sort().map(hexToRgb);
  if (!left.length || left.some((color) => !color) || right.some((color) => !color)) return Infinity;
  return left.reduce((sum, color, index) => sum + rgbDistance(color, right[index]), 0) / left.length;
}

function wordCount(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s'-]/g, " ")
    .split(/\s+/)
    .filter(Boolean).length;
}

function monochromeIntent(text) {
  return /\bmono(chrome|chromatic)?\b|\bgr[ae]yscale\b|\bblack[- ]and[- ]white\b|\bB&W\b|\bachromatic\b/i.test(text);
}

const styleIds = readdirSync(STYLES_DIR)
  .filter((id) => existsSync(join(STYLES_DIR, id, "style.json")))
  .sort();
const styles = styleIds.map((id) => {
  const directory = join(STYLES_DIR, id);
  return {
    id,
    style: JSON.parse(readFileSync(join(directory, "style.json"), "utf8")),
    prose: readFileSync(join(directory, "STYLE.md"), "utf8"),
    evidence: existsSync(join(directory, "evidence.json"))
      ? readFileSync(join(directory, "evidence.json"), "utf8")
      : "",
  };
});

const sentenceOwners = new Map();
for (const { id, prose } of styles) {
  const seen = new Set();
  let repeatedSentenceCount = 0;
  const sentences = prose
    .replace(/^#.*$/gm, " ")
    .split(/(?<=[.!?])\s+/)
    .map((sentence) => sentence.toLowerCase().replace(/[^a-z0-9\s'-]/g, " ").replace(/\s+/g, " ").trim())
    .filter((sentence) => sentence.split(/\s+/).length >= 12);
  for (const sentence of sentences) {
    if (seen.has(sentence)) repeatedSentenceCount += 1;
    seen.add(sentence);
  }
  if (repeatedSentenceCount) errors.push(`${id}: REPEATED PROSE — ${repeatedSentenceCount} repeated sentence(s) within STYLE.md`);
  for (const sentence of seen) {
    if (!sentenceOwners.has(sentence)) sentenceOwners.set(sentence, []);
    sentenceOwners.get(sentence).push(id);
  }
}
for (const [sentence, owners] of sentenceOwners) {
  if (owners.length >= 3) {
    errors.push(`TEMPLATE PROSE — identical sentence appears in ${owners.length} styles: ${owners.join(", ")} :: ${sentence.slice(0, 100)}…`);
  }
}

for (const { id, style, prose, evidence } of styles) {
  const hexes = style.concerns?.palette?.hexes || [];
  const colors = hexes.map(hexToRgb);
  if (!hexes.length || colors.some((color) => !color)) errors.push(`${id}: invalid palette hexes`);
  if (arithmeticProgression(colors)) errors.push(`${id}: PALETTE FORMULA — arithmetic RGB progression`);
  const span = hueSpan(colors.filter(Boolean).map(hue).filter((value) => value !== null));
  if (span < 60 && !monochromeIntent(prose)) {
    errors.push(`${id}: PALETTE FLATNESS — hue span ${span.toFixed(1)}° < 60 without monochrome intent`);
  }
  const words = wordCount(prose);
  if (words < 350 || words > 700) errors.push(`${id}: PROSE LENGTH — ${words} words (required 350–700)`);
  if (!evidence) errors.push(`${id}: missing evidence.json`);
  else if (evidencePlaceholders.test(evidence)) errors.push(`${id}: placeholder or generic evidence text`);
}

for (let left = 0; left < styles.length; left += 1) {
  for (let right = left + 1; right < styles.length; right += 1) {
    const a = styles[left];
    const b = styles[right];
    const distance = meanSortedDistance(
      a.style.concerns?.palette?.hexes || [],
      b.style.concerns?.palette?.hexes || [],
    );
    if (distance < 40) {
      errors.push(`PALETTE COLLISION: ${a.id} ↔ ${b.id} mean sorted RGB distance ${distance.toFixed(2)} < 40`);
    }
  }
}

if (errors.length) {
  console.error(`validate-authorship: FAIL (${errors.length} error(s))`);
  for (const error of errors) console.error(`  - ${error}`);
  process.exit(1);
}

console.log("validate-authorship: OK");
console.log(`  styles checked: ${styles.length} (derived from references/catalog/styles/)`);
console.log("  checks: palette formula, collision, flatness; prose length; repeated template prose; truthful evidence text");
