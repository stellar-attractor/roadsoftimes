# Frontend media runtime matrix

Status: FE-0 baseline for [frontend runtime epic](https://github.com/stellar-attractor/roadsoftimes/issues/1).

This document freezes the public media readers and their current behavior before
FE-1 changes the shared resolver contract. It does not describe Visual Composer
or local authoring paths.

## Public contract

Exhibit media records store ASCII filenames. A public exhibit URL is derived
only from:

1. museum slug;
2. typed media role;
3. stored filename.

The canonical relative path is:

`exhibits/<museum-slug>/<role-folder>/<filename>`

The primary and fallback origins are:

- `https://media.roadsoftimes.com`
- `https://media-roadsoftimes.pages.dev`

Collages are a separate entity type. Their rendered videos use
`exhibits/<museum-slug>/videos/<record-id>[ _mobile].webm` and must never enter
the exhibit role resolver.

## Field-to-role matrix

| Entity | Catalog field | Role | Folder | Expected type | Current readers |
|---|---|---|---|---|---|
| Exhibit | `video` | `exhibit_video` | `800_glow` | WebM/MP4/MOV basename | Player fallback source; DB mirror |
| Exhibit | `zones.exhibit_video.source` | `exhibit_video` | `800_glow` | WebM/MP4/MOV basename | Player video zone, catalog animated thumbnail |
| Exhibit | `mobile.zones.exhibit_video.source` | `exhibit_video` | `800_glow` | WebM/MP4/MOV basename | Player mobile layout |
| Exhibit | `zones.exhibit_video.source_png` | `image_800` | `800` | PNG basename | Safari player fallback, catalog still thumbnail |
| Exhibit | `mobile.zones.exhibit_video.source_png` | `image_800` | `800` | PNG basename | Safari mobile fallback |
| Exhibit | `image` / `zones.image.source` | `source_image` | `png` | PNG basename | Player image zone |
| Exhibit | `mobile.zones.image.source` | `source_image` | `png` | PNG basename | Player mobile image zone |
| Exhibit | `preview` | `preview` | `previews` | WebM/MP4/MOV basename | Catalog cards, museum strip, player preview |
| Exhibit | `mobile.preview` | `preview_mobile` | `previews` | WebM/MP4/MOV basename | Portrait catalog/strip/player preview |
| Shared | `flag`, `zones.image_flag.source`, `images[].source` with flag role | flag | `flags` | Canonical shared relative path | Player and catalog country graphics |
| Shared | `frame.source`, `frame_overlay.source`, HUD template source | HUD plate | `huds` | Canonical shared relative path | Player background/overlay |
| Collage | `video` | collage video | `videos` | Explicit collage path or derived record filename | Player |
| Collage | `mobile.video` | collage mobile video | `videos` | Explicit collage path or derived mobile filename | Player mobile |

## Consumer matrix

| Surface | Source file | Inputs | Current resolver | Fallback | FE owner |
|---|---|---|---|---|---|
| Exhibit player | `site/js/infographic-player.js` | slug + typed role + basename | `buildExhibitMediaUrls` | Bounded primary → Pages transition | FE-1, FE-2 |
| Exhibit player previews | `site/js/infographic-player.js` | record preview, otherwise inferred record id | `_previewPath` / `_choosePreview` | Uses player media loading | FE-2 |
| Exhibit player collage | `site/js/infographic-player.js` | slug + record id/layout | `_collageVideoPath` | Player media loading | FE-2 |
| Static catalog | `site/index.html` | museum-name lookup + basename | Separate `pngSrc`, `glowSrc`, `previewSrc` builders | Generic DOM `error` swap | FE-3 |
| Blogger catalog | `template/blogger-catalog.html` | museum-name lookup + basename | Copied catalog builders | Copied DOM `error` swap | FE-4 |
| Museum strip | `template/blogger-hud-strip.html` | museum slug + preview | `mediaUrl` accepts URLs/paths; `previewSrc` infers legacy paths | None for strip videos | FE-3, FE-4 |
| Museum strip test copy | `tools/museums/test-hud-strip.html` | record id inference | Flat `/previews/` path | None | FE-4 |
| Blogger exhibit embed | `template/blogger-exhibit.html` | player options | Delegates to player | Delegates to player | FE-4 |
| Blogger generic widget | `template/blogger-widget.html` | manually entered full media URLs | Static sample markup | None | Explicitly outside catalog resolver; review in FE-4 |

## Known resolver duplication and legacy behavior

The following behavior is frozen as debt, not approved as the target design:

- `site/index.html` and `template/blogger-catalog.html` duplicate CDN constants,
  museum lookup, URL concatenation, and fallback handlers.
- `template/blogger-hud-strip.html::mediaUrl` accepts full HTTP URLs and arbitrary
  relative paths.
- The museum strip infers preview filenames from record IDs when catalog fields
  are absent.
- The museum strip retains a flat `/previews/<id>...` fallback without a museum
  slug.
- `tools/museums/test-hud-strip.html` uses the old flat preview location.
- The player contains compatibility logic for explicit legacy collage paths.
- Flags and HUD plates are shared-root assets rather than museum-role assets;
  they require typed shared resolvers, not exhibit path inference.

FE-1 through FE-5 may reduce these counts. New occurrences are forbidden.

## Frozen baseline fixtures

| Case | Fixture | Expected runtime result |
|---|---|---|
| Valid ASCII exhibit | `Brummbar_800_glow.webm` | Accepted |
| Valid transliterated exhibit | `SMS_Grosser_Kurfuerst_800_glow.webm` | Accepted |
| Unicode filename | `Großer_Kurfürst_800_glow.webm` | Rejected |
| Cyrillic filename | `Танк_800_glow.webm` | Rejected |
| Whitespace filename | `BV 206 S_800_glow.webm` | Rejected |
| Relative path | `assets/item.webm` | Rejected |
| Canonical-looking path | `exhibits/museum/800_glow/item.webm` | Rejected as resolver input |
| Full URL | `https://media.roadsoftimes.com/item.webm` | Rejected as resolver input |
| Missing file | valid basename with primary and fallback failure | One fallback, then terminal failure |
| Collage | `Category: Коллажи` | Routed only through collage resolver |

## FE-0 exit criteria

- Every production reader is represented above.
- Every media field is assigned to one typed role or explicitly marked shared.
- Exhibit and collage semantics are separate.
- `site/tests/smoke_frontend_media_inventory.js` freezes the production consumer
  list and current legacy markers.
- FE-0 makes no production behavior changes.
