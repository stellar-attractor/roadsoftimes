"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

class FakeMedia {
  constructor() {
    this.listeners = {};
    this.assignments = [];
  }

  addEventListener(name, listener) {
    (this.listeners[name] ||= []).push(listener);
  }

  set src(value) {
    this.assignments.push(value);
    this._src = value;
  }

  get src() {
    return this._src;
  }

  emit(name) {
    for (const listener of this.listeners[name] || []) listener();
  }
}

const context = {
  window: null,
  navigator: { userAgent: "node" },
  URL,
  URLSearchParams,
  console: { warn() {} }
};
context.window = context;
vm.createContext(context);
vm.runInContext(
  fs.readFileSync(path.join(__dirname, "../js/media-runtime.js"), "utf8"),
  context
);
vm.runInContext(
  fs.readFileSync(path.join(__dirname, "../js/infographic-player.js"), "utf8"),
  context
);

assert.equal(
  context.RotExhibit.mediaRuntime,
  context.RotMediaRuntime,
  "player delegates public URL construction to the shared runtime"
);

const urls = context.RotExhibit.buildExhibitMediaUrls(
  "marinemuseum-wilhelmshaven",
  "exhibit_video",
  "SMS_Grosser_Kurfuerst_800_glow.webm"
);
assert.equal(
  urls.primary,
  "https://media.roadsoftimes.com/exhibits/marinemuseum-wilhelmshaven/800_glow/SMS_Grosser_Kurfuerst_800_glow.webm"
);
assert.equal(
  urls.fallback,
  "https://media-roadsoftimes.pages.dev/exhibits/marinemuseum-wilhelmshaven/800_glow/SMS_Grosser_Kurfuerst_800_glow.webm"
);
assert.equal(new URL(urls.primary).pathname, new URL(urls.fallback).pathname);

const primarySuccess = new FakeMedia();
context.RotExhibit.bindMediaFallback(primarySuccess, urls);
assert.deepEqual(primarySuccess.assignments, [urls.primary]);

const fallbackSuccess = new FakeMedia();
context.RotExhibit.bindMediaFallback(fallbackSuccess, urls);
fallbackSuccess.emit("error");
assert.deepEqual(fallbackSuccess.assignments, [urls.primary, urls.fallback]);

const totalFailure = new FakeMedia();
const states = [];
context.RotExhibit.bindMediaFallback(totalFailure, urls, detail => states.push(detail.status));
totalFailure.emit("error");
totalFailure.emit("error");
totalFailure.emit("error");
assert.deepEqual(totalFailure.assignments, [urls.primary, urls.fallback]);
assert.deepEqual(states, ["fallback", "failed"]);

assert.throws(
  () => context.RotExhibit.buildExhibitMediaUrls("museum", "exhibit_video", "Großer.webm"),
  /ASCII/
);
assert.throws(
  () => context.RotExhibit.buildExhibitMediaUrls("museum", "exhibit_video", "folder/item.webm"),
  /basename/
);

const staticCatalog = fs.readFileSync(path.join(__dirname, "../index.html"), "utf8");
const runtimeLoaderAt = staticCatalog.indexOf("/js/media-runtime.js?v=fe2");
const playerLoaderAt = staticCatalog.indexOf("/js/infographic-player.js?v=fe2");
assert.ok(runtimeLoaderAt >= 0, "static catalog loads the shared media runtime");
assert.ok(playerLoaderAt > runtimeLoaderAt, "static catalog declares runtime before player");

console.log("Site exhibit media URL/fallback smoke checks passed");
