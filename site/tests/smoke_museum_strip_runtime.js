"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const source = fs.readFileSync(
  path.join(__dirname, "../../template/blogger-hud-strip.html"),
  "utf8"
);

assert.ok(source.includes("RotMediaRuntime.exhibitUrls("), "strip uses shared runtime");
assert.ok(source.includes("mobile ? 'preview_mobile' : 'preview'"), "strip uses typed preview roles");
assert.ok(source.includes("data-fallback="), "strip carries the matching fallback URL");
assert.ok(source.includes("dataset.fallbackUsed"), "strip retries fallback at most once");
assert.ok(source.includes("hs-thumb-missing"), "strip exposes missing preview state");
assert.ok(!source.includes("function mediaUrl("), "strip accepts no arbitrary stored path");
assert.ok(!source.includes("MEDIA_CDN + '/previews/'"), "strip has no flat preview fallback");
assert.ok(!source.includes("+ e.id + suffix"), "strip does not infer preview filenames from record ids");

console.log("Museum strip media runtime smoke checks passed");
