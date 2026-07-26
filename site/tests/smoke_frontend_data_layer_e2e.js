"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const siteRoot = path.resolve(__dirname, "..");
const read = relative => fs.readFileSync(path.join(siteRoot, relative), "utf8");
const records = JSON.parse(read("infographics.json"));
const museums = JSON.parse(read("museums.json"));
const museumSlugs = new Map(museums.map(museum => [museum.name, museum.id]));

const context = { window: null };
context.window = context;
vm.createContext(context);
vm.runInContext(read("js/media-runtime.js"), context);
const runtime = context.RotMediaRuntime;
const failures = [];

function validateExhibit(record, role, filename, field) {
  if (!filename) return;
  const slug = museumSlugs.get(record.Museum);
  try {
    runtime.exhibitUrls(slug, role, filename);
  } catch (error) {
    failures.push(`${record.id} · ${field}: ${error.message} (${filename})`);
  }
}

function validateImageZone(record, zone, field) {
  if (!zone || !zone.source || zone.role === "frame") return;
  if (zone.role === "image_flag" || /^flags\//i.test(zone.source)) return;
  if (zone.type === "image" || zone.media_type === "image") {
    validateExhibit(record, "source_image", zone.source, field);
  }
}

for (const record of records) {
  for (const [field, value] of [["video", record.video], ["image", record.image]]) {
    if (!value) continue;
    try {
      runtime.assertAsciiFilename(value);
    } catch (error) {
      failures.push(`${record.id} · ${field}: ${error.message} (${value})`);
    }
  }

  validateExhibit(record, "preview", record.preview, "preview");
  validateExhibit(record, "preview_mobile", record.mobile && record.mobile.preview, "mobile.preview");

  if (record.Category === "Коллажи") continue;
  for (const [prefix, zones] of [
    ["zones", record.zones],
    ["mobile.zones", record.mobile && record.mobile.zones],
  ]) {
    for (const [role, zone] of Object.entries(zones || {})) {
      if (!zone || typeof zone !== "object") continue;
      if (role === "exhibit_video") {
        validateExhibit(record, "exhibit_video", zone.source, `${prefix}.${role}.source`);
        validateExhibit(record, "image_800", zone.source_png, `${prefix}.${role}.source_png`);
      } else {
        validateImageZone(record, zone, `${prefix}.${role}.source`);
      }
    }
  }
}

assert.deepEqual(failures, [], `Invalid frontend media fields:\n${failures.join("\n")}`);

const player = read("js/infographic-player.js");
for (const forbidden of [
  "EXHIBIT_MEDIA_ROLE_DIRS",
  "function _defaultPreviewPath(",
  "function pickPreviewPath(",
  "function previewUrl(",
  "stripSitePrefix",
  "prototype._cdnUrl",
]) {
  assert.ok(!player.includes(forbidden), `player must not retain legacy resolver: ${forbidden}`);
}
assert.ok(player.includes("RotMediaRuntime must load before"), "player fails closed without the shared runtime");
assert.ok(player.includes("global.RotMediaRuntime.collageUrls("), "collages use the typed runtime");

for (const [recordId, expectedHud] of [
  ["Aircraft01", "HUD08"],
  ["SMS Großer Kurfürst", "HUD05"],
]) {
  const record = records.find(item => item.id === recordId);
  assert.ok(record, `${recordId} fixture exists`);
  assert.equal(record.hud_key, expectedHud, `${recordId} retains its explicit HUD key`);
  const desktopHud = runtime.sharedUrls("hud", `${expectedHud}_Frame.webm`);
  const mobileHud = runtime.sharedUrls("hud", `${expectedHud}_Frame_mobile.webm`);
  assert.equal(new URL(desktopHud.primary).pathname, new URL(desktopHud.fallback).pathname);
  assert.equal(new URL(mobileHud.primary).pathname, new URL(mobileHud.fallback).pathname);
}

for (const [recordId, expectedPreview] of [
  ["Aircraft01", "Aircraft01_pr.webm"],
  ["DZVR21", "DZVR21_pr.webm"],
  ["SMS Großer Kurfürst", "SMS_Grosser_Kurfuerst_pr.webm"],
]) {
  const record = records.find(item => item.id === recordId);
  assert.ok(record, `${recordId} preview fixture exists`);
  assert.equal(record.preview, expectedPreview, `${recordId} has an explicit desktop preview binding`);
}

const fixture = records.find(record =>
  record.zones
  && record.zones.exhibit_video
  && /Grosser.*Kurfuerst/i.test(record.zones.exhibit_video.source || "")
);
assert.ok(fixture, "representative Grosser Kurfuerst fixture exists");
const fixtureSlug = museumSlugs.get(fixture.Museum);
const fixtureFilename = fixture.zones.exhibit_video.source;
const urls = runtime.exhibitUrls(fixtureSlug, "exhibit_video", fixtureFilename);
assert.equal(
  urls.relative,
  `exhibits/${fixtureSlug}/800_glow/${fixtureFilename}`,
  "basename record and museum slug produce the canonical relative path"
);
assert.equal(new URL(urls.primary).pathname, new URL(urls.fallback).pathname);

console.log(`Frontend data-layer E2E passed: ${records.length} records, zero invalid media fields`);
