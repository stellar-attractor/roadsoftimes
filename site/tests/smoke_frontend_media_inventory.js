"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const siteRoot = path.resolve(__dirname, "..");
const repoRoot = path.resolve(siteRoot, "..");

function read(relative) {
  return fs.readFileSync(path.join(repoRoot, relative), "utf8");
}

const consumers = Object.freeze({
  "site/js/infographic-player.js": [
    "buildExhibitMediaUrls",
    "bindMediaFallback",
    "_collageVideoPath",
  ],
  "site/index.html": [
    "function pngSrc(",
    "function glowSrc(",
    "function previewSrc(",
    "MEDIA_CDN_FALLBACK",
  ],
  "template/blogger-catalog.html": [
    "function pngSrc(",
    "function glowSrc(",
    "function previewSrc(",
    "MEDIA_CDN_FALLBACK",
  ],
  "template/blogger-hud-strip.html": [
    "function mediaUrl(",
    "function previewSrc(",
    "RotExhibit.init",
  ],
  "template/blogger-exhibit.html": ["RotExhibit.init"],
  "tools/museums/test-hud-strip.html": ["function previewSrc("],
});

for (const [relative, markers] of Object.entries(consumers)) {
  const source = read(relative);
  for (const marker of markers) {
    assert.ok(source.includes(marker), `${relative} must retain inventoried consumer: ${marker}`);
  }
}

const player = read("site/js/infographic-player.js");
for (const role of ["exhibit_video", "image_800", "source_image", "preview", "preview_mobile"]) {
  assert.ok(player.includes(`${role}:`), `player role registry must include ${role}`);
}

const strip = read("template/blogger-hud-strip.html");
assert.ok(
  strip.includes("if (/^https?:\\/\\//i.test(path)) return path;"),
  "FE-0 freezes arbitrary URL acceptance in museum strip until FE-3/FE-4"
);
assert.ok(
  strip.includes("return MEDIA_CDN + '/previews/' + e.id + suffix; // legacy fallback"),
  "FE-0 freezes flat preview fallback until FE-3/FE-4"
);

const oldStripCopy = read("tools/museums/test-hud-strip.html");
assert.ok(
  oldStripCopy.includes("MEDIA_CDN + '/previews/' + e.id + suffix"),
  "FE-0 freezes stale test-copy preview path until FE-4"
);

console.log("Frontend media consumer inventory baseline passed");
