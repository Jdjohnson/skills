#!/usr/bin/env node

import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const argv = process.argv.slice(2);
const mode = argv[0] || "";
const EXECUTION_MODES = new Map([
  ["ai", "AI generation"],
  ["ai generation", "AI generation"],
  ["photographer", "a photographer"],
  ["a photographer", "a photographer"],
  ["self-shoot", "self-shooting"],
  ["self-shooting", "self-shooting"],
  ["both", "both"],
]);

function value(flag, fallback = "") {
  const index = argv.indexOf(flag);
  return index >= 0 && argv[index + 1] ? argv[index + 1] : fallback;
}

function normalize(input) {
  return String(input || "")
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[’']/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function hasPhrase(text, phrase) {
  return Boolean(phrase) && ` ${text} `.includes(` ${phrase} `);
}

const STOP = new Set("a an and are as at be but by can do does for from has have i if in into is it its like more my of on or our that the their them then this to too up want we with you your".split(" "));
const NEGATORS = new Set(["not", "no", "avoid", "without", "never", "dont", "doesnt"]);
const NEGATIVE_GENERIC = new Set(["color", "image", "light", "look", "photo", "photography", "portrait", "scene", "subject"]);
const SCOPE_BREAKS = new Set(["but", "however", "except", "instead", "while", "though", "although", "yet"]);
const STEMS = new Map([
  ["people", "person"], ["persons", "person"], ["workers", "worker"], ["working", "work"],
  ["photos", "photo"], ["photographs", "photo"], ["photography", "photo"],
  ["children", "child"], ["kids", "child"], ["riders", "rider"], ["bikes", "bike"],
  ["motorcycles", "motorcycle"], ["products", "product"], ["components", "component"],
  ["interiors", "interior"], ["buildings", "building"], ["lakes", "lake"], ["lakeside", "lake"],
  ["dishes", "dish"], ["meals", "meal"],
  ["events", "event"], ["meetings", "meeting"], ["teams", "team"], ["portraits", "portrait"],
  ["blurred", "blur"], ["blurry", "blur"], ["softness", "soft"], ["moving", "motion"],
  ["warmer", "warm"], ["warmth", "warm"],
  ["indoors", "indoor"], ["pane", "window"], ["panes", "window"],
  ["dancers", "dancer"], ["leaping", "leap"], ["trails", "trail"],
]);

function tokens(input) {
  return [...new Set(normalize(input).split(" ").filter((token) => token && !STOP.has(token)).map((token) => STEMS.get(token) || token))];
}

function queryIntent(input) {
  const words = String(input || "")
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[’']/g, "")
    .replace(/[,.;:!?()[\]{}]+/g, " | ")
    .replace(/[^a-z0-9|]+/g, " ")
    .trim()
    .split(/\s+/)
    .filter(Boolean);
  const positive = [];
  const negative = [];
  let negated = false;
  for (const word of words) {
    if (word === "|") {
      negated = false;
      continue;
    }
    if (SCOPE_BREAKS.has(word)) {
      negated = false;
      continue;
    }
    if (NEGATORS.has(word)) {
      negated = true;
      continue;
    }
    (negated ? negative : positive).push(word);
  }
  return {
    positiveText: positive.join(" "),
    negativeText: negative.join(" "),
    positiveTokens: tokens(positive.join(" ")),
    negativeTokens: tokens(negative.join(" ")),
  };
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function jsonFiles(directory) {
  return readdirSync(directory).filter((name) => name.endsWith(".json")).sort();
}

const catalog = join(ROOT, "references/catalog");
const ledger = readJson(join(ROOT, "references/source-ledger.json"));
const subjectCatalog = readJson(join(catalog, "subject-sets.json"));
const visibleFitCatalog = existsSync(join(catalog, "visible-fit.json"))
  ? readJson(join(catalog, "visible-fit.json"))
  : { references: [] };
const visibleFitReferences = new Map((visibleFitCatalog.references || []).map((item) => [item.id, item]));
const supportReferences = (subjectCatalog.references || []).map((item) => {
  const defaults = subjectCatalog.sourceDefaults || {};
  const review = {
    ...(defaults.review || {}),
    ...(item.review || {}),
    teachingRole: item.teachingRole || item.review?.teachingRole || "",
  };
  return { ...defaults, ...item, review };
});
const references = new Map([...(ledger.references || []), ...supportReferences].map((item) => [item.id, item]));
const aliases = readJson(join(catalog, "aliases.json")).aliases || [];
const looks = jsonFiles(join(catalog, "looks")).map((name) => readJson(join(catalog, "looks", name)));
const axes = jsonFiles(join(catalog, "axes")).map((name) => readJson(join(catalog, "axes", name)));
const axisValues = new Map(axes.flatMap((axis) => (axis.values || []).map((item) => [item.id, item])));

const INTENTS = [
  { words: "portrait person founder leader professional approachable skin face", ids: ["approachable-environmental-portrait", "window-light-editorial-portrait", "mid-century-editorial-portrait", "polished-commercial-headshot", "low-key-character-portrait"] },
  { words: "team work workplace worker collaboration meeting conference candid", ids: ["candid-event-reportage", "humanist-available-light-photo-essay", "industrial-color-production-reportage", "industrial-workplace-documentary", "approachable-environmental-portrait"] },
  { words: "person worker machinery factory industrial gritty documentary", ids: ["industrial-human-machine-portrait", "industrial-workplace-documentary", "industrial-color-production-reportage", "fsa-social-documentary", "humanist-available-light-photo-essay"] },
  { words: "machined metal component part product manufactured precision honest", ids: ["clean-seamless-product", "scientific-specimen-record", "sculptural-hard-light-product", "industrial-color-production-reportage", "luxury-still-life-polish"] },
  { words: "glass jar candle bottle skincare packaging reflection translucent", ids: ["luxury-still-life-polish", "clean-seamless-product", "sculptural-hard-light-product", "selective-focus-macro", "dark-moody-tabletop"] },
  { words: "food restaurant dish edible ingredient table cozy meal", ids: ["bright-editorial-food", "window-light-food-story", "dark-moody-tabletop", "direct-flash-still-life"] },
  { words: "interior clinic architecture room building material space", ids: ["symmetrical-interior-study", "straight-photography-precision", "tilt-shift-architectural-study", "blue-hour-urban-architecture", "new-topographics-deadpan-landscape"] },
  { words: "lake river water shoreline mist hazy quiet landscape", ids: ["overcast-minimal-landscape", "pictorialist-soft-focus-landscape", "long-exposure-seascape", "new-topographics-deadpan-landscape", "travel-photo-essay"] },
  { words: "child summer sprinkler play playful yard messy motion", ids: ["candid-event-reportage", "editorial-contact-sheet-sequence", "frozen-sports-action", "peak-action-photojournalism", "instant-film-everyday-snapshot"] },
  { words: "motorcycle bike cyclist rider vehicle motion pan city night", ids: ["rolling-automotive-pan", "rear-curtain-flash-motion", "night-street-color", "night-light-trail-cityscape", "peak-action-photojournalism"] },
  { words: "bird animal wildlife habitat pond nature", ids: ["super-telephoto-wildlife", "frozen-sports-action", "selective-focus-macro", "scientific-specimen-record"] },
  { words: "historical vintage antique 1920s 1940s studio portrait", ids: ["daguerreotype-studio-portrait", "wet-plate-collodion-portrait", "mid-century-editorial-portrait", "mid-century-commercial-color", "new-vision-geometry"] },
];

function textScore(query, record) {
  const intent = queryIntent(query);
  const queryText = normalize(intent.positiveText);
  const queryTokens = intent.positiveTokens;
  const fields = [
    [record.displayName, 10], [record.id, 8], [record.family, 6],
    [record.aliases, 9], [record.applicability, 8], [record.cues || record.visibleCues, 6],
    [record.definition, 3], [record.axisValueIds, 2],
  ];
  let score = 0;
  for (const [field, weight] of fields) {
    const source = Array.isArray(field) ? field.join(" ") : field;
    const text = normalize(source);
    const fieldTokens = new Set(tokens(source));
    for (const token of queryTokens) if (fieldTokens.has(token) || text.includes(token)) score += weight;
  }
  for (const phrase of record.aliases || []) {
    const normalized = normalize(phrase);
    if (normalized && (queryText.includes(normalized) || normalized.includes(queryText))) score += 45;
  }
  for (const alias of aliases) {
    const phrase = normalize(alias.phrase);
    if (!phrase || !queryText.includes(phrase)) continue;
    if (alias.targets.some((target) => target.kind === "look" && target.id === record.id)) score += 60;
    if (alias.targets.some((target) => target.kind === "axis-value" && Object.values(record.axisValues || {}).flat().includes(target.id))) score += 25;
  }
  for (const intent of INTENTS) {
    const overlap = tokens(intent.words).filter((token) => queryTokens.includes(token)).length;
    const position = intent.ids.indexOf(record.id);
    if (overlap && position >= 0) score += overlap * Math.max(4, 18 - position * 3);
  }
  const positiveRecord = fields.map(([field]) => Array.isArray(field) ? field.join(" ") : field).join(" ");
  const positiveRecordText = normalize(positiveRecord);
  const positiveRecordTokens = new Set(tokens(positiveRecord));
  const antiCueText = normalize((record.antiCues || []).join(" "));
  const antiCueTokens = new Set(tokens(record.antiCues || []));
  for (const token of intent.negativeTokens) {
    if (!NEGATIVE_GENERIC.has(token) && (positiveRecordTokens.has(token) || positiveRecordText.includes(token))) score -= 28;
    if (antiCueTokens.has(token) || antiCueText.includes(token)) score += 18;
  }
  for (const phrase of record.aliases || []) {
    const normalized = normalize(phrase);
    if (normalized && intent.negativeText.includes(normalized)) score -= 45;
  }
  for (const alias of aliases) {
    const phrase = normalize(alias.phrase);
    if (!phrase || !intent.negativeText.includes(phrase)) continue;
    if (alias.targets.some((target) => target.kind === "look" && target.id === record.id)) score -= 60;
    if (alias.targets.some((target) => target.kind === "axis-value" && Object.values(record.axisValues || {}).flat().includes(target.id))) score -= 25;
  }
  return score;
}

function displayReference(id) {
  const item = references.get(id);
  if (!item) throw new Error(`Missing reference ${id}`);
  const displayPath = item.displayMode === "bundled" ? resolve(ROOT, item.localPath) : item.assetUrl;
  if (item.displayMode === "bundled" && !existsSync(displayPath)) throw new Error(`Missing bundled image ${displayPath}`);
  const compactClaim = ({ field, value, basis }) => ({ field, value, basis });
  const confirmed = (item.technicalClaims || []).filter((claim) => claim.basis === "confirmed").map(compactClaim);
  const documented = (item.technicalClaims || []).filter((claim) => claim.basis === "documented").map(compactClaim);
  return {
    id: item.id,
    path: displayPath,
    title: item.title,
    ...(item.attributionText ? { credit: item.attributionText } : {}),
    ...(confirmed.length ? { confirmed } : {}),
    ...(documented.length ? { documented } : {}),
    role: item.review?.teachingRole || "",
  };
}

const FIT_VALUE_ALIASES = Object.freeze({
  subjectCount: new Map([
    ["single", "single"], ["single-person", "single"], ["one-person", "single"], ["one", "single"], ["person", "single"], ["individual", "single"],
    ["group", "group"], ["team", "group"], ["many", "group"],
  ]),
  setting: new Map([
    ["home-office", "home-office"], ["homeoffice", "home-office"], ["home", "home-office"], ["office", "office"],
    ["workplace", "workplace"], ["workshop", "workshop"], ["industrial-workplace", "industrial-workplace"],
  ]),
  action: new Map([
    ["solo-work", "solo-work"], ["solo", "solo-work"], ["working", "solo-work"], ["work", "solo-work"],
    ["group-work", "group-work"], ["group", "group-work"], ["collaboration", "group-work"], ["discussion", "group-work"], ["meeting", "group-work"],
    ["industrial-task", "industrial-task"], ["industrial", "industrial-task"], ["portrait", "portrait"],
  ]),
  trait: new Map([
    ["solo-work", "solo-work"], ["group-work", "group-work"], ["group", "group-work"], ["home-office", "home-office"],
    ["workplace", "workplace"], ["documentary", "documentary"], ["portrait", "portrait"], ["industrial", "industrial"],
  ]),
});
const FIT_KEY_ALIASES = new Map([
  ["subject", "subjectCount"], ["subject-count", "subjectCount"], ["subjectcount", "subjectCount"], ["people", "subjectCount"], ["count", "subjectCount"],
  ["setting", "setting"], ["scene", "setting"],
  ["action", "action"], ["activity", "action"], ["task", "action"],
  ["trait", "trait"], ["traits", "trait"],
]);

function flagValues(flags) {
  const accepted = new Set(flags);
  const values = [];
  for (let index = 0; index < argv.length - 1; index += 1) {
    if (!accepted.has(argv[index]) || !argv[index + 1] || argv[index + 1].startsWith("--")) continue;
    values.push(argv[index + 1]);
    index += 1;
  }
  return values;
}

function canonicalFitValue(key, raw) {
  const normalized = normalize(raw).replace(/ /g, "-");
  const canonical = FIT_VALUE_ALIASES[key]?.get(normalized);
  if (!canonical) throw new Error(`Unknown hard-fit ${key} value ${raw}`);
  return canonical;
}

function canonicalFitKey(raw) {
  const normalized = normalize(raw).replace(/ /g, "-");
  const key = FIT_KEY_ALIASES.get(normalized);
  if (!key) throw new Error(`Unknown hard-fit constraint ${raw}`);
  return key;
}

function parseHardFit() {
  const hardFit = { subjectCount: [], setting: [], action: [], trait: [], excludedTraits: [] };
  const add = (key, raw, excluded = false) => {
    const canonicalKey = canonicalFitKey(key);
    const canonicalValue = canonicalFitValue(canonicalKey, raw);
    const target = excluded ? hardFit.excludedTraits : hardFit[canonicalKey];
    if (!target.includes(canonicalValue)) target.push(canonicalValue);
  };
  for (const rawToken of flagValues(["--hard-fit", "--hard-constraint", "--hard-constraints", "--constraint", "--constraints", "--require-fit", "--fit"]).flatMap((item) => item.split(/[,;]/))) {
    const separator = rawToken.indexOf("=");
    if (separator < 1 || separator === rawToken.length - 1) throw new Error(`Hard-fit constraint must be key=value: ${rawToken}`);
    add(rawToken.slice(0, separator), rawToken.slice(separator + 1));
  }
  for (const [key, flags] of Object.entries({
    subjectCount: ["--subject-count", "--subject"],
    setting: ["--setting"],
    action: ["--action", "--activity"],
    trait: ["--require-trait", "--include-trait"],
  })) for (const raw of flagValues(flags)) add(key, raw);
  for (const raw of flagValues(["--exclude-trait"]).flatMap((item) => item.split(","))) add("trait", raw, true);
  const present = Object.values(hardFit).some((values) => values.length);
  return present ? hardFit : undefined;
}

function compactHardFitConstraints(hardFit) {
  if (!hardFit) return undefined;
  return {
    source: "controlled-cli",
    ...(hardFit.subjectCount.length ? { "subject-count": hardFit.subjectCount } : {}),
    ...(hardFit.setting.length ? { setting: hardFit.setting } : {}),
    ...(hardFit.action.length ? { action: hardFit.action } : {}),
    ...(hardFit.trait.length ? { trait: hardFit.trait } : {}),
    ...(hardFit.excludedTraits.length ? { "excluded-trait": hardFit.excludedTraits } : {}),
    ...(hardFit.excludedReferences?.length ? { "excluded-reference": hardFit.excludedReferences } : {}),
  };
}

function fitFieldValues(record, field) {
  if (!record || !Object.hasOwn(record, field) || record[field] === null || record[field] === undefined) return undefined;
  return Array.isArray(record[field]) ? record[field] : [record[field]];
}

function fitDisplayReference(id, fitRole) {
  return {
    ...displayReference(id),
    fitRole,
    anchorEligible: fitRole === "eligible-target",
    ...(fitRole === "eligible-target" ? {} : { componentStudy: true }),
  };
}

function evaluateVisibleFit(set, hardFit, excluded) {
  const eligibleCandidates = [];
  const traitStudies = [];
  const componentStudies = [];
  const eligibleTreatmentLookIds = [];
  const traitStudyTreatmentLookIds = [];
  const exclusions = [];
  const missingCoverage = [];
  for (const [referenceIndex, referenceId] of (set.referenceIds || []).entries()) {
    const record = visibleFitReferences.get(referenceId);
    if (excluded.has(referenceId)) {
      exclusions.push({ referenceId, reason: "explicit reference exclusion" });
      continue;
    }
    const excludedTrait = hardFit.excludedTraits.find((trait) => fitFieldValues(record, "traits")?.includes(trait));
    if (excludedTrait) {
      exclusions.push({ referenceId, reason: `excluded trait: ${excludedTrait}` });
      continue;
    }
    const requiredFields = [
      ["subjectCount", hardFit.subjectCount],
      ["settings", hardFit.setting],
      ["actions", hardFit.action],
      ["traits", hardFit.trait],
    ].filter(([, values]) => values.length);
    const unknown = requiredFields.filter(([field]) => !fitFieldValues(record, field)).map(([field]) => field);
    if (hardFit.excludedTraits.length && !fitFieldValues(record, "traits")) unknown.push("traits");
    if (unknown.length) {
      componentStudies.push({
        ...fitDisplayReference(referenceId, "component-study"),
        componentStudyReason: `visible fit unknown for ${[...new Set(unknown)].join(", ")}; not an anchor`,
      });
      missingCoverage.push({ referenceId, fields: [...new Set(unknown)], reason: "visible fit is unknown; no fit inferred" });
      continue;
    }
    const mismatch = requiredFields.some(([field, values]) => !values.some((value) => fitFieldValues(record, field).includes(value)));
    if (record?.traitStudyFor?.includes(set.id)) {
      traitStudies.push({ ...fitDisplayReference(referenceId, "trait-study"), traitStudyReason: "analogical reference; not an anchor" });
      if (set.treatmentLookIds?.[referenceIndex]) traitStudyTreatmentLookIds.push(set.treatmentLookIds[referenceIndex]);
    } else if (!mismatch) {
      eligibleCandidates.push(fitDisplayReference(referenceId, "eligible-target"));
      if (set.treatmentLookIds?.[referenceIndex]) eligibleTreatmentLookIds.push(set.treatmentLookIds[referenceIndex]);
    } else {
      const mismatchedFields = requiredFields
        .filter(([field, values]) => !values.some((value) => fitFieldValues(record, field).includes(value)))
        .map(([field]) => field);
      componentStudies.push({
        ...fitDisplayReference(referenceId, "component-study"),
        componentStudyReason: `partial fit on ${mismatchedFields.join(", ")}; not an anchor`,
      });
    }
  }
  const coverageGap = eligibleCandidates.length < 3
    ? {
      scope: "eligible-candidates",
      required: 3,
      found: eligibleCandidates.length,
      reason: `only ${eligibleCandidates.length} catalog references visibly satisfy all controlled constraints`,
    }
    : undefined;
  return {
    constraints: compactHardFitConstraints(hardFit),
    eligibleCandidates: eligibleCandidates.slice(0, 3),
    traitStudies: traitStudies.slice(0, 3),
    ...(componentStudies.length ? { componentStudies: componentStudies.slice(0, 3) } : {}),
    eligibleTreatmentLookIds: eligibleTreatmentLookIds.slice(0, 3),
    ...(traitStudyTreatmentLookIds.length ? { traitStudyTreatmentLookIds: traitStudyTreatmentLookIds.slice(0, 3) } : {}),
    ...(coverageGap ? { coverageGap } : {}),
    exclusions,
    missingCoverage,
    complete: eligibleCandidates.length >= 3 && missingCoverage.length === 0,
  };
}

function queryScopeMissingCoverage() {
  return [{
    scope: "query",
    fields: ["subject-set"],
    reason: "no positively matched subject set; hard-fit reference eligibility cannot be inferred from constraints alone",
  }];
}

function appearanceTerm(cue) {
  const item = axisValues.get(cue);
  return item?.claimPolicy === "inferred" && item.visibleCues?.[0] ? item.visibleCues[0] : cue;
}

function compactLook(look, includeReferences = true) {
  return {
    id: look.id,
    name: look.displayName,
    family: look.family,
    direction: look.definition,
    terms: (look.cues || []).slice(0, 4).map(appearanceTerm),
    avoid: (look.antiCues || []).slice(0, 2),
    uses: (look.applicability || []).slice(0, 4),
    ...(includeReferences ? { references: (look.referenceIds || []).map(displayReference) } : {}),
  };
}

function compactTreatment(look) {
  return {
    id: look.id,
    name: look.displayName,
    direction: look.definition,
    terms: (look.cues || []).slice(0, 4).map(appearanceTerm),
  };
}

function matchedSubjectSet(query, excluded = new Set(), hardFit) {
  const intent = queryIntent(query);
  const queryText = normalize(intent.positiveText);
  const queryTokens = intent.positiveTokens;
  const hasFitContext = Boolean(hardFit && (hardFit.setting.length || hardFit.action.length || hardFit.trait.length || hardFit.excludedTraits.length));
  const ranked = (subjectCatalog.sets || []).map((set) => {
    let score = 0;
    const triggerTokens = tokens((set.triggers || []).join(" "));
    const semanticOverlap = triggerTokens.filter((token) => queryTokens.includes(token)).length;
    for (const trigger of set.triggers || []) {
      const phrase = normalize(trigger);
      const triggerTokens = tokens(trigger);
      const overlap = triggerTokens.filter((token) => queryTokens.includes(token)).length;
      if (hasPhrase(queryText, phrase)) score = Math.max(score, 100 + triggerTokens.length * 10);
      else if (triggerTokens.length && overlap === triggerTokens.length) score = Math.max(score, 40 + overlap * 10);
    }
    for (const trigger of set.priorityTriggers || []) {
      const triggerTokens = tokens(trigger);
      if (triggerTokens.length && triggerTokens.every((token) => queryTokens.includes(token))) score += 200;
    }
    const blocked = (set.antiCues || []).some((cue) => {
      const phrase = normalize(cue);
      const cueTokens = tokens(cue);
      return hasPhrase(queryText, phrase) || (cueTokens.length > 0 && cueTokens.every((token) => queryTokens.includes(token)));
    });
    const negatedSetTerm = intent.negativeTokens.some((token) => tokens([...(set.triggers || []), set.id]).includes(token));
    if (blocked || negatedSetTerm) score = 0;
    if (hardFit && score === 0 && !blocked && !negatedSetTerm && semanticOverlap >= 2) score = semanticOverlap;
    const availablePairs = (set.referenceIds || [])
      .map((referenceId, referenceIndex) => ({
        referenceId,
        treatmentId: set.treatmentLookIds?.[referenceIndex],
      }))
      .filter(({ referenceId, treatmentId }) => !excluded.has(referenceId) && (!treatmentId || !excluded.has(treatmentId)));
    const matchedReferences = availablePairs
      .slice(0, 3)
      .map(({ referenceId }) => {
        const reference = displayReference(referenceId);
        const alsoDiffers = set.alsoDiffers?.[referenceId] || [];
        return alsoDiffers.length ? { ...reference, alsoDiffers } : reference;
      });
    const matchedTreatmentLookIds = availablePairs
      .slice(0, 3)
      .map(({ treatmentId }) => treatmentId)
      .filter(Boolean);
    const visibleFit = hardFit ? evaluateVisibleFit(set, hardFit, excluded) : undefined;
    return {
      set,
      score,
      matchedReferences,
      matchedTreatmentLookIds,
      visibleFit,
      complete: hardFit ? visibleFit.complete : matchedReferences.length === 3,
    };
  }).filter(({ score }) => score > 0)
    .sort((a, b) => {
      if (hardFit && hasFitContext) return Number(b.complete) - Number(a.complete)
        || (b.visibleFit?.eligibleCandidates.length || 0) - (a.visibleFit?.eligibleCandidates.length || 0)
        || b.score - a.score || a.set.id.localeCompare(b.set.id);
      if (hardFit) return Number(b.complete) - Number(a.complete) || b.score - a.score || a.set.id.localeCompare(b.set.id);
      return Number(b.complete) - Number(a.complete) || b.score - a.score || a.set.id.localeCompare(b.set.id);
    });
  if (!ranked[0]) return undefined;
  const { set, matchedReferences, matchedTreatmentLookIds, complete, visibleFit } = ranked[0];
  return {
    id: set.id,
    role: set.role,
    requiredLocks: set.requiredLocks || [],
    transferCard: set.transferCard || [],
    treatmentLookIds: matchedTreatmentLookIds,
    complete,
    ...(set.catalogGap ? { catalogGap: set.catalogGap } : {}),
    references: matchedReferences,
    ...(visibleFit ? { hardFit: visibleFit } : {}),
  };
}

function subjectPacket(subjectSet, includeReferences = false) {
  if (!subjectSet) return undefined;
  const hardFit = subjectSet.hardFit;
  return {
    id: subjectSet.id,
    role: subjectSet.role,
    ...(subjectSet.requiredLocks.length ? { requiredLocks: subjectSet.requiredLocks } : {}),
    ...(subjectSet.transferCard.length ? { transferCard: subjectSet.transferCard } : {}),
    complete: subjectSet.complete,
    ...(subjectSet.catalogGap ? { catalogGap: subjectSet.catalogGap } : {}),
    ...(includeReferences ? {
      pairByIndex: true,
      treatmentLookIds: hardFit ? hardFit.eligibleTreatmentLookIds : subjectSet.treatmentLookIds,
      ...(hardFit?.traitStudyTreatmentLookIds?.length ? { traitStudyTreatmentLookIds: hardFit.traitStudyTreatmentLookIds } : {}),
      references: hardFit ? hardFit.eligibleCandidates : subjectSet.references,
      ...(hardFit ? {
        eligibleCandidates: hardFit.eligibleCandidates,
        ...(hardFit.traitStudies.length ? { traitStudies: hardFit.traitStudies } : {}),
        ...(hardFit.componentStudies?.length ? { componentStudies: hardFit.componentStudies } : {}),
        ...(hardFit.exclusions.length ? { exclusions: hardFit.exclusions } : {}),
        ...(hardFit.coverageGap ? { coverageGap: hardFit.coverageGap } : {}),
        missingCoverage: hardFit.missingCoverage,
      } : {}),
    } : {}),
  };
}

function rankedLooks(query, limit, excluded, includeReferences = true) {
  return looks
    .filter((look) => !excluded.has(look.id) && !(look.referenceIds || []).some((id) => excluded.has(id)))
    .map((look) => ({ look, score: textScore(query, look) }))
    .sort((a, b) => b.score - a.score || a.look.id.localeCompare(b.look.id))
    .slice(0, limit)
    .map(({ look }) => compactLook(look, includeReferences));
}

function subjectLooks(query, subjectSet, excluded, hardFit, limit = 3) {
  const orderedLookIds = hardFit ? (hardFit.eligibleTreatmentLookIds || []) : (subjectSet?.treatmentLookIds || []);
  const curated = new Set(orderedLookIds);
  const blockedLookIds = new Set([...excluded, ...(hardFit?.traitStudyTreatmentLookIds || [])]);
  const preferred = looks
    .filter((look) => curated.has(look.id) && !blockedLookIds.has(look.id) && !(look.referenceIds || []).some((id) => blockedLookIds.has(id)))
    .sort((a, b) => orderedLookIds.indexOf(a.id) - orderedLookIds.indexOf(b.id))
    .map(compactTreatment);
  if (hardFit) return preferred.slice(0, limit);
  if (preferred.length >= 3) return preferred.slice(0, limit);
  const used = new Set(preferred.map((look) => look.id));
  const fallback = looks
    .filter((look) => !used.has(look.id) && !blockedLookIds.has(look.id) && !(look.referenceIds || []).some((id) => blockedLookIds.has(id)))
    .map((look) => ({ look, score: textScore(query, look) }))
    .sort((a, b) => b.score - a.score || a.look.id.localeCompare(b.look.id))
    .map(({ look }) => compactTreatment(look));
  return [...preferred, ...fallback].slice(0, limit);
}

function axisRecords() {
  return axes.flatMap((axis) => axis.values.map((item) => ({ ...item, axisId: axis.id, axisName: axis.displayName })));
}

function rankedAxes(query, limit, includeReferences = true) {
  return axisRecords()
    .map((item) => ({ item, score: textScore(query, item) }))
    .sort((a, b) => b.score - a.score || a.item.id.localeCompare(b.item.id))
    .slice(0, limit)
    .map(({ item }) => ({
      axisId: item.axisId,
      axisName: item.axisName,
      id: item.id,
      name: item.displayName,
      direction: item.definition,
      cues: (item.visibleCues || []).slice(0, 4),
      avoid: (item.antiCues || []).slice(0, 2),
      claimPolicy: item.claimPolicy,
      ...(includeReferences ? { references: (item.referenceIds || []).slice(0, 1).map(displayReference) } : {}),
    }));
}

function requestedDelta(input) {
  const text = String(input || "").trim();
  const separators = [
    /\s*;\s*(?:hold|keep|preserve)\b/i,
    /\s+while\s+(?:holding|keeping|preserving)\b/i,
  ];
  const indices = separators.map((pattern) => text.search(pattern)).filter((index) => index > 0);
  return indices.length ? text.slice(0, Math.min(...indices)).trim() : text;
}

function multiSampleSubjectSet(query, excluded, hardFit) {
  if (!argv.includes("--multi-sample")) return undefined;
  const match = String(query || "").match(/sample\s+a\s*:\s*([\s\S]*?)(?:sample\s+b\s*:)([\s\S]*)/i);
  if (!match) return undefined;
  const clauses = [match[1], match[2]].map((clause) => new Set(tokens(clause)));
  const ranked = (subjectCatalog.sets || []).filter((set) => Array.isArray(set.sampleCoverage) && set.sampleCoverage.length === 2)
    .map((set) => {
      const coverage = set.sampleCoverage.map((terms, index) => tokens(terms.join(" ")).filter((token) => clauses[index].has(token)));
      const score = coverage.every((matches) => matches.length) ? coverage.reduce((total, matches) => total + matches.length, 0) : 0;
      return { set, score };
    })
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score || a.set.id.localeCompare(b.set.id));
  return ranked[0] ? matchedSubjectSet(ranked[0].set.triggers[0], excluded, hardFit) : undefined;
}

const query = value("--query");
const limit = Math.max(1, Math.min(8, Number(value("--limit", mode === "axes" || mode === "refine" ? "4" : "5"))));
const id = value("--id");
const anchorRef = value("--anchor-ref");
const requestedExclusions = new Set(flagValues(["--exclude"]).flatMap((item) => item.split(",")).map((item) => item.trim()).filter(Boolean));
const hardFit = parseHardFit();
if (hardFit && requestedExclusions.size) hardFit.excludedReferences = [...requestedExclusions];
const excluded = new Set(requestedExclusions);
for (const set of subjectCatalog.sets || []) {
  for (let index = 0; index < Math.min(set.referenceIds?.length || 0, set.treatmentLookIds?.length || 0); index += 1) {
    const referenceId = set.referenceIds[index];
    const treatmentId = set.treatmentLookIds[index];
    if (requestedExclusions.has(referenceId)) excluded.add(treatmentId);
    if (requestedExclusions.has(treatmentId)) excluded.add(referenceId);
  }
}
const generationCheck = argv.includes("--generation-check");
const recovery = argv.includes("--recovery");
if (recovery && mode !== "looks") throw new Error("--recovery is only supported for looks");
if (recovery && requestedExclusions.size === 0) throw new Error("--recovery requires --exclude");
const requestedMode = value("--mode");
const executionMode = requestedMode ? EXECUTION_MODES.get(requestedMode.toLowerCase()) : undefined;
const outputContext = value("--output");
if (requestedMode && !executionMode) throw new Error(`Unknown execution mode ${requestedMode}`);
const executionContext = {
  executionModeStatus: executionMode ? "known" : "unknown",
  ...(executionMode ? { executionMode } : {}),
  ...(outputContext ? { outputContext } : {}),
};

let output;
if (mode === "looks") {
  if (!query) throw new Error("looks requires --query");
  const subjectSet = multiSampleSubjectSet(query, excluded, hardFit) || matchedSubjectSet(query, excluded, hardFit);
  const recoveryExhausted = recovery && (!subjectSet || !subjectSet.complete);
  const recoveryCoverageGap = recoveryExhausted ? {
    scope: "recovery",
    status: "recovery-exhausted",
    ...(subjectSet?.id ? { subjectSet: subjectSet.id } : {}),
    reason: subjectSet
      ? `exclusions leave no complete closer route for ${subjectSet.id}`
      : "no eligible closer subject set remains after exclusions",
  } : undefined;
  const responseSubjectSet = recoveryExhausted && subjectSet ? {
    ...subjectSet,
    references: [],
    treatmentLookIds: [],
    ...(subjectSet.hardFit ? {
      hardFit: {
        ...subjectSet.hardFit,
        eligibleCandidates: [],
        traitStudies: [],
        componentStudies: [],
        eligibleTreatmentLookIds: [],
        traitStudyTreatmentLookIds: [],
      },
    } : {}),
  } : subjectSet;
  const resultLimit = hardFit ? limit : (subjectSet?.complete ? 3 : limit);
  const hardFitPacket = subjectSet?.hardFit || (hardFit ? {
    constraints: compactHardFitConstraints(hardFit),
    eligibleCandidates: [],
    traitStudies: [],
    eligibleTreatmentLookIds: [],
    exclusions: [],
    missingCoverage: queryScopeMissingCoverage(),
    complete: false,
  } : undefined);
  const responseHardFitPacket = recoveryExhausted && hardFitPacket ? {
    ...hardFitPacket,
    eligibleCandidates: [],
    traitStudies: [],
    componentStudies: [],
    eligibleTreatmentLookIds: [],
    traitStudyTreatmentLookIds: [],
  } : hardFitPacket;
  output = {
    mode,
    ...executionContext,
    ...(subjectSet?.complete ? { noSearch: true } : {}),
    ...(hardFit && !subjectSet?.complete ? { needsSearch: true } : {}),
    ...(recoveryExhausted ? { recoveryExhausted: true, coverageGap: recoveryCoverageGap } : {}),
    ...(hardFit ? { hardFit: responseHardFitPacket } : {}),
    subjectSet: subjectPacket(responseSubjectSet, true),
    results: recoveryExhausted
      ? []
      : subjectSet?.complete || hardFit
        ? subjectLooks(query, subjectSet, excluded, hardFitPacket, resultLimit)
        : rankedLooks(query, resultLimit, excluded, true),
  };
} else if (mode === "axes") {
  if (!query) throw new Error("axes requires --query");
  output = { mode, ...executionContext, noSearch: true, results: rankedAxes(query, limit) };
} else if (mode === "refine") {
  if (!id || !query) throw new Error("refine requires --id and --query");
  const anchor = looks.find((look) => look.id === id);
  if (!anchor) throw new Error(`Unknown look ${id}`);
  if (anchorRef && !references.has(anchorRef)) throw new Error(`Unknown anchor reference ${anchorRef}`);
  const anchorReferences = anchorRef ? [displayReference(anchorRef)] : (anchor.referenceIds || []).map(displayReference);
  const deltaQuery = requestedDelta(query);
  const routingQuery = `${anchor.id} ${generationCheck ? deltaQuery : query}`;
  const subjectSet = matchedSubjectSet(routingQuery, excluded, hardFit);
  const hardFitPacket = subjectSet?.hardFit || (hardFit ? {
    constraints: compactHardFitConstraints(hardFit),
    eligibleCandidates: [],
    traitStudies: [],
    eligibleTreatmentLookIds: [],
    exclusions: [],
    missingCoverage: queryScopeMissingCoverage(),
    complete: false,
  } : undefined);
  const hardFitIncomplete = Boolean(hardFit && !subjectSet?.complete);
  const compatibleReferences = hardFit
    ? (hardFitPacket?.eligibleCandidates || [])
    : (subjectSet?.references || []);
  const supportingReferences = subjectSet?.complete
    ? compatibleReferences.filter((reference) => reference.id !== anchorRef).slice(0, 2)
    : [];
  const reviewedCombinationGap = generationCheck && subjectSet?.complete && subjectSet.catalogGap;
  output = {
    mode,
    ...executionContext,
    ...(generationCheck
      ? reviewedCombinationGap
        ? { noSearch: true, catalogGap: subjectSet.catalogGap }
        : { needsSearch: true }
      : hardFitIncomplete ? { needsSearch: true } : { noSearch: true }),
    ...(hardFit ? { hardFit: hardFitPacket } : {}),
    subjectSet: subjectPacket(generationCheck && !reviewedCombinationGap && !hardFit ? undefined : subjectSet, Boolean(hardFit)),
    anchor: { ...compactLook(anchor, false), references: anchorReferences, locked: anchor.lockedQualities, adapt: anchor.adaptiveGuidance },
    ...(reviewedCombinationGap && supportingReferences.length ? { combinationComponents: supportingReferences } : {}),
    ...(!generationCheck && supportingReferences.length ? { supportingReferences } : {}),
    deltas: rankedAxes(deltaQuery, limit, !(hardFit && hardFitIncomplete)),
  };
} else if (mode === "profile") {
  if (!id) throw new Error("profile requires --id");
  const look = looks.find((item) => item.id === id);
  if (!look) throw new Error(`Unknown look ${id}`);
  if (anchorRef && !references.has(anchorRef)) throw new Error(`Unknown anchor reference ${anchorRef}`);
  output = {
    mode,
    ...executionContext,
    noSearch: true,
    look: {
      ...compactLook(look, false),
      references: anchorRef ? [displayReference(anchorRef)] : (look.referenceIds || []).map(displayReference),
      locked: look.lockedQualities,
      adapt: look.adaptiveGuidance,
      axisValues: look.axisValues,
      incompatibilities: look.incompatibilities,
    },
  };
} else {
  throw new Error("Usage: query.mjs looks|axes|refine|profile [--query text] [--id look-id] [--anchor-ref reference-id] [--mode ai|photographer|self-shoot|both] [--output text] [--multi-sample] [--generation-check] [--recovery] [--limit n] [--exclude ids] [--hard-constraint subject-count=single|group] [--hard-constraint setting=home-office|office|workshop|industrial-workplace|workplace] [--hard-constraint action=solo-work|group-work|industrial-task|portrait] [--exclude-trait trait]");
}

console.log(JSON.stringify(output));
