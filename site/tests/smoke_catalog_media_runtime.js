"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const source = fs.readFileSync(path.join(__dirname, "../index.html"), "utf8");

const runtimeAt = source.indexOf('<script src="/js/media-runtime.js?v=fe3"></script>');
const catalogAt = source.indexOf("function catalogMediaPrimary(");
assert.ok(runtimeAt >= 0, "static catalog loads media runtime");
assert.ok(catalogAt > runtimeAt, "media runtime loads before catalog resolver calls");

assert.ok(
  source.includes("window.RotMediaRuntime.exhibitUrls(slug, role, filename"),
  "catalog delegates exhibit URL construction to shared runtime"
);
assert.ok(
  source.includes("catalogMediaPrimary(r, 'image_800', src)"),
  "catalog PNG thumbnails use image_800 role"
);
assert.ok(
  source.includes("catalogMediaPrimary(r, 'exhibit_video', src)"),
  "catalog animated thumbnails use exhibit_video role"
);
assert.ok(
  source.includes("catalogMediaPrimary(r, suffix ? 'preview_mobile' : 'preview', src)"),
  "catalog previews select the typed desktop/mobile role"
);
assert.ok(
  !source.includes("MEDIA_CDN + '/exhibits/'"),
  "static catalog contains no manual exhibit URL concatenation"
);

console.log("Static catalog media runtime smoke checks passed");
