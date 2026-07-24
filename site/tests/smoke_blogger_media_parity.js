"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const repoRoot = path.resolve(__dirname, "../..");
const read = (relative) => fs.readFileSync(path.join(repoRoot, relative), "utf8");

const catalog = read("template/blogger-catalog.html");
const runtimeAt = catalog.indexOf("js/media-runtime.js?v=fe4");
const resolverAt = catalog.indexOf("function catalogMediaPrimary(");
assert.ok(runtimeAt >= 0 && resolverAt > runtimeAt, "Blogger catalog loads runtime before resolving media");
assert.ok(catalog.includes("RotMediaRuntime.exhibitUrls(slug, role, filename"), "Blogger catalog uses shared runtime");
assert.ok(catalog.includes("catalogMediaPrimary(r, 'image_800', src)"), "Blogger catalog uses image role");
assert.ok(catalog.includes("catalogMediaPrimary(r, 'exhibit_video', src)"), "Blogger catalog uses video role");
assert.ok(
  catalog.includes("catalogMediaPrimary(r, suffix ? 'preview_mobile' : 'preview', src)"),
  "Blogger catalog uses typed preview roles"
);
assert.ok(!catalog.includes("MEDIA_CDN + '/exhibits/'"), "Blogger catalog has no manual exhibit paths");

for (const relative of ["template/blogger-exhibit.html", "template/blogger-widget.html"]) {
  const source = read(relative);
  const runtime = source.indexOf("js/media-runtime.js?v=fe4");
  const player = source.indexOf("js/infographic-player.js?v=fe4");
  assert.ok(runtime >= 0 && player > runtime, `${relative} loads runtime before player`);
}

for (const relative of ["template/blogger-hud-strip.html", "tools/museums/test-hud-strip.html"]) {
  const source = read(relative);
  assert.ok(source.includes("RotMediaRuntime.exhibitUrls("), `${relative} uses shared preview resolver`);
  assert.ok(source.includes("data-fallback="), `${relative} exposes fallback URL`);
  assert.ok(source.includes("hs-thumb-missing"), `${relative} exposes missing-preview state`);
  assert.ok(!source.includes("MEDIA_CDN + '/previews/'"), `${relative} has no flat preview path`);
  assert.ok(!source.includes("+ e.id + suffix"), `${relative} does not infer preview names`);
}

console.log("Blogger media parity smoke checks passed");
