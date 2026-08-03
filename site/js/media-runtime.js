/**
 * Roads of Times public media runtime.
 *
 * Pure path/URL functions only. Catalog fields contain filenames; this module
 * owns the conversion to public primary and fallback URLs.
 */
(function initRotMediaRuntime(global) {
  "use strict";

  if (global.RotMediaRuntime) return;

  var DEFAULT_PRIMARY_ORIGIN = "https://media.roadsoftimes.com";
  var DEFAULT_FALLBACK_ORIGIN = "https://media-roadsoftimes.pages.dev";

  var EXHIBIT_ROLES = Object.freeze({
    exhibit_video: Object.freeze({ folder: "800_glow", extensions: ["webm", "mp4", "mov"] }),
    image_800: Object.freeze({ folder: "800", extensions: ["png"] }),
    source_image: Object.freeze({ folder: "png", extensions: ["png", "jpg", "jpeg", "webp"] }),
    preview: Object.freeze({ folder: "previews", extensions: ["webm", "mp4", "mov"] }),
    preview_mobile: Object.freeze({ folder: "previews", extensions: ["webm", "mp4", "mov"] }),
    museum_photo: Object.freeze({ folder: "", extensions: ["jpg", "jpeg", "png", "webp", "gif", "avif"] })
  });

  var SHARED_ROLES = Object.freeze({
    flag: Object.freeze({ folder: "flags", extensions: ["svg", "png", "webp"] }),
    hud: Object.freeze({ folder: "huds", extensions: ["webm", "mp4", "mov", "png", "jpg", "jpeg", "webp"] })
  });

  // Places/Times/Roads catalog photos: site/media-site/assets/{type}/{id}/{filename}
  // (Epic #47's sibling catalogs — same upload convention as museum_photo, just
  // filed under assets/ instead of exhibits/ since there's no per-exhibit role set).
  var CATALOG_ASSET_TYPES = Object.freeze({
    places: Object.freeze({ extensions: ["jpg", "jpeg", "png", "webp", "gif", "avif"] }),
    times: Object.freeze({ extensions: ["jpg", "jpeg", "png", "webp", "gif", "avif"] }),
    roads: Object.freeze({ extensions: ["jpg", "jpeg", "png", "webp", "gif", "avif"] })
  });

  function assertOrigin(value, fallback) {
    var origin = String(value || fallback || "").replace(/\/+$/, "");
    if (!/^https:\/\/[^/]+$/.test(origin)) {
      throw new TypeError("Media origin must be an HTTPS origin");
    }
    return origin;
  }

  function assertSlug(value, label) {
    var slug = String(value || "").trim();
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) {
      throw new TypeError("Invalid " + (label || "slug") + ": " + JSON.stringify(value));
    }
    return slug;
  }

  function assertMuseumSlug(value) {
    return assertSlug(value, "museum slug");
  }

  function assertAsciiFilename(value, extensions) {
    var filename = String(value || "").trim();
    if (!filename || filename === "." || filename === ".." || /[\/\\]/.test(filename)) {
      throw new TypeError("Media filename must be a basename");
    }
    if (!/^[A-Za-z0-9][A-Za-z0-9._-]*\.[A-Za-z0-9]+$/.test(filename)) {
      throw new TypeError("Media filename must be ASCII and include an extension");
    }
    var extension = filename.split(".").pop().toLowerCase();
    if (extensions && extensions.indexOf(extension) === -1) {
      throw new TypeError("Extension ." + extension + " is not allowed for this media role");
    }
    return filename;
  }

  function origins(options) {
    var opts = options || {};
    return {
      primary: assertOrigin(opts.primaryOrigin, DEFAULT_PRIMARY_ORIGIN),
      fallback: assertOrigin(opts.fallbackOrigin, DEFAULT_FALLBACK_ORIGIN)
    };
  }

  function urlPair(relative, options) {
    var base = origins(options);
    return Object.freeze({
      relative: relative,
      primary: base.primary + "/" + relative,
      fallback: base.fallback + "/" + relative
    });
  }

  function exhibitUrls(museumSlug, role, filename, options) {
    var definition = EXHIBIT_ROLES[String(role || "")];
    if (!definition) throw new TypeError("Unknown exhibit media role: " + String(role || ""));
    var slug = assertMuseumSlug(museumSlug);
    var basename = assertAsciiFilename(filename, definition.extensions);
    return urlPair(
      ["exhibits", slug, definition.folder, basename].filter(Boolean).join("/"),
      options
    );
  }

  function sharedUrls(role, filename, options) {
    var definition = SHARED_ROLES[String(role || "")];
    if (!definition) throw new TypeError("Unknown shared media role: " + String(role || ""));
    var basename = assertAsciiFilename(filename, definition.extensions);
    return urlPair(definition.folder + "/" + basename, options);
  }

  function collageUrls(museumSlug, recordId, layout, options) {
    var slug = assertMuseumSlug(museumSlug);
    var id = assertAsciiFilename(String(recordId || "") + ".webm", ["webm"]).slice(0, -5);
    var suffix = layout === "mobile" ? "_mobile.webm" : ".webm";
    if (layout && layout !== "desktop" && layout !== "mobile") {
      throw new TypeError("Collage layout must be desktop or mobile");
    }
    return urlPair("exhibits/" + slug + "/videos/" + id + suffix, options);
  }

  function catalogAssetUrls(catalogType, recordId, filename, options) {
    var definition = CATALOG_ASSET_TYPES[String(catalogType || "")];
    if (!definition) throw new TypeError("Unknown catalog asset type: " + String(catalogType || ""));
    var id = assertSlug(recordId, catalogType + " id");
    var basename = assertAsciiFilename(filename, definition.extensions);
    return urlPair(["assets", catalogType, id, basename].join("/"), options);
  }

  global.RotMediaRuntime = Object.freeze({
    DEFAULT_PRIMARY_ORIGIN: DEFAULT_PRIMARY_ORIGIN,
    DEFAULT_FALLBACK_ORIGIN: DEFAULT_FALLBACK_ORIGIN,
    EXHIBIT_ROLES: EXHIBIT_ROLES,
    SHARED_ROLES: SHARED_ROLES,
    CATALOG_ASSET_TYPES: CATALOG_ASSET_TYPES,
    assertMuseumSlug: assertMuseumSlug,
    assertAsciiFilename: assertAsciiFilename,
    exhibitUrls: exhibitUrls,
    sharedUrls: sharedUrls,
    collageUrls: collageUrls,
    catalogAssetUrls: catalogAssetUrls
  });
})(typeof window !== "undefined" ? window : globalThis);
