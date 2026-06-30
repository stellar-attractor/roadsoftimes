/**
 * infographic-player.js
 * Self-contained exhibit infographic widget.
 *
 * Usage in Blogger HTML widget:
 *   <div id="rot-exhibit"></div>
 *   <script src="https://your-cdn/site/js/infographic-player.js"></script>
 *   <script>RotExhibit.init({ container: '#rot-exhibit', db: 'site/infographics.json' });</script>
 *
 * Or to start on a specific exhibit:
 *   RotExhibit.init({ container: '#rot-exhibit', db: '...', id: 'Tank_HUD0601' });
 */

(function (global) {
  "use strict";

  const CDN_BASE = "https://roadsoftimes.pages.dev"; // override via init options

  /* ─── CSS injected once ─────────────────────────────────────────────────── */
  const STYLE = `
.rot-exhibit-wrap {
  position: relative;
  width: 100%;
  background: #000;
  user-select: none;
}
.rot-exhibit-stage {
  position: relative;
  transform-origin: top left;
  overflow: hidden;
}
.rot-exhibit-stage video,
.rot-exhibit-stage .rot-zone {
  position: absolute;
}
.rot-exhibit-stage .rot-zone {
  overflow: hidden;
  box-sizing: border-box;
}
.rot-exhibit-stage .rot-zone-text {
  line-height: 1.45;
  overflow: hidden;
}
.rot-exhibit-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: #0a0a06;
  font-family: 'PT Sans', sans-serif;
}
.rot-exhibit-nav-btn {
  background: none;
  border: 1px solid #3a3520;
  color: #c9a84c;
  cursor: pointer;
  padding: 4px 14px;
  font-size: 16px;
  border-radius: 3px;
  line-height: 1;
  transition: background 0.15s;
}
.rot-exhibit-nav-btn:hover { background: #1a1a0e; }
.rot-exhibit-nav-btn:disabled { opacity: 0.25; cursor: default; }
.rot-exhibit-nav-info {
  font-size: 11px;
  color: #7a7060;
  text-align: center;
  flex: 1;
  padding: 0 10px;
}
.rot-exhibit-nav-title {
  color: #c8c0a8;
  font-size: 12px;
  font-weight: bold;
  display: block;
}
.rot-exhibit-nav-counter {
  color: #7a7060;
  font-size: 10px;
}
.rot-exhibit-loading {
  color: #7a7060;
  font-size: 13px;
  padding: 40px;
  text-align: center;
  font-family: monospace;
}
.rot-exhibit-error {
  color: #b03030;
  font-size: 12px;
  padding: 20px;
  text-align: center;
  font-family: monospace;
}
.rot-exhibit-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 99998;
  background: rgba(0,0,0,0.85);
}
.rot-exhibit-backdrop.rot-active { display: block; }
.rot-exhibit-wrap.rot-fullscreen {
  position: fixed;
  inset: 5vh 5vw;
  width: 90vw !important;
  height: 90vh;
  z-index: 99999;
  background: #000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.rot-stage-wrap { cursor: zoom-in; }
.rot-exhibit-wrap.rot-fullscreen .rot-stage-wrap { cursor: zoom-out; }
`;


  function injectStyles() {
    if (document.getElementById("rot-exhibit-css")) return;

    // Google Fonts
    if (!document.querySelector('link[href*="Orbitron"]')) {
      const lnk = document.createElement("link");
      lnk.rel  = "stylesheet";
      lnk.href = "https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Oswald:wght@400;500;600;700&family=PT+Sans:ital,wght@0,400;0,700;1,400&family=Kelly+Slab&display=swap";
      document.head.appendChild(lnk);
    }

    const el = document.createElement("style");
    el.id = "rot-exhibit-css";
    el.textContent = STYLE;
    document.head.appendChild(el);
  }

  /* ─── Safari detection (VP9 alpha not supported) ───────────────────────── */
  const IS_SAFARI = (function () {
    var ua = navigator.userAgent;
    return ua.indexOf("Safari") !== -1 && ua.indexOf("Chrome") === -1 && ua.indexOf("Chromium") === -1;
  }());

  const MOBILE_TEXT_OVERRIDES = ["subtitle", "header", "ttx_text"];

  var _museumSlugs = { "Болкув": "bolkow" };

  function _loadMuseumSlugMap(dbUrl) {
    var museumsUrl = String(dbUrl || "").replace(/[^/]+$/, "museums.json");
    if (!museumsUrl || museumsUrl === "museums.json") {
      museumsUrl = "museums.json";
    }
    return fetch(museumsUrl + "?v=" + Date.now())
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (list) {
        (list || []).forEach(function (m) {
          if (m && m.name && m.id) _museumSlugs[m.name] = m.id;
        });
      })
      .catch(function () {});
  }

  function _museumSlugForRec(rec) {
    if (!rec || typeof rec !== "object") return "";
    var mus = String(rec.Museum || "").trim();
    if (_museumSlugs[mus]) return _museumSlugs[mus];
    if (rec.Category === "Коллажи") {
      return _museumSlugs["Дороги Времён"] || "roadsoftimes";
    }
    return "";
  }

  function _defaultPreviewPath(rec, mobile) {
    if (!rec || !rec.id) return null;
    var slug = _museumSlugForRec(rec);
    if (!slug) return null;
    var suffix = mobile ? "_mobile_pr.webm" : "_pr.webm";
    return "exhibits/" + slug + "/previews/" + rec.id + suffix;
  }

  function _isCollage(rec) {
    return !!rec && String(rec.Category || "").trim() === "Коллажи";
  }

  // Collage = standalone pre-rendered video at exhibits/<museum>/videos/<id>.webm
  // (museum of the record, else the virtual museum "Дороги Времён" → roadsoftimes).
  function _collageVideoPath(rec, mobile) {
    if (!rec || !rec.id) return null;
    // Honor an explicit path only if it's already a proper exhibits/<museum>/videos/
    // entry — older records may carry a stale flat exhibits/<id>_800_glow.webm.
    var explicit = mobile ? (rec.mobile && rec.mobile.video) : rec.video;
    if (explicit && /\/videos\//.test(explicit)) return explicit;
    var slug = _museumSlugForRec(rec) || "roadsoftimes";
    var suffix = mobile ? "_mobile.webm" : ".webm";
    return "exhibits/" + slug + "/videos/" + rec.id + suffix;
  }

  function _layoutQueryOverride() {
    var q = new URLSearchParams(window.location.search).get("layout");
    if (q === "mobile" || q === "desktop") return q;
    return null;
  }

  function _isMobileViewport() {
    return window.matchMedia("(max-width: 768px), (orientation: portrait)").matches;
  }

  /** Merge desktop record with mobile layout slice when viewport (or ?layout=) requests it. */
  function pickLayout(rec) {
    if (!rec || typeof rec !== "object") return rec;
    var override = _layoutQueryOverride();
    var wantMobile = override === "mobile" ||
      (override !== "desktop" && _isMobileViewport());
    if (!wantMobile || !rec.mobile || !rec.mobile.zones) {
      return Object.assign({}, rec, { _isMobile: false });
    }

    var m = rec.mobile;
    var layoutRec = Object.assign({}, rec, {
      canvas_width: m.canvas_width != null ? m.canvas_width : rec.canvas_width,
      canvas_height: m.canvas_height != null ? m.canvas_height : rec.canvas_height,
      frame: m.frame || rec.frame,
      frame_overlay: m.frame_overlay !== undefined ? m.frame_overlay : rec.frame_overlay,
      zones: m.zones,
      _isMobile: true
    });

    MOBILE_TEXT_OVERRIDES.forEach(function (field) {
      if (m[field]) layoutRec[field] = m[field];
    });

    return layoutRec;
  }

  function resolveText(rec, layoutRec, field) {
    if (layoutRec && layoutRec._isMobile && layoutRec[field]) return layoutRec[field];
    return rec[field];
  }

  /** Site-relative preview path for catalog thumbs (layout-aware). */
  function pickPreviewPath(rec) {
    if (!rec || typeof rec !== "object") return null;
    var override = _layoutQueryOverride();
    var wantMobile = override === "mobile" ||
      (override !== "desktop" && _isMobileViewport());
    if (wantMobile && rec.mobile && (rec.mobile.preview || rec.mobile.zones)) {
      if (rec.mobile.preview) return rec.mobile.preview;
      return _defaultPreviewPath(rec, true);
    }
    if (rec.preview) return rec.preview;
    return _defaultPreviewPath(rec, false);
  }

  function previewUrl(rec, cdnBase, stripSitePrefix) {
    var path = pickPreviewPath(rec);
    if (!path) return "";
    if (/^https?:\/\//.test(path)) return path;
    var s = stripSitePrefix ? path.replace(/^site\//, "") : path;
    var base = (cdnBase || "").replace(/\/$/, "");
    return base ? base + "/" + s : "/" + s;
  }

  /* ─── Main class ─────────────────────────────────────────────────────────── */

  function ExhibitPlayer(opts) {
    this.container = typeof opts.container === "string"
      ? document.querySelector(opts.container)
      : opts.container;
    this.dbUrl  = opts.db   || "site/infographics.json";
    this.cdnBase = (opts.cdnBase || "").replace(/\/$/, "");
    this.stripSitePrefix = opts.stripSitePrefix || false;
    this.startId = opts.id  || null;
    this.single  = opts.single || false;
    this.records = [];
    this.index   = 0;

    this._wrap  = null;
    this._stage = null;
    this._prevBtn = null;
    this._nextBtn = null;
    this._infoEl  = null;
    this._layoutMq = null;

    injectStyles();
    this._buildShell();
    this._load();
  }

  ExhibitPlayer.prototype._buildShell = function () {
    const c = this.container;
    if (!c) return;
    c.innerHTML = "";

    this._wrap = document.createElement("div");
    this._wrap.className = "rot-exhibit-wrap";
    this._wrap.style.background = "#000"; // prevent Blogger theme override

    // Stage container collapses to the visual (scaled) height so the nav sits below it
    this._stageWrap = document.createElement("div");
    this._stageWrap.className = "rot-stage-wrap";
    this._stageWrap.style.cssText = "position:relative;overflow:hidden;width:100%;";
    this._stageWrap.addEventListener("click", () => this._toggleFullscreen());
    this._backdrop = document.createElement("div");
    this._backdrop.className = "rot-exhibit-backdrop";
    this._backdrop.addEventListener("click", () => this._toggleFullscreen());
    document.body.appendChild(this._backdrop);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this._wrap.classList.contains("rot-fullscreen")) {
        this._toggleFullscreen();
      }
    });

    this._stage = document.createElement("div");
    this._stage.className = "rot-exhibit-stage";
    this._stageWrap.appendChild(this._stage);


    this._wrap.appendChild(this._stageWrap);

    // Navigation bar
    const nav = document.createElement("div");
    nav.className = "rot-exhibit-nav";

    this._prevBtn = document.createElement("button");
    this._prevBtn.className = "rot-exhibit-nav-btn";
    this._prevBtn.textContent = "←";
    this._prevBtn.addEventListener("click", () => this._go(-1));

    this._infoEl = document.createElement("div");
    this._infoEl.className = "rot-exhibit-nav-info";

    this._nextBtn = document.createElement("button");
    this._nextBtn.className = "rot-exhibit-nav-btn";
    this._nextBtn.textContent = "→";
    this._nextBtn.addEventListener("click", () => this._go(1));


    nav.appendChild(this._prevBtn);
    nav.appendChild(this._infoEl);
    nav.appendChild(this._nextBtn);

    if (this.single) {
      this._prevBtn.style.display = "none";
      this._nextBtn.style.display = "none";
      this._infoEl.style.display  = "none";
    }

    this._wrap.appendChild(nav);
    c.appendChild(this._wrap);

    this._stage.innerHTML = '<div class="rot-exhibit-loading">Загрузка базы экспонатов…</div>';

    // Resize observer to rescale stage
    const ro = new ResizeObserver(() => this._rescale());
    ro.observe(this._wrap);

    var self = this;
    this._layoutMq = window.matchMedia("(max-width: 768px), (orientation: portrait)");
    if (this._layoutMq.addEventListener) {
      this._layoutMq.addEventListener("change", function () {
        if (self.records.length) self._render();
      });
    } else if (this._layoutMq.addListener) {
      this._layoutMq.addListener(function () {
        if (self.records.length) self._render();
      });
    }
  };

  ExhibitPlayer.prototype._load = function () {
    const self = this;
    _loadMuseumSlugMap(self.dbUrl).finally(function () {
      fetch(self.dbUrl + "?v=" + Date.now())
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        })
        .then(function (data) {
          self.records = Array.isArray(data) ? data : [];
          if (self.records.length === 0) throw new Error("Пустая база");

          // Find starting index
          if (self.startId) {
            const idx = self.records.findIndex(function (r) { return r.id === self.startId; });
            self.index = idx >= 0 ? idx : 0;
          }
          self._render();
        })
        .catch(function (err) {
          self._stage.innerHTML = '<div class="rot-exhibit-error">Ошибка загрузки: ' + err.message + '</div>';
        });
    });
  };

  ExhibitPlayer.prototype._go = function (delta) {
    const next = this.index + delta;
    if (next < 0 || next >= this.records.length) return;
    this.index = next;
    this._render();
  };

  ExhibitPlayer.prototype._cdnUrl = function (src) {
    if (!src) return "";
    // Already absolute
    if (/^https?:\/\//.test(src)) return src;
    // stripSitePrefix: true → production CDN where site/ folder is the root
    // stripSitePrefix: false (default) → local server serving repo root
    var s = this.stripSitePrefix ? src.replace(/^site\//, "") : src;
    return this.cdnBase ? this.cdnBase + "/" + s : "/" + s;
  };

  ExhibitPlayer.prototype._render = function () {
    const base = this.records[this.index];
    if (!base) return;
    const rec = pickLayout(base);

    const W = rec.canvas_width  || 1456;
    const H = rec.canvas_height || 1080;

    // Clear stage
    this._stage.innerHTML = "";
    this._stage.style.width  = W + "px";
    this._stage.style.height = H + "px";

    // ── Collage: a standalone pre-rendered video. Play it full-stage and skip the
    //    zone/frame compositing and the 800/800_glow source media exhibits require.
    if (_isCollage(rec)) {
      var collageSrc = _collageVideoPath(rec, !!rec._isMobile);
      if (collageSrc) {
        var cv = this._makeVideo(this._cdnUrl(collageSrc));
        cv.style.cssText = "left:0;top:0;width:100%;height:100%;object-fit:fill;";
        cv.style.zIndex = 0;
        this._stage.appendChild(cv);
      }
      this._rescale();
      this._updateNav(base, rec);
      return;
    }

    // ── Frame (HUD background video) ──────────────────────────────────────
    const frameInfo = rec.frame || (rec.zones && rec.zones.frame);
    if (frameInfo && frameInfo.source) {
      this._appendFrameLayer(frameInfo);
    }

    // ── Zones ─────────────────────────────────────────────────────────────
    const zones = rec.zones || {};
    const TEXT_ROLES = ["ttx_text", "subtitle", "title", "ttx_label", "header"];

    // exhibit video
    if (zones.exhibit_video) this._appendVideoZone(zones.exhibit_video);

    // all image zones — any zone with type/media_type 'image' (except frame)
    const _renderedImgIds = new Set();
    Object.keys(zones).forEach(role => {
      if (role === 'frame' || role === 'frame_overlay') return;
      const z = zones[role]; if (!z) return;
      if (z.type === 'image' || z.media_type === 'image') {
        this._appendImageZone(z);
        if (z.id) _renderedImgIds.add(z.id);
      }
    });

    // text zones: fixed order first, then any remaining text/ttx zones
    const _renderedTextRoles = new Set(TEXT_ROLES);
    TEXT_ROLES.forEach(role => {
      if (zones[role]) this._appendTextZone(zones[role], role);
    });
    Object.keys(zones).forEach(role => {
      if (_renderedTextRoles.has(role) || role === 'frame') return;
      const z = zones[role]; if (!z) return;
      if (z.type === 'text' || z.type === 'ttx' || z.type === 'header') {
        this._appendTextZone(z, role);
      }
    });

    // frame overlay
    if (zones.frame_overlay) {
      const v = this._makeVideo(this._cdnUrl(zones.frame_overlay.source));
      v.style.cssText = "left:0;top:0;width:100%;height:100%;object-fit:fill;";
      v.style.zIndex  = zones.frame_overlay.z_index != null ? zones.frame_overlay.z_index : 10;
      this._stage.appendChild(v);
    }

    // rec.images array — skip duplicates already rendered via zones
    const renderedIds = new Set(Object.values(zones).filter(z => z && z.id).map(z => z.id));
    if (Array.isArray(rec.images)) {
      rec.images.forEach(iz => {
        if (!renderedIds.has(iz.id)) this._appendImageZone(iz);
      });
    }

    this._rescale();
    this._updateNav(base, rec);
  };

  ExhibitPlayer.prototype._hudFrameWebmCandidate = function (src) {
    if (!src || /\.webm$/i.test(src)) return "";
    var m = String(src).match(/HUD(\d{2,4})/i);
    if (!m) return "";
    var digits = m[1];
    var stem = digits.length > 2 ? ("HUD" + digits.slice(0, 2) + "_Frame") : ("HUD" + digits + "_Frame");
    if (/mobile/i.test(src)) return "huds/" + stem + "_mobile.webm";
    return "huds/" + stem + ".webm";
  };

  ExhibitPlayer.prototype._appendFrameLayer = function (frameInfo) {
    var z = -1; // always background — content zones render on top
    var style = "left:0;top:0;width:100%;height:100%;object-fit:fill;";
    var src = frameInfo.source;
    var primary = this._cdnUrl(src);
    var webmPath = this._hudFrameWebmCandidate(src);
    var webmUrl = webmPath ? this._cdnUrl(webmPath) : "";

    if (webmUrl && webmUrl !== primary && /\.png$/i.test(src)) {
      var v = this._makeVideo(webmUrl);
      v.style.cssText = style;
      v.style.zIndex = z;
      v.addEventListener("error", function () {
        if (/\.png$/i.test(src)) {
          var img = document.createElement("img");
          img.src = primary;
          img.style.cssText = style;
          img.style.zIndex = z;
          v.replaceWith(img);
        } else {
          v.src = primary;
        }
      }, { once: true });
      this._stage.appendChild(v);
      return;
    }

    if (/\.png$/i.test(src)) {
      var img = document.createElement("img");
      img.src = primary;
      img.style.cssText = style;
      img.style.zIndex = z;
      this._stage.appendChild(img);
      return;
    }

    var video = this._makeVideo(primary);
    video.style.cssText = style;
    video.style.zIndex = z;
    this._stage.appendChild(video);
  };

  ExhibitPlayer.prototype._appendVideoZone = function (z) {
    const wrap = document.createElement("div");
    wrap.className = "rot-zone";
    this._positionEl(wrap, z);
    wrap.style.zIndex = z.z_index != null ? z.z_index : 5;
    wrap.style.background = "transparent";
    wrap.style.padding = "2.5%"; // keep exhibit within frame window (95% rule)

    const fit = z.fit === "stretch" ? "fill" : (z.fit === "contain" ? "contain" : "cover");
    if (z.source_png && IS_SAFARI) {
      // PNG only for Safari: VP9 alpha not supported there
      const img = document.createElement("img");
      img.src = this._cdnUrl(z.source_png);
      img.style.cssText = "position:absolute;top:5%;left:5%;width:90%;height:90%;object-fit:" + fit + ";";
      wrap.appendChild(img);
    } else {
      const v = this._makeVideo(this._cdnUrl(z.source));
      v.style.cssText = "width:100%;height:100%;object-fit:" + fit + ";display:block;background:transparent;";
      wrap.appendChild(v);
    }

    this._stage.appendChild(wrap);
  };

  ExhibitPlayer.prototype._appendImageZone = function (z) {
    if (!z || !z.source) return;
    const el = document.createElement("img");
    el.src = this._cdnUrl(z.source);
    el.style.position = "absolute";
    el.style.left   = z.x + "px";
    el.style.top    = z.y + "px";
    el.style.width  = z.width  + "px";
    el.style.height = z.height + "px";
    el.style.zIndex = z.z_index != null ? z.z_index : 5;
    el.style.opacity = z.opacity != null ? z.opacity : 1;
    var fit = z.fit || "stretch";
    el.style.objectFit = fit === "stretch" ? "fill" : (fit === "contain" ? "contain" : "cover");
    this._stage.appendChild(el);
  };

  ExhibitPlayer.prototype._appendTextZone = function (z, role) {
    // Outer div: zone bounds + vertical centering via flexbox (matches tracer: start_y = (h-total_h)//2)
    const el = document.createElement("div");
    el.className = "rot-zone rot-zone-text";
    this._positionEl(el, z);
    el.style.zIndex   = z.z_index != null ? z.z_index : 4;
    el.style.display  = "flex";
    el.style.flexDirection = "column";
    el.style.justifyContent = "center";
    el.style.boxSizing = "border-box";

    if (z.text_effect === "engraved") {
      el.style.textShadow = "0 1px 2px rgba(0,0,0,0.8), 0 -1px 1px rgba(255,255,255,0.12)";
    }

    // Inner div: carries font, color, alignment, padding, actual text
    var inner = document.createElement("div");
    var parsed = _parseFontStr(z.font);
    var fontSize = z.font_size || 14;
    var parsedFamily = (parsed && parsed.family) || "";
    var fontFamily = parsedFamily ||
      ((role === "title" || role === "ttx_label" || role === "header")
        ? "'Orbitron', sans-serif"
        : "'PT Sans', sans-serif");
    inner.style.color      = z.color || "#e8f8ff";
    inner.style.fontSize   = fontSize + "px";
    inner.style.fontWeight = (parsed && parsed.weight) || "400";
    inner.style.fontFamily = fontFamily;
    inner.style.lineHeight = "1.3";
    inner.style.boxSizing  = "border-box";
    inner.style.width      = "100%";

    var textAlign = z.text_align || "left";
    var hPad = Math.max(6, Math.round((z.width || 0) * 0.04));
    inner.style.textAlign = textAlign;
    if (textAlign === "left" || textAlign === "justify") inner.style.paddingLeft  = hPad + "px";
    if (textAlign === "right")                           inner.style.paddingRight = hPad + "px";

    if (textAlign === "justify" && z.type !== "ttx" && role !== "ttx_text") {
      inner.style.whiteSpace = "normal";
      var paras = (z.text || "").split(/\n[ \t]*\n/);
      inner.innerHTML = paras.map(function(p) {
        return "<p style='margin:0 0 1em 0'>" + esc(p.replace(/\n/g, " ")) + "</p>";
      }).join("");
    } else {
      inner.style.whiteSpace = "pre-wrap";
      inner.textContent = z.text || "";
    }

    el.appendChild(inner);
    this._stage.appendChild(el);
  };

  ExhibitPlayer.prototype._positionEl = function (el, z) {
    el.style.left   = z.x + "px";
    el.style.top    = z.y + "px";
    el.style.width  = z.width  + "px";
    el.style.height = z.height + "px";
  };

  ExhibitPlayer.prototype._makeVideo = function (src) {
    const v = document.createElement("video");
    v.src      = src;
    v.autoplay = true;
    v.loop     = true;
    v.muted    = true;
    v.setAttribute("playsinline", "");
    v.style.position = "absolute";
    return v;
  };

  ExhibitPlayer.prototype._rescale = function () {
    if (!this._wrap || !this._stage || !this._stageWrap) return;
    const stageW = parseFloat(this._stage.style.width)  || 1456;
    const stageH = parseFloat(this._stage.style.height) || 1080;
    var scale;
    if (this._wrap.classList.contains("rot-fullscreen")) {
      const navH = this._wrap.querySelector(".rot-exhibit-nav") ? this._wrap.querySelector(".rot-exhibit-nav").offsetHeight : 44;
      const scaleByW = (window.innerWidth  * 0.9) / stageW;
      const scaleByH = (window.innerHeight * 0.9 - navH) / stageH;
      scale = Math.min(scaleByW, scaleByH);
    } else {
      scale = this._wrap.clientWidth / stageW;
    }
    this._stage.style.transform  = "scale(" + scale + ")";
    this._stageWrap.style.height = (stageH * scale) + "px";
  };

  ExhibitPlayer.prototype._toggleFullscreen = function () {
    const isFs = this._wrap.classList.toggle("rot-fullscreen");
    this._backdrop.classList.toggle("rot-active", isFs);
    document.body.style.overflow = isFs ? "hidden" : "";
    this._rescale();
  };

  ExhibitPlayer.prototype._updateNav = function (base, layoutRec) {
    const rec = layoutRec || base;
    const n = this.records.length;
    const i = this.index;

    this._prevBtn.disabled = i === 0;
    this._nextBtn.disabled = i === n - 1;

    var title = resolveText(base, rec, "title") || base.id;
    var layoutTag = rec._isMobile ? ' <span style="opacity:0.55">· mobile</span>' : "";

    this._infoEl.innerHTML =
      '<span class="rot-exhibit-nav-title">' + esc(title) + layoutTag + '</span>' +
      '<span class="rot-exhibit-nav-counter">' + (i + 1) + ' / ' + n + '</span>';

  };

  /* ─── Helpers ───────────────────────────────────────────────────────────── */

  // Parse canvas font string "600 28px 'Orbitron', Arial, sans-serif"
  // → { weight: "600", family: "'Orbitron', Arial, sans-serif" }
  function _parseFontStr(fontStr) {
    if (!fontStr) return null;
    // "600 22px Orbitron, sans-serif"
    var m = fontStr.match(/^(\d+)\s+[\d.]+px\s+(.+)$/);
    if (m) return { weight: m[1], family: m[2] };
    // "italic 600 22px Family" or "bold 22px Family"
    var m2 = fontStr.match(/^(?:italic\s+)?([a-zA-Z]+)\s+[\d.]+px\s+(.+)$/);
    if (m2) return { weight: m2[1], family: m2[2] };
    // "16px Menlo, Consolas, monospace" — no weight
    var m3 = fontStr.match(/^[\d.]+px\s+(.+)$/);
    if (m3) return { weight: "400", family: m3[1] };
    return null;
  }

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  /* ─── Public API ─────────────────────────────────────────────────────────── */

  global.RotExhibit = {
    init: function (opts) {
      return new ExhibitPlayer(opts);
    },
    pickLayout: pickLayout,
    resolveText: resolveText,
    pickPreviewPath: pickPreviewPath,
    previewUrl: previewUrl,
    isMobileViewport: _isMobileViewport,
    layoutQueryOverride: _layoutQueryOverride
  };

}(window));
