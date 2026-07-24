"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const context = { window: null };
context.window = context;
vm.createContext(context);
vm.runInContext(
  fs.readFileSync(path.join(__dirname, "../js/media-runtime.js"), "utf8"),
  context
);

const runtime = context.RotMediaRuntime;
const slug = "marinemuseum-wilhelmshaven";

const roleCases = [
  ["exhibit_video", "Item_800_glow.webm", "800_glow"],
  ["image_800", "Item_800.png", "800"],
  ["source_image", "Item.png", "png"],
  ["preview", "Item_pr.webm", "previews"],
  ["preview_mobile", "Item_mobile_pr.webm", "previews"],
];

for (const [role, filename, folder] of roleCases) {
  const urls = runtime.exhibitUrls(slug, role, filename);
  assert.equal(urls.relative, `exhibits/${slug}/${folder}/${filename}`);
  assert.equal(new URL(urls.primary).pathname, new URL(urls.fallback).pathname);
}

assert.equal(
  runtime.sharedUrls("flag", "germany_wwii.svg").relative,
  "flags/germany_wwii.svg"
);
assert.equal(
  runtime.sharedUrls("hud", "HUD06_Frame.webm").relative,
  "huds/HUD06_Frame.webm"
);
assert.equal(
  runtime.collageUrls("roadsoftimes", "Zorndorf", "desktop").relative,
  "exhibits/roadsoftimes/videos/Zorndorf.webm"
);
assert.equal(
  runtime.collageUrls("roadsoftimes", "Zorndorf", "mobile").relative,
  "exhibits/roadsoftimes/videos/Zorndorf_mobile.webm"
);

for (const invalid of [
  "Großer_Kurfürst_800_glow.webm",
  "Танк_800_glow.webm",
  "BV 206 S_800_glow.webm",
  "assets/item.webm",
  "exhibits/museum/800_glow/item.webm",
  "https://media.roadsoftimes.com/item.webm",
  "missing-extension",
]) {
  assert.throws(
    () => runtime.exhibitUrls("museum", "exhibit_video", invalid),
    /filename|basename|ASCII/
  );
}

assert.throws(() => runtime.exhibitUrls("../museum", "exhibit_video", "item.webm"), /slug/);
assert.throws(() => runtime.exhibitUrls("museum", "unknown", "item.webm"), /Unknown/);
assert.throws(() => runtime.exhibitUrls("museum", "image_800", "item.webm"), /Extension/);
assert.throws(() => runtime.sharedUrls("unknown", "item.png"), /Unknown/);
assert.throws(() => runtime.collageUrls("museum", "item", "tablet"), /layout/);

const custom = runtime.exhibitUrls("museum", "preview", "item.webm", {
  primaryOrigin: "https://primary.example",
  fallbackOrigin: "https://fallback.example",
});
assert.equal(custom.primary, "https://primary.example/exhibits/museum/previews/item.webm");
assert.equal(custom.fallback, "https://fallback.example/exhibits/museum/previews/item.webm");

console.log("Public media runtime contract smoke checks passed");
