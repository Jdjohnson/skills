import assert from "node:assert/strict";
import test from "node:test";

import {
  approvalTextMatchesPacket,
  buildApprovalPacket,
  buildSlackNotificationPayload,
  createApprovedDeal,
} from "../scripts/create-deal.mjs";

const env = {
  SUPABASE_URL: "https://example.supabase.co",
  SUPABASE_KEY: "test-key",
  SLACK_DEAL_WEBHOOK_URL: "https://hooks.slack.test/deal",
};

const dealInput = {
  dealName: "AI Inquiry + Quote Readiness POC",
  companyName: "Positronic",
  stage: "discovery",
  divisionName: "MSAI",
  sourceName: "REFERRAL",
  sourceDetail: "JMARK referral",
  ownerEmail: "jarad.johnson@mostlyserious.io",
  note: "Initial note",
};

function response(status, body) {
  return {
    ok: status >= 200 && status < 300,
    status,
    text: async () => (typeof body === "string" ? body : JSON.stringify(body)),
  };
}

function routeFetch({ crmPostStatus = 201, slackStatus = 200 } = {}) {
  const calls = [];
  const fetchImpl = async (url, options = {}) => {
    calls.push({ url: String(url), options });
    const path = String(url);
    if (path.includes("/profiles")) return response(200, [{ id: "owner-1", email: dealInput.ownerEmail }]);
    if (path.includes("/divisions")) return response(200, [{ id: "division-1", name: "MSAI" }]);
    if (path.includes("/sources")) return response(200, [{ id: "source-1", name: "REFERRAL" }]);
    if (path.includes("/companies") && options.method !== "POST") return response(200, [{ id: "company-1", name: "Positronic" }]);
    if (path.includes("/deals") && options.method !== "POST") return response(200, []);
    if (path.includes("/deals") && options.method === "POST") {
      return response(crmPostStatus, crmPostStatus >= 400 ? "crm failed" : [{ id: "deal-1", created_at: "now" }]);
    }
    if (path.includes("/deal_notes")) return response(201, [{ id: "note-1" }]);
    if (path === env.SLACK_DEAL_WEBHOOK_URL) return response(slackStatus, slackStatus >= 400 ? "slack failed" : "ok");
    throw new Error(`Unexpected fetch: ${path}`);
  };
  return { calls, fetchImpl };
}

async function packetFor(fetchImpl) {
  return buildApprovalPacket({ input: dealInput, env, fetchImpl });
}

test("preview emits a canonical approval id and exact approval text", async () => {
  const { fetchImpl } = routeFetch();
  const packet = await packetFor(fetchImpl);
  assert.equal(packet.type, "mscrm_new_deal_approval_packet");
  assert.match(packet.approval_id, /^[a-f0-9]{16}$/);
  assert.equal(packet.required_approval_text, `I approve creating MSCRM deal ${packet.approval_id}`);
});

test("create without Jarad approval creates no CRM record", async () => {
  const { calls, fetchImpl } = routeFetch();
  const packet = await packetFor(fetchImpl);
  await assert.rejects(
    () =>
      createApprovedDeal({
        packet,
        approvedBy: "Someone Else",
        approvalText: packet.required_approval_text,
        env,
        fetchImpl,
      }),
    /approved-by must be Jarad Johnson/,
  );
  assert.equal(calls.filter((call) => call.options.method === "POST").length, 0);
});

test("natural-language approval text is accepted for the current packet", async () => {
  const { calls, fetchImpl } = routeFetch();
  const packet = await packetFor(fetchImpl);
  assert.equal(approvalTextMatchesPacket({ packet, approvalText: "approved" }), true);
  assert.equal(approvalTextMatchesPacket({ packet, approvalText: "this is approved" }), true);
  assert.equal(approvalTextMatchesPacket({ packet, approvalText: "add it to MSCRM" }), true);
  assert.equal(approvalTextMatchesPacket({ packet, approvalText: "post the ad" }), true);
  assert.equal(approvalTextMatchesPacket({ packet, approvalText: "not yet" }), false);

  const receipt = await createApprovedDeal({
    packet,
    approvedBy: "Jarad Johnson",
    approvalText: "approved",
    env,
    fetchImpl,
  });
  assert.equal(receipt.ok, true);
  assert.equal(receipt.crm.status, "created");
  assert.equal(receipt.slack.status, "sent");
  assert.equal(calls.some((call) => call.url === env.SLACK_DEAL_WEBHOOK_URL), true);
});

test("unapproved natural text creates no CRM record", async () => {
  const { calls, fetchImpl } = routeFetch();
  const packet = await packetFor(fetchImpl);
  await assert.rejects(
    () =>
      createApprovedDeal({
        packet,
        approvedBy: "Jarad Johnson",
        approvalText: "not yet",
        env,
        fetchImpl,
      }),
    /approval text must explicitly approve packet/,
  );
  assert.equal(calls.filter((call) => call.options.method === "POST").length, 0);
});

