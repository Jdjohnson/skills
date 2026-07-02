#!/usr/bin/env node

import { createHash } from "node:crypto";
import { access, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const CRM_SYNC_LIB_PATH = "dot-runtime/automations/mscrm-sales-sync/lib/sales-crm-sync.mjs";

async function resolveCrmSyncLib() {
  const here = dirname(fileURLToPath(import.meta.url));
  const candidates = [
    resolve(here, "../../../", CRM_SYNC_LIB_PATH),
    resolve(process.cwd(), CRM_SYNC_LIB_PATH),
    process.env.DOT_WORKSPACE ? resolve(process.env.DOT_WORKSPACE, CRM_SYNC_LIB_PATH) : null,
  ].filter(Boolean);

  for (const candidate of candidates) {
    try {
      await access(candidate);
      return import(pathToFileURL(candidate).href);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }

  throw new Error(`Unable to find ${CRM_SYNC_LIB_PATH}; run this skill from a Dot workspace or set DOT_WORKSPACE.`);
}

const {
  CRM_BASE_URL,
  OWNER_EMAIL,
  VALID_STAGES,
  buildSupabaseRestUrl,
  credentialPaths,
  loadEnvFile,
  resolveCredentials,
  resolveOwnerProfile,
  supabaseGet,
} = await resolveCrmSyncLib();

const PACKET_TYPE = "mscrm_new_deal_approval_packet";
const PACKET_VERSION = 1;
const ACTIVE_STAGES = new Set(["first_contact", "discovery", "proposal_writing", "closing", "on_hold"]);

function stableStringify(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map((item) => stableStringify(item)).join(",")}]`;
  return `{${Object.keys(value)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
    .join(",")}}`;
}

function hashObject(value) {
  return createHash("sha256").update(stableStringify(value)).digest("hex");
}

function compactObject(value) {
  return Object.fromEntries(Object.entries(value).filter(([, item]) => item !== undefined && item !== null && item !== ""));
}

function parseArgs(argv) {
  const [mode, ...rest] = argv;
  const args = { mode };
  for (let index = 0; index < rest.length; index += 1) {
    const item = rest[index];
    if (!item.startsWith("--")) throw new Error(`Unexpected argument: ${item}`);
    const key = item.slice(2);
    const next = rest[index + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
    } else {
      args[key] = next;
      index += 1;
    }
  }
  return args;
}

async function readJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

function normalizeDealInput(input) {
  const dealName = input.dealName || input.deal_name;
  const companyName = input.companyName || input.company_name;
  const stage = input.stage;
  const divisionName = input.divisionName || input.division_name || input.division;
  const sourceName = input.sourceName || input.source_name || input.source;
  const ownerEmail = input.ownerEmail || input.owner_email || OWNER_EMAIL;

  const missing = [];
  for (const [field, value] of Object.entries({ dealName, companyName, stage, divisionName, sourceName, ownerEmail })) {
    if (!value) missing.push(field);
  }
  if (missing.length) throw new Error(`Missing required deal field(s): ${missing.join(", ")}`);
  if (!VALID_STAGES.has(stage)) throw new Error(`Invalid stage: ${stage}`);

  return {
    dealName: String(dealName).trim(),
    companyName: String(companyName).trim(),
    companyId: input.companyId || input.company_id || null,
    createCompany: input.createCompany === true || input.create_company === true,
    stage,
    divisionName: String(divisionName).trim(),
    sourceName: String(sourceName).trim(),
    sourceDetail: input.sourceDetail || input.source_detail || null,
    ownerEmail: String(ownerEmail).trim(),
    valueMin: input.valueMin ?? input.value_min ?? null,
    valueMax: input.valueMax ?? input.value_max ?? null,
    expectedCloseDate: input.expectedCloseDate || input.expected_close_date || null,
    primaryContact: input.primaryContact || input.primary_contact || null,
    note: input.note || null,
  };
}

async function findRowsByName({ credentials, table, name, fetchImpl }) {
  return supabaseGet({
    credentials,
    table,
    params: { select: "id,name", name: `ilike.${name}` },
    fetchImpl,
  });
}

async function resolveNamedReference({ credentials, table, name, fetchImpl }) {
  const rows = await findRowsByName({ credentials, table, name, fetchImpl });
  if (rows.length !== 1) {
    throw new Error(`Expected exactly one ${table} row named "${name}", found ${rows.length}`);
  }
  return rows[0];
}

async function resolveCompany({ credentials, deal, fetchImpl }) {
  if (deal.companyId) {
    const rows = await supabaseGet({
      credentials,
      table: "companies",
      params: { select: "id,name", id: `eq.${deal.companyId}` },
      fetchImpl,
    });
    if (rows.length !== 1) throw new Error(`Company ID not found: ${deal.companyId}`);
    return { status: "existing_by_id", row: rows[0] };
  }

  const rows = await findRowsByName({ credentials, table: "companies", name: deal.companyName, fetchImpl });
  if (rows.length === 1) return { status: "existing_by_name", row: rows[0] };
  if (rows.length > 1) throw new Error(`Company name "${deal.companyName}" matched ${rows.length} rows; provide companyId`);
  if (!deal.createCompany) throw new Error(`Company "${deal.companyName}" not found and createCompany is not true`);
  return { status: "create_on_approved_run", row: null };
}

async function findDuplicateDeals({ credentials, ownerId, companyId, dealName, fetchImpl }) {
  if (!companyId) return [];
  const rows = await supabaseGet({
    credentials,
    table: "deals",
    params: {
      select: "id,deal_name,stage,company_id",
      owner_id: `eq.${ownerId}`,
      company_id: `eq.${companyId}`,
      stage: "neq.deleted",
    },
    fetchImpl,
  });
  const target = dealName.toLowerCase();
  return rows.filter((row) => ACTIVE_STAGES.has(row.stage) || String(row.deal_name || "").toLowerCase() === target);
}

export async function buildApprovalPacket({ input, env = process.env, fetchImpl = globalThis.fetch }) {
  const deal = normalizeDealInput(input);
  const credentials = resolveCredentials(env);
  const owner = await resolveOwnerProfile({ credentials, ownerEmail: deal.ownerEmail, fetchImpl });
  const division = await resolveNamedReference({ credentials, table: "divisions", name: deal.divisionName, fetchImpl });
  const source = await resolveNamedReference({ credentials, table: "sources", name: deal.sourceName, fetchImpl });
  const company = await resolveCompany({ credentials, deal, fetchImpl });
  const duplicates = await findDuplicateDeals({
    credentials,
    ownerId: owner.id,
    companyId: company.row?.id,
    dealName: deal.dealName,
    fetchImpl,
  });

  const approvalMaterial = {
    action: "create-mscrm-deal",
    version: PACKET_VERSION,
    deal: {
      ...deal,
      companyId: company.row?.id || deal.companyId || null,
      companyName: company.row?.name || deal.companyName,
      ownerId: owner.id,
      divisionId: division.id,
      divisionName: division.name,
      sourceId: source.id,
      sourceName: source.name,
      createdByAi: true,
    },
    checks: {
      companyStatus: company.status,
      duplicateDeals: duplicates.map((row) => ({
        id: row.id,
        dealName: row.deal_name,
        stage: row.stage,
      })),
      slackRoute: "SLACK_DEAL_WEBHOOK_URL",
    },
  };
  const approvalId = hashObject(approvalMaterial).slice(0, 16);

  return {
    type: PACKET_TYPE,
    approval_id: approvalId,
    required_approval_text: `I approve creating MSCRM deal ${approvalId}`,
    approval_material: approvalMaterial,
  };
}

function resolveSlackWebhook(env = process.env) {
  if (env.SLACK_DEAL_WEBHOOK_URL) return { value: env.SLACK_DEAL_WEBHOOK_URL, source: "environment" };
  for (const filePath of credentialPaths(env)) {
    const fileEnv = loadEnvFile(filePath);
    if (fileEnv.SLACK_DEAL_WEBHOOK_URL) {
      return { value: fileEnv.SLACK_DEAL_WEBHOOK_URL, source: filePath };
    }
  }
  return { value: "", source: "" };
}

export function approvalTextMatchesPacket({ packet, approvalText }) {
  if (approvalText === packet.required_approval_text) return true;

  const normalized = String(approvalText || "")
    .trim()
    .toLowerCase()
    .replace(/[.!?]+$/g, "")
    .replace(/\s+/g, " ");

  const approvalId = String(packet.approval_id || "").toLowerCase();
  const naturalApprovals = new Set([
    "approved",
    "this is approved",
    "this is approved.",
    "approve",
    "i approve",
    "go ahead",
    "go for it",
    "create it",
    "create the deal",
    "create the crm deal",
    "create the mscrm deal",
    "add it",
    "add it to crm",
    "add it to mscrm",
    "add to crm",
    "add to mscrm",
    "post it",
    "post it to slack",
    "post the ad",
    "post the add",
    "send it to slack",
  ]);

  if (naturalApprovals.has(normalized)) return true;
  if (approvalId && normalized === `approved ${approvalId}`) return true;
  if (approvalId && normalized === `approve ${approvalId}`) return true;
  if (approvalId && normalized === `create ${approvalId}`) return true;

  return false;
}

function verifyApproval({ packet, approvedBy, approvalText }) {
  if (packet.type !== PACKET_TYPE) throw new Error(`Invalid packet type: ${packet.type}`);
  if (approvedBy !== "Jarad Johnson") throw new Error("Create blocked: approved-by must be Jarad Johnson");
  const expectedId = hashObject(packet.approval_material).slice(0, 16);
  if (packet.approval_id !== expectedId) throw new Error("Create blocked: approval packet hash mismatch");
  if (!approvalTextMatchesPacket({ packet, approvalText })) {
    throw new Error(
      `Create blocked: approval text must explicitly approve packet "${packet.approval_id}" or equal "${packet.required_approval_text}"`,
    );
  }
  return { status: "approved", approvedBy, approvalId: packet.approval_id };
}

async function supabasePost({ credentials, table, body, fetchImpl = globalThis.fetch }) {
  const response = await fetchImpl(buildSupabaseRestUrl(credentials.url, table), {
    method: "POST",
    headers: {
      apikey: credentials.key,
      Authorization: `Bearer ${credentials.key}`,
      "Content-Type": "application/json",
      Prefer: "return=representation",
    },
    body: JSON.stringify(body),
  });
  const text = await response.text();
  if (!response.ok) throw new Error(`Supabase POST ${table} failed with HTTP ${response.status}: ${text}`);
  const rows = text ? JSON.parse(text) : [];
  if (!Array.isArray(rows) || !rows.length) throw new Error(`Supabase POST ${table} returned no rows`);
  return rows[0];
}

async function ensureCompany({ credentials, deal, fetchImpl }) {
  if (deal.companyId) return { id: deal.companyId, name: deal.companyName };
  if (!deal.createCompany) throw new Error("Create blocked: packet does not allow company creation");
  return supabasePost({
    credentials,
    table: "companies",
    body: { name: deal.companyName },
    fetchImpl,
  });
}

async function createOptionalContact({ credentials, dealId, companyId, contact, fetchImpl }) {
  if (!contact) return null;
  if (!contact.name && !contact.email) throw new Error("Primary contact requires at least name or email");
  const createdContact = await supabasePost({
    credentials,
    table: "contacts",
    body: compactObject({
      company_id: companyId,
      name: contact.name,
      email: contact.email,
      phone: contact.phone,
      title: contact.title,
      created_by_ai: true,
    }),
    fetchImpl,
  });
  await supabasePost({
    credentials,
    table: "deal_contacts",
    body: { deal_id: dealId, contact_id: createdContact.id, is_primary: true },
    fetchImpl,
  });
  return createdContact;
}

async function createOptionalNote({ credentials, dealId, ownerId, note, fetchImpl }) {
  if (!note) return null;
  return supabasePost({
    credentials,
    table: "deal_notes",
    body: {
      deal_id: dealId,
      author_id: ownerId,
      body: note,
    },
    fetchImpl,
  });
}

function titleCaseStage(stage) {
  return String(stage || "")
    .split("_")
    .filter(Boolean)
    .map((part) => `${part.slice(0, 1).toUpperCase()}${part.slice(1)}`)
    .join(" ");
}

function nameFromEmail(email) {
  const localPart = String(email || "").split("@")[0];
  if (!localPart) return "";
  return localPart
    .split(/[._-]+/)
    .filter(Boolean)
    .map((part) => `${part.slice(0, 1).toUpperCase()}${part.slice(1)}`)
    .join(" ");
}

function formatMoney(value) {
  if (value === null || value === undefined || value === "") return "";
  const number = Number(value);
  if (!Number.isFinite(number)) return String(value);
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(number);
}

function formatValueRange(deal) {
  const min = formatMoney(deal.valueMin);
  const max = formatMoney(deal.valueMax);
  if (min && max && min !== max) return `${min} - ${max}`;
  return min || max || "-";
}

export function buildSlackNotificationPayload({ deal, crmDeal, company, contact }) {
  const dealUrl = `${CRM_BASE_URL}/deals/${crmDeal.id}`;
  const primaryPerson = contact?.name || deal.primaryContact?.name || "-";
  const owner = nameFromEmail(deal.ownerEmail) || deal.ownerEmail || "-";
  const fields = [
    { title: "Company", value: company.name || deal.companyName || "-", short: true },
    { title: "Primary person", value: primaryPerson, short: true },
    { title: "Owner", value: owner, short: true },
    { title: "Stage", value: titleCaseStage(deal.stage) || "-", short: true },
    { title: "Value", value: formatValueRange(deal), short: true },
  ];

  return {
    text: `New deal: ${deal.dealName}`,
    attachments: [
      {
        fallback: `New deal: ${deal.dealName} - ${dealUrl}`,
        color: "#ff5a1f",
        pretext: `:new: New deal: ${deal.dealName}`,
        title: deal.dealName,
        title_link: dealUrl,
        fields,
        actions: [
          {
            type: "button",
            text: "Open deal",
            url: dealUrl,
          },
        ],
        footer: "Added by MSCRM",
      },
    ],
  };
}

async function postSlackNotification({ webhookUrl, deal, crmDeal, company, contact, fetchImpl }) {
  const payload = buildSlackNotificationPayload({ deal, crmDeal, company, contact });
  const response = await fetchImpl(webhookUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const text = await response.text();
  if (!response.ok) throw new Error(`Slack notification failed with HTTP ${response.status}: ${text}`);
  return { status: "sent", dealUrl: `${CRM_BASE_URL}/deals/${crmDeal.id}` };
}

export async function createApprovedDeal({
  packet,
  approvedBy,
  approvalText,
  env = process.env,
  fetchImpl = globalThis.fetch,
}) {
  const approval = verifyApproval({ packet, approvedBy, approvalText });
  const slackWebhook = resolveSlackWebhook(env);
  if (!slackWebhook.value) {
    throw new Error("Create blocked: SLACK_DEAL_WEBHOOK_URL is not configured");
  }

  const credentials = resolveCredentials(env);
  const deal = packet.approval_material.deal;
  const company = await ensureCompany({ credentials, deal, fetchImpl });
  const crmDeal = await supabasePost({
    credentials,
    table: "deals",
    body: compactObject({
      deal_name: deal.dealName,
      company_id: company.id,
      owner_id: deal.ownerId,
      division_id: deal.divisionId,
      source_id: deal.sourceId,
      source_detail: deal.sourceDetail,
      stage: deal.stage,
      value_min: deal.valueMin,
      value_max: deal.valueMax,
      expected_close_date: deal.expectedCloseDate,
      created_by_ai: true,
    }),
    fetchImpl,
  });

  const contact = await createOptionalContact({
    credentials,
    dealId: crmDeal.id,
    companyId: company.id,
    contact: deal.primaryContact,
    fetchImpl,
  });
  const note = await createOptionalNote({
    credentials,
    dealId: crmDeal.id,
    ownerId: deal.ownerId,
    note: deal.note,
    fetchImpl,
  });

  let slack;
  try {
    slack = await postSlackNotification({ webhookUrl: slackWebhook.value, deal, crmDeal, company, contact, fetchImpl });
  } catch (error) {
    return {
      ok: false,
      approval,
      crm: {
        status: "created",
        dealId: crmDeal.id,
        dealUrl: `${CRM_BASE_URL}/deals/${crmDeal.id}`,
        companyId: company.id,
        contactId: contact?.id || null,
        noteId: note?.id || null,
      },
      slack: { status: "failed", error: error.message },
      errors: [error.message],
    };
  }

  return {
    ok: true,
    approval,
    crm: {
      status: "created",
      dealId: crmDeal.id,
      dealUrl: `${CRM_BASE_URL}/deals/${crmDeal.id}`,
      companyId: company.id,
      contactId: contact?.id || null,
      noteId: note?.id || null,
    },
    slack,
    errors: [],
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.mode === "preview") {
    if (!args.input) throw new Error("preview requires --input <deal.json>");
    const packet = await buildApprovalPacket({ input: await readJson(args.input) });
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
    return;
  }
  if (args.mode === "create") {
    if (!args.packet) throw new Error("create requires --packet <approval-packet.json>");
    const receipt = await createApprovedDeal({
      packet: await readJson(args.packet),
      approvedBy: args["approved-by"],
      approvalText: args["approval-text"],
    });
    process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
    process.exitCode = receipt.ok ? 0 : 1;
    return;
  }
  throw new Error("Usage: create-deal.mjs <preview|create> [options]");
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 2;
  });
}
