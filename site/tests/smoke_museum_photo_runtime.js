"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const siteRoot = path.resolve(__dirname, "..");
const repoRoot = path.resolve(siteRoot, "..");
const museums = JSON.parse(fs.readFileSync(path.join(siteRoot, "museums.json"), "utf8"));
const full = fs.readFileSync(path.join(repoRoot, "template/blogger-museums.html"), "utf8");
const widget = fs.readFileSync(path.join(repoRoot, "template/blogger-museums-widget.html"), "utf8");
const editor = fs.readFileSync(path.join(siteRoot, "museums.html"), "utf8");

for (const museum of museums) {
  assert.match(museum.id, /^[a-z0-9]+(?:-[a-z0-9]+)*$/, `${museum.id}: canonical slug`);
  if (!museum.photo) continue;
  assert.match(
    museum.photo,
    /^[A-Za-z0-9][A-Za-z0-9._-]*\.[A-Za-z0-9]+$/,
    `${museum.id}: basename-only photo`
  );
  assert.ok(
    fs.existsSync(path.join(siteRoot, "media-site/exhibits", museum.id, museum.photo)),
    `${museum.id}: canonical local photo exists`
  );
}

for (const [name, source] of [["museums", full], ["widget", widget], ["editor", editor]]) {
  assert.ok(source.includes("'museum_photo'"), `${name} uses the typed museum photo role`);
  assert.ok(source.includes("RotMediaRuntime.exhibitUrls"), `${name} uses the shared runtime`);
}
assert.ok(full.includes("data-museum-photo-fallback"), "museums page exposes bounded fallback state");
assert.ok(widget.includes("data-museum-photo-fallback"), "featured widget exposes bounded fallback state");
assert.ok(!full.includes("src=\"' + esc(r.photo)"), "museums page never treats photo as a URL");
assert.ok(!widget.includes("src=\"' + esc(r.photo"), "widget never treats photo as a URL");
assert.ok(
  !full.includes("r.landing_url ? 'window.location.href="),
  "museum cards and table rows always open the detail card"
);
assert.ok(
  full.includes("meta.push('<a class=\"landing\""),
  "detail card exposes a separate landing-page link"
);

console.log(`Museum photo runtime checks passed (${museums.length} records)`);