test("missing Slack webhook blocks before CRM creation", async () => {
  const { calls, fetchImpl } = routeFetch();
  const packet = await packetFor(fetchImpl);
  await assert.rejects(
    () =>
      createApprovedDeal({
        packet,
        approvedBy: "Jarad Johnson",
        approvalText: packet.required_approval_text,
        env: {
          SUPABASE_URL: env.SUPABASE_URL,
          SUPABASE_KEY: env.SUPABASE_KEY,
          DOT_CRM_ENV_PATH: "/tmp/ms-crm-test-missing.env",
        },
        fetchImpl,
      }),
    /SLACK_DEAL_WEBHOOK_URL is not configured/,
  );
  assert.equal(calls.filter((call) => call.options.method === "POST").length, 0);
});

test("approved create posts CRM before Slack", async () => {
  const { calls, fetchImpl } = routeFetch();
  const packet = await packetFor(fetchImpl);
  const receipt = await createApprovedDeal({
    packet,
    approvedBy: "Jarad Johnson",
    approvalText: packet.required_approval_text,
    env,
    fetchImpl,
  });
  assert.equal(receipt.ok, true);
  assert.equal(receipt.crm.status, "created");
  assert.equal(receipt.slack.status, "sent");
  const postUrls = calls.filter((call) => call.options.method === "POST").map((call) => call.url);
  assert.match(postUrls[0], /\/rest\/v1\/deals$/);
  assert.equal(postUrls.at(-1), env.SLACK_DEAL_WEBHOOK_URL);

  const noteCall = calls.find((call) => call.url.includes("/deal_notes") && call.options.method === "POST");
  const noteBody = JSON.parse(noteCall.options.body);
  assert.equal(noteBody.body, "Initial note");
  assert.equal(noteBody.author_id, "owner-1");
  assert.equal("note" in noteBody, false);
  assert.equal("profile_id" in noteBody, false);
  assert.equal("created_by_ai" in noteBody, false);

  const slackCall = calls.find((call) => call.url === env.SLACK_DEAL_WEBHOOK_URL);
  const slackPayload = JSON.parse(slackCall.options.body);
  assert.equal(slackPayload.text, "New deal: AI Inquiry + Quote Readiness POC");
  assert.equal(slackPayload.attachments[0].pretext, ":new: New deal: AI Inquiry + Quote Readiness POC");
  assert.equal(slackPayload.attachments[0].title, "AI Inquiry + Quote Readiness POC");
  assert.equal(slackPayload.attachments[0].title_link, "https://mscrm.vercel.app/deals/deal-1");
  assert.deepEqual(
    slackPayload.attachments[0].fields.map((field) => [field.title, field.value, field.short]),
    [
      ["Company", "Positronic", true],
      ["Primary person", "-", true],
      ["Owner", "Jarad Johnson", true],
      ["Stage", "Discovery", true],
      ["Value", "-", true],
    ],
  );
  assert.equal(slackPayload.attachments[0].actions[0].text, "Open deal");
});

test("Slack payload includes contact and value fields when present", () => {
  const payload = buildSlackNotificationPayload({
    deal: {
      ...dealInput,
      valueMin: 10000,
      valueMax: 15000,
      primaryContact: { name: "Ryan Haas" },
    },
    crmDeal: { id: "deal-2" },
    company: { name: "Paul Mueller Company" },
    contact: { name: "Ryan Haas" },
  });

  assert.equal(payload.text, "New deal: AI Inquiry + Quote Readiness POC");
  assert.equal(payload.attachments[0].fields.find((field) => field.title === "Primary person").value, "Ryan Haas");
  assert.equal(payload.attachments[0].fields.find((field) => field.title === "Value").value, "$10,000 - $15,000");
});

test("CRM creation failure prevents Slack post", async () => {
  const { calls, fetchImpl } = routeFetch({ crmPostStatus: 500 });
  const packet = await packetFor(fetchImpl);
  await assert.rejects(
    () =>
      createApprovedDeal({
        packet,
        approvedBy: "Jarad Johnson",
        approvalText: packet.required_approval_text,
        env,
        fetchImpl,
      }),
    /Supabase POST deals failed/,
  );
  assert.equal(calls.some((call) => call.url === env.SLACK_DEAL_WEBHOOK_URL), false);
});

test("Slack failure reports CRM created and Slack failed", async () => {
  const { fetchImpl } = routeFetch({ slackStatus: 500 });
  const packet = await packetFor(fetchImpl);
  const receipt = await createApprovedDeal({
    packet,
    approvedBy: "Jarad Johnson",
    approvalText: packet.required_approval_text,
    env,
    fetchImpl,
  });
  assert.equal(receipt.ok, false);
  assert.equal(receipt.crm.status, "created");
  assert.equal(receipt.slack.status, "failed");
  assert.match(receipt.errors[0], /Slack notification failed/);
});
