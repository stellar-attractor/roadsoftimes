# Roads of Times Domain Model Specification

**Version:** 1.0  
**Status:** Proposed  
**Target milestone:** After the HUD Tracer repository migration  
**Primary implementation target:** Git-based JSON storage with static delivery through Cloudflare  
**Future persistence target:** Cloudflare D1 or another relational database without domain redesign

---

## 1. Purpose

This document defines the initial domain model and data architecture for the **Roads of Times** project.

The purpose of the specification is to:

- establish a stable project-wide data model;
- consolidate HUD Tracer and Roads of Times into one repository;
- replace scattered and implicit metadata with structured JSON datasets;
- keep the current implementation compatible with static hosting and CDN delivery;
- preserve a straightforward migration path from JSON files to a relational database;
- prevent frontend code, tools, and content pipelines from depending on physical storage details.

JSON is the initial persistence format. It is not part of the domain model itself.

The domain model defined here must remain valid if persistence later changes to Cloudflare D1, PostgreSQL, SQLite, or another structured storage system.

---

## 2. Scope

Version 1.0 covers the following primary entities:

- places;
- museums;
- exhibits;
- historical periods;
- routes;
- media assets;
- people;
- historical events.

Version 1.0 also defines:

- repository placement for HUD Tracer;
- JSON storage layout;
- stable identifier rules;
- cross-entity references;
- multilingual text conventions;
- validation and indexing requirements;
- generated versus authored data;
- migration boundaries;
- acceptance criteria.

The following are explicitly outside the initial implementation scope:

- database deployment;
- public editing or administration interfaces;
- authentication and authorization;
- user accounts, comments, ratings, or favorites;
- binary media storage in a database;
- full-text search infrastructure;
- automatic geographic route optimization;
- replacement of existing Blogger or media-site publication flows.

---

## 3. Architectural Principles

### 3.1 Storage independence

Application code must work with domain objects rather than with specific files or directory paths.

Frontend and tooling code must not assume that a museum, exhibit, place, or period is permanently stored in a particular JSON file.

A repository or data-access layer must isolate physical persistence from consumers.

### 3.2 Stable identifiers

Every entity must have a permanent machine-readable identifier.

Identifiers must not change when:

- a title is corrected;
- a translation changes;
- a place changes its public name;
- an exhibit is moved to another category;
- a route is renamed;
- a file is moved within the repository.

### 3.3 One authoritative owner per fact

A fact must be authored in one place only.

Examples:

- a museum stores its `place_id`;
- the place file does not duplicate the complete museum record;
- an exhibit stores its `museum_id`;
- a media asset stores its storage key and technical metadata;
- a museum record does not duplicate full media asset objects.

Derived reverse relationships must be generated into indexes instead of being manually duplicated.

### 3.4 Separation of metadata and media

JSON files store metadata and references only.

Images, WebM files, MP4 files, SVG files, audio files, and source assets must remain in file or object storage.

Binary data, Base64 content, and BLOB-like payloads are forbidden in domain JSON files.

### 3.5 Authored data versus generated data

Human-maintained source data and machine-generated indexes must be stored separately.

Generated files must never be edited manually.

### 3.6 Additive evolution

Schema evolution should be additive whenever possible.

Fields may be added without changing existing field meaning. Renaming or removing fields requires an explicit migration.

### 3.7 Small, bounded aggregate files

The project must not create one JSON file per exhibit.

A museum's exhibits must be stored as one aggregate JSON file because the expected scale is approximately 100–200 exhibits per museum.

The implementation may split an exhibit file later only when a measurable operational reason appears, such as excessive file size, merge conflicts, or domain-specific partitioning.

### 3.8 Deterministic output

All generated JSON must be deterministic:

- UTF-8 encoding;
- two-space indentation;
- stable key ordering where generated;
- stable array ordering;
- final newline;
- no timestamp changes unless the underlying data changed, except where timestamps are explicitly required.

---

## 4. Target Repository Structure

The exact existing repository structure must be preserved where possible. The target additions are:

```text
RoadsOfTimes/
├── site/
├── media-site/
├── tools/
│   └── hud_panel_tracer/
├── data/
│   ├── source/
│   │   ├── places/
│   │   ├── museums/
│   │   ├── exhibits/
│   │   ├── periods/
│   │   ├── routes/
│   │   ├── people/
│   │   ├── events/
│   │   └── media/
│   └── generated/
│       ├── indexes/
│       ├── manifests/
│       └── public/
├── schemas/
├── scripts/
│   └── data/
├── tests/
│   └── data/
└── docs/
```

### 4.1 `tools/hud_panel_tracer`

Contains the migrated HUD Tracer application and its internal application assets.

HUD Tracer must not own canonical project data. It reads and updates Roads of Times domain data through an explicit data-access layer.

### 4.2 `data/source`

Contains canonical authored JSON files committed to Git.

These files are the source of truth during the JSON-based phase.

### 4.3 `data/generated`

Contains indexes, manifests, publication projections, and other reproducible artifacts.

Generated data may be committed only when required by deployment or external tooling. Otherwise it should be generated in CI or local build steps.

### 4.4 `schemas`

Contains JSON Schema definitions for every entity and aggregate file.

### 4.5 `scripts/data`

Contains validation, migration, indexing, normalization, and export scripts.

---

## 5. Naming Conventions

### 5.1 File names

All authored JSON file names must use lowercase kebab-case.

Examples:

```text
panzermuseum-munster.json
marinemuseum-wilhelmshaven.json
lower-silesia-castles.json
world-war-ii.json
```

### 5.2 Entity type names

Entity type names must use lowercase snake_case where values contain more than one word.

Examples:

```text
historical_period
battlefield
archaeological_site
media_asset
```

### 5.3 Property names

JSON property names must use lowercase snake_case.

### 5.4 Identifier format

Canonical entity IDs must be globally unique and namespaced:

```text
place.nysa
museum.panzermuseum-munster
period.world-war-ii
route.lower-silesia-castles
person.frederick-the-great
event.battle-of-zorndorf
media.panzermuseum-munster.marder-iii.main-800
```

Exhibit IDs must also be globally unique. They must include the museum namespace to avoid collisions:

```text
exhibit.panzermuseum-munster.marder-iii-ausf-h
exhibit.marinemuseum-wilhelmshaven.grosser-kurfuerst-model
```

IDs must match:

```regex
^[a-z][a-z0-9]*(\.[a-z0-9]+(?:-[a-z0-9]+)*)+$
```

### 5.5 Slugs

A slug is a presentation and URL concern. It may initially match the final segment of an ID, but it is not the canonical key.

Every entity exposed through a website route may define a separate `slug`.

---

## 6. Common Entity Envelope

All first-class entities must contain the following common fields:

```json
{
  "id": "museum.panzermuseum-munster",
  "entity_type": "museum",
  "schema_version": 1,
  "status": "published",
  "slug": "panzermuseum-munster",
  "created_utc": "2026-07-15T00:00:00Z",
  "updated_utc": "2026-07-15T00:00:00Z"
}
```

### 6.1 Required common fields

| Field | Type | Rule |
|---|---:|---|
| `id` | string | Permanent globally unique identifier |
| `entity_type` | string | Must match the entity schema |
| `schema_version` | integer | Starts at `1` |
| `status` | string | Controlled vocabulary |
| `slug` | string | URL-safe kebab-case value |
| `created_utc` | string | ISO 8601 UTC with `Z` suffix |
| `updated_utc` | string | ISO 8601 UTC with `Z` suffix |

### 6.2 Status values

Initial allowed values:

```text
draft
review
published
archived
```

Deleted records should normally remain represented as archived records when external references may exist.

---

## 7. Multilingual Text Model

Translatable text must use language-keyed objects.

```json
{
  "name": {
    "pl": "Nysa",
    "ru": "Ныса",
    "en": "Nysa"
  }
}
```

### 7.1 Language codes

Use lowercase ISO 639-1 language codes where available:

```text
pl
ru
en
de
```

### 7.2 Required language policy

No global mandatory language is imposed by this specification.

Each publishing pipeline may define required languages. Validation must distinguish between:

- structurally valid translation objects;
- publication readiness for a target language.

### 7.3 Long-form text

Long descriptions may be stored directly as strings when they remain manageable.

Markdown is allowed for authored long-form text. The field name must make the format explicit when ambiguity exists:

```json
{
  "description_markdown": {
    "ru": "...",
    "en": "..."
  }
}
```

Raw HTML should not be canonical domain content unless required by a legacy publishing target.

---

## 8. Core Domain Entities

## 8.1 Place

A place represents a geographic or spatial location.

A place is not limited to a city.

### 8.1.1 Initial place types

```text
country
region
city
town
village
district
museum_site
castle
fortress
battlefield
archaeological_site
monument
building
lake
river
mountain
island
other
```

### 8.1.2 Place schema example

```json
{
  "id": "place.nysa",
  "entity_type": "place",
  "schema_version": 1,
  "status": "published",
  "slug": "nysa",
  "created_utc": "2026-07-15T00:00:00Z",
  "updated_utc": "2026-07-15T00:00:00Z",
  "place_type": "city",
  "name": {
    "pl": "Nysa",
    "ru": "Ныса",
    "en": "Nysa"
  },
  "country_code": "PL",
  "parent_place_id": "place.opole-voivodeship",
  "coordinates": {
    "lat": 50.4741,
    "lon": 17.3340
  },
  "period_ids": [
    "period.middle-ages",
    "period.early-modern"
  ],
  "summary": {
    "ru": "..."
  },
  "references": []
}
```

### 8.1.3 Place rules

- Coordinates are optional for broad regions but required for point locations where known.
- Latitude must be between `-90` and `90`.
- Longitude must be between `-180` and `180`.
- Geographic hierarchy is represented through `parent_place_id`.
- A museum references its place; the place must not duplicate full museum records.

---

## 8.2 Museum

A museum represents an institution, museum branch, historic collection open to the public, or museum-like site.

### 8.2.1 Museum schema example

```json
{
  "id": "museum.panzermuseum-munster",
  "entity_type": "museum",
  "schema_version": 1,
  "status": "published",
  "slug": "panzermuseum-munster",
  "created_utc": "2026-07-15T00:00:00Z",
  "updated_utc": "2026-07-15T00:00:00Z",
  "name": {
    "de": "Deutsches Panzermuseum Munster",
    "ru": "Немецкий танковый музей в Мунстере",
    "en": "German Tank Museum Munster"
  },
  "place_id": "place.munster-lower-saxony",
  "country_code": "DE",
  "coordinates": {
    "lat": 52.9850,
    "lon": 10.1020
  },
  "museum_types": [
    "military_history",
    "technology"
  ],
  "period_ids": [
    "period.world-war-i",
    "period.world-war-ii",
    "period.cold-war"
  ],
  "website": "https://example.invalid",
  "media_root": "exhibits/panzermuseum-munster",
  "summary": {
    "ru": "...",
    "en": "..."
  },
  "references": []
}
```

### 8.2.2 Museum rules

- `place_id` is required.
- `country_code` uses ISO 3166-1 alpha-2.
- `media_root` is a storage-relative path, not a local absolute path.
- Opening hours and ticket prices are time-sensitive. They must be modeled as optional operational metadata with a source and verification timestamp, not as timeless descriptive facts.
- Exhibit records must not be embedded inside the museum object.

---

## 8.3 Exhibit Aggregate

Each museum has one authored exhibit aggregate file.

Path convention:

```text
data/source/exhibits/<museum-slug>.json
```

Example:

```text
data/source/exhibits/panzermuseum-munster.json
```

### 8.3.1 Aggregate structure

```json
{
  "schema_version": 1,
  "museum_id": "museum.panzermuseum-munster",
  "updated_utc": "2026-07-15T00:00:00Z",
  "exhibits": []
}
```

### 8.3.2 Exhibit schema example

```json
{
  "id": "exhibit.panzermuseum-munster.marder-iii-ausf-h",
  "entity_type": "exhibit",
  "schema_version": 1,
  "status": "published",
  "slug": "marder-iii-ausf-h",
  "created_utc": "2026-07-15T00:00:00Z",
  "updated_utc": "2026-07-15T00:00:00Z",
  "museum_id": "museum.panzermuseum-munster",
  "inventory_number": null,
  "name": {
    "de": "Marder III Ausf. H",
    "ru": "Marder III Ausf. H",
    "en": "Marder III Ausf. H"
  },
  "object_type": "armored_vehicle",
  "period_ids": [
    "period.world-war-ii"
  ],
  "place_ids": [],
  "person_ids": [],
  "event_ids": [],
  "tags": [
    "tank-destroyer",
    "germany",
    "tracked-vehicle"
  ],
  "description_markdown": {
    "ru": "...",
    "en": "..."
  },
  "technical_data": {
    "country_of_origin": "DE",
    "year_from": 1942,
    "year_to": 1943
  },
  "media_ids": [
    "media.panzermuseum-munster.marder-iii.main-800",
    "media.panzermuseum-munster.marder-iii.hud-desktop"
  ],
  "references": []
}
```

### 8.3.3 Exhibit rules

- One museum normally has one exhibit aggregate file.
- The aggregate is expected to contain approximately 100–200 exhibits.
- Every exhibit inside an aggregate must reference the same `museum_id` as the aggregate envelope.
- Exhibit IDs must remain globally unique.
- Domain-specific technical data belongs under `technical_data` until a strong case exists for normalized cross-domain fields.
- `technical_data` must remain JSON-compatible and must not contain presentation HTML.
- Arrays of references must contain IDs, not embedded copies of related entities.

### 8.3.4 Future split threshold

A museum exhibit file may be partitioned only when at least one of the following becomes true:

- the uncompressed JSON file exceeds 10 MB;
- routine merge conflicts become a measurable problem;
- one museum exceeds approximately 1,000 exhibits;
- separate independently managed collections require different ownership;
- build or editor performance becomes unacceptable.

Partitioning must preserve a generated museum-level aggregate or index for consumers.

---

## 8.4 Historical Period

Historical periods provide a hierarchical temporal classification.

Use `period`, not `time`, as the domain term.

### 8.4.1 Period schema example

```json
{
  "id": "period.world-war-ii",
  "entity_type": "historical_period",
  "schema_version": 1,
  "status": "published",
  "slug": "world-war-ii",
  "created_utc": "2026-07-15T00:00:00Z",
  "updated_utc": "2026-07-15T00:00:00Z",
  "name": {
    "ru": "Вторая мировая война",
    "en": "World War II",
    "de": "Zweiter Weltkrieg"
  },
  "parent_period_id": "period.twentieth-century",
  "start_date": "1939-09-01",
  "end_date": "1945-09-02",
  "date_precision": "day",
  "summary": {
    "ru": "..."
  },
  "references": []
}
```

### 8.4.2 Date precision

Allowed initial values:

```text
day
month
year
decade
century
approximate
unknown
```

### 8.4.3 Period rules

- Periods may overlap.
- Parent-child hierarchy expresses classification, not strict containment.
- Exact dates must not be invented to fit broad historical concepts.
- BCE support must be designed before ancient-period data requires it. Version 1 may use nullable numeric year fields for such records if ISO dates are unsuitable.

---

## 8.5 Route

A route represents a curated Roads of Times journey, itinerary, or thematic sequence of stops.

It is not a road segment or GIS routing primitive.

### 8.5.1 Route schema example

```json
{
  "id": "route.lower-silesia-castles",
  "entity_type": "route",
  "schema_version": 1,
  "status": "draft",
  "slug": "lower-silesia-castles",
  "created_utc": "2026-07-15T00:00:00Z",
  "updated_utc": "2026-07-15T00:00:00Z",
  "name": {
    "ru": "Замки Нижней Силезии",
    "en": "Castles of Lower Silesia"
  },
  "route_type": "travel_itinerary",
  "period_ids": [
    "period.middle-ages",
    "period.early-modern"
  ],
  "stops": [
    {
      "order": 1,
      "place_id": "place.bolkow",
      "museum_id": "museum.bolkow-castle-museum",
      "event_id": null,
      "note": {
        "ru": "..."
      }
    }
  ],
  "summary": {
    "ru": "..."
  },
  "media_ids": [],
  "references": []
}
```

### 8.5.2 Route rules

- Stop order must be explicit and unique within a route.
- Each stop must reference at least one of `place_id`, `museum_id`, or `event_id`.
- Routes may be geographic, thematic, or editorial.
- Travel logistics that change frequently should be separated from timeless historical narrative where practical.

---

## 8.6 Person

A person represents a historical individual relevant to places, museums, exhibits, events, routes, or project articles.

### 8.6.1 Person schema example

```json
{
  "id": "person.frederick-the-great",
  "entity_type": "person",
  "schema_version": 1,
  "status": "published",
  "slug": "frederick-the-great",
  "created_utc": "2026-07-15T00:00:00Z",
  "updated_utc": "2026-07-15T00:00:00Z",
  "name": {
    "de": "Friedrich II.",
    "ru": "Фридрих Великий",
    "en": "Frederick the Great"
  },
  "birth_date": "1712-01-24",
  "death_date": "1786-08-17",
  "period_ids": [
    "period.age-of-enlightenment"
  ],
  "summary": {
    "ru": "..."
  },
  "media_ids": [],
  "references": []
}
```

---

## 8.7 Historical Event

An event represents a historical occurrence with temporal and geographic context.

Examples include battles, treaties, unions, sieges, discoveries, expeditions, and political acts.

### 8.7.1 Event schema example

```json
{
  "id": "event.battle-of-zorndorf",
  "entity_type": "historical_event",
  "schema_version": 1,
  "status": "published",
  "slug": "battle-of-zorndorf",
  "created_utc": "2026-07-15T00:00:00Z",
  "updated_utc": "2026-07-15T00:00:00Z",
  "event_type": "battle",
  "name": {
    "ru": "Цорндорфское сражение",
    "en": "Battle of Zorndorf",
    "de": "Schlacht bei Zorndorf"
  },
  "start_date": "1758-08-25",
  "end_date": "1758-08-25",
  "date_precision": "day",
  "place_ids": [
    "place.zorndorf-battlefield"
  ],
  "period_ids": [
    "period.seven-years-war"
  ],
  "person_ids": [
    "person.frederick-the-great"
  ],
  "summary": {
    "ru": "..."
  },
  "media_ids": [],
  "references": []
}
```

---

## 8.8 Media Asset

A media asset represents metadata about a file stored in `media-site`, Cloudflare R2, or another file/object store.

### 8.8.1 Media catalog organization

Media records should be stored as aggregate files by logical owner or collection, not as one JSON file per asset.

Recommended initial paths:

```text
data/source/media/museums/panzermuseum-munster.json
data/source/media/museums/marinemuseum-wilhelmshaven.json
data/source/media/places/nysa.json
```

### 8.8.2 Media asset schema example

```json
{
  "id": "media.panzermuseum-munster.marder-iii.main-800",
  "entity_type": "media_asset",
  "schema_version": 1,
  "status": "published",
  "slug": "marder-iii-main-800",
  "created_utc": "2026-07-15T00:00:00Z",
  "updated_utc": "2026-07-15T00:00:00Z",
  "owner_type": "exhibit",
  "owner_id": "exhibit.panzermuseum-munster.marder-iii-ausf-h",
  "kind": "image",
  "variant": "web-800",
  "storage_provider": "media-site",
  "storage_key": "exhibits/panzermuseum-munster/800/marder-iii-ausf-h.png",
  "public_url": null,
  "mime_type": "image/png",
  "width": 800,
  "height": 533,
  "duration_ms": null,
  "size_bytes": 245123,
  "checksum_sha256": null,
  "has_alpha": true,
  "title": {
    "ru": "Marder III Ausf. H"
  },
  "alt_text": {
    "ru": "...",
    "en": "..."
  }
}
```

### 8.8.3 Media rules

- `storage_key` must be relative and portable.
- Local absolute paths must never be stored in canonical data.
- `public_url` may be generated from deployment configuration and may remain `null` in source data.
- One logical source image may have multiple media asset records representing variants.
- Variants may include:

```text
source-original
cutout-master
web-800
web-mobile
preview
thumbnail
hud-desktop
hud-mobile
webm
mp4
```

- Media files must not be embedded in JSON.
- Checksums are optional initially but recommended for generated assets and migration verification.

---

## 9. References and Provenance

Factual content should support explicit provenance.

### 9.1 Reference object

```json
{
  "source_type": "museum_label",
  "title": "Museum exhibit label",
  "url": null,
  "publisher": "Deutsches Panzermuseum Munster",
  "accessed_utc": "2026-07-15T00:00:00Z",
  "note": "Photographed on site"
}
```

### 9.2 Initial source types

```text
museum_label
museum_website
book
article
archive
photograph
primary_source
official_database
other
```

References are embedded value objects because they describe the provenance of their owner. A separate first-class source entity may be introduced later if widespread reuse justifies it.

---

## 10. Relationships

The initial relationship model uses explicit foreign IDs.

```text
Place
  ├── parent Place
  ├── Museum
  ├── Route stop
  └── Event

Museum
  ├── Place
  ├── Exhibit aggregate
  ├── Period
  └── Route stop

Exhibit
  ├── Museum
  ├── Period
  ├── Place
  ├── Person
  ├── Event
  └── Media Asset

Route
  ├── ordered Place/Museum/Event stops
  └── Period

Event
  ├── Place
  ├── Person
  ├── Period
  └── Media Asset
```

### 10.1 Relationship rules

- References must point from the entity that owns the relationship semantics.
- Reverse relationships must normally be generated.
- Dangling references are validation errors.
- Circular references are allowed where semantically valid, but recursive serializers must guard against infinite expansion.
- API or frontend projections must control relationship expansion explicitly.

---

## 11. Authored File Layout

Recommended initial layout:

```text
data/source/
├── places/
│   ├── poland.json
│   ├── germany.json
│   └── lower-silesia.json
├── museums/
│   ├── panzermuseum-munster.json
│   ├── marinemuseum-wilhelmshaven.json
│   └── bolkow-castle-museum.json
├── exhibits/
│   ├── panzermuseum-munster.json
│   ├── marinemuseum-wilhelmshaven.json
│   └── bolkow-castle-museum.json
├── periods/
│   ├── broad-periods.json
│   ├── european-conflicts.json
│   └── twentieth-century.json
├── routes/
│   └── lower-silesia-castles.json
├── people/
│   └── eighteenth-century.json
├── events/
│   └── seven-years-war.json
└── media/
    ├── museums/
    ├── places/
    └── routes/
```

The project should use aggregate files based on edit ownership and expected scale. It does not require one file per entity.

Every entity inside an aggregate must still have its own stable ID and validate against its entity schema.

---

## 12. Indexes and Generated Projections

Source JSON must remain optimized for maintainability. Consumers should use generated indexes and projections when required.

### 12.1 Required generated indexes

At minimum, generate:

```text
data/generated/indexes/entities-by-id.json
data/generated/indexes/museums-by-place.json
data/generated/indexes/exhibits-by-museum.json
data/generated/indexes/entities-by-period.json
data/generated/indexes/media-by-owner.json
data/generated/indexes/routes-by-place.json
```

### 12.2 Entity registry example

```json
{
  "museum.panzermuseum-munster": {
    "entity_type": "museum",
    "source_file": "data/source/museums/panzermuseum-munster.json"
  },
  "exhibit.panzermuseum-munster.marder-iii-ausf-h": {
    "entity_type": "exhibit",
    "source_file": "data/source/exhibits/panzermuseum-munster.json"
  }
}
```

### 12.3 Generated public projections

The build may produce frontend-specific JSON under:

```text
data/generated/public/
```

These projections may denormalize data for fast static delivery. They are not canonical and must be fully reproducible from `data/source`.

---

## 13. JSON Schema Requirements

Separate JSON Schema documents must be provided for:

- common entity fields;
- place;
- museum;
- exhibit;
- exhibit aggregate;
- historical period;
- route;
- person;
- historical event;
- media asset;
- media aggregate;
- reference object.

### 13.1 Schema policy

- Use a modern JSON Schema draft supported by the selected validator.
- Set `additionalProperties` deliberately for every object.
- Prefer strict schemas for stable top-level structures.
- Permit controlled extensibility in `technical_data` and explicitly designated metadata objects.
- Validate ID formats with regular expressions.
- Validate date and timestamp formats.
- Validate enum values.
- Validate required references separately from structural schema validation.

---

## 14. Validation Pipeline

A single command must validate all project data.

Proposed command:

```bash
python -m scripts.data.validate
```

The validator must perform:

1. JSON syntax validation;
2. JSON Schema validation;
3. duplicate ID detection;
4. dangling reference detection;
5. entity type consistency checks;
6. aggregate ownership checks;
7. duplicate route stop order checks;
8. period hierarchy cycle detection;
9. place hierarchy cycle detection;
10. media storage key uniqueness checks;
11. local media existence checks where applicable;
12. deterministic ordering checks or normalization warnings.

Validation must return a non-zero process exit code on errors.

Warnings must not be silently converted into success in CI logs.

---

## 15. Data Access Layer

HUD Tracer, scripts, and future frontend tooling must not independently parse arbitrary project directories.

A shared data-access package must provide operations such as:

```python
get_entity(entity_id)
get_museum(museum_id)
get_exhibits_for_museum(museum_id)
get_media_for_owner(owner_id)
list_places(place_type=None)
list_periods()
validate_all()
write_exhibit_aggregate(museum_id, exhibits)
```

The implementation language may initially be Python because HUD Tracer and processing pipelines already use Python.

The interface must not expose physical filenames as domain identifiers.

Writes must be atomic:

1. serialize to a temporary file;
2. validate the complete replacement;
3. replace the target file atomically;
4. regenerate affected indexes.

---

## 16. HUD Tracer Integration

### 16.1 Repository migration

HUD Tracer must be moved into:

```text
tools/hud_panel_tracer/
```

The migration must preserve its application structure and existing names unless a change is required for repository integration.

### 16.2 Responsibilities

HUD Tracer may:

- select a museum;
- select or create an exhibit record;
- read linked source media;
- generate HUD variants;
- generate WebM or other publication assets;
- update media metadata;
- associate media assets with exhibits;
- display validation errors.

HUD Tracer must not:

- invent IDs independently from the shared ID service;
- store canonical metadata in its own private project files;
- write binary content into JSON;
- use local absolute paths as persistent storage keys;
- bypass schema validation when saving domain data;
- edit generated indexes directly.

### 16.3 Project context

HUD Tracer must receive or discover one explicit project root.

All paths must be resolved relative to that root.

The application must work when the repository is cloned to a different machine or directory.

### 16.4 Save transaction

A HUD generation save operation should follow this sequence:

1. validate selected museum and exhibit;
2. generate media files into a temporary output location;
3. verify generated files;
4. move files into the canonical media path;
5. create or update media asset records;
6. update the exhibit's `media_ids`;
7. validate the affected aggregate files;
8. atomically save JSON;
9. regenerate affected indexes;
10. report the resulting files and entity IDs.

If any step before the atomic commit fails, canonical JSON must remain unchanged.

---

## 17. Media Storage Strategy

### 17.1 Initial state

Existing media remains in the current `media-site` directory structure.

Canonical data stores storage-relative keys such as:

```text
exhibits/panzermuseum-munster/800/marder-iii-ausf-h.png
huds/panzermuseum-munster/marder-iii-ausf-h-desktop.webm
```

### 17.2 Future R2 migration

A future migration to Cloudflare R2 must change deployment configuration and media storage adapters, not domain IDs.

`storage_provider` and `storage_key` must make migration possible without changing exhibit records.

### 17.3 Original assets

Heavy original photos, editing masters, and intermediate production assets may remain outside the public media store.

Only assets required by the publication and processing pipelines need canonical media asset records.

---

## 18. Git and Collaboration Rules

- Canonical source JSON is committed to Git.
- Generated files must have an explicit commit policy.
- Data modifications should be isolated from unrelated code refactors.
- Large automated rewrites must be performed in separate commits.
- Normalization scripts must produce deterministic diffs.
- Entity IDs must be reviewed as public API decisions.
- Renaming files must not rename entity IDs.
- Merge conflicts in aggregate exhibit files must be resolved semantically and revalidated.

---

## 19. Migration from Existing Data

Migration must be incremental.

### Phase 0 — Repository relocation

- move HUD Tracer into the Roads of Times repository;
- preserve existing behavior;
- make project root resolution portable;
- do not mix domain migration with UI/UX refactoring unless unavoidable.

### Phase 1 — Data foundation

- create the directory structure;
- create JSON Schemas;
- implement the validator;
- implement ID utilities;
- implement the entity registry and generated indexes.

### Phase 2 — Initial canonical entities

Create records for:

- existing museums;
- their places;
- the initial historical periods;
- existing exhibit aggregates;
- existing publication media.

The Panzermuseum Munster dataset with 99 exhibits should be the first complete migration case.

### Phase 3 — HUD Tracer read integration

- load museums and exhibits through the shared data-access layer;
- resolve media through media asset records;
- keep writes disabled until read behavior is verified.

### Phase 4 — HUD Tracer write integration

- implement atomic exhibit and media updates;
- regenerate indexes after save;
- add validation feedback to the UI;
- remove private duplicate metadata stores.

### Phase 5 — Publication projections

- generate frontend-specific JSON from canonical data;
- preserve existing frontend contracts where required;
- avoid immediate frontend rewrites.

### Phase 6 — Optional database migration

A database migration may begin when JSON creates measurable constraints.

The initial migration maps domain entities to database tables without redesigning identifiers or relationships.

---

## 20. Future Relational Mapping

The expected future table mapping is:

```text
places
museums
exhibits
historical_periods
routes
route_stops
people
historical_events
media_assets
exhibit_periods
exhibit_places
exhibit_people
exhibit_events
museum_periods
event_people
event_places
```

Multilingual content may initially remain in JSON columns or be normalized into translation tables later.

JSON aggregate file boundaries do not define future database table boundaries.

Stable entity IDs remain valid external keys after migration.

---

## 21. Database Migration Triggers

JSON remains acceptable until actual operational constraints appear.

A database migration should be considered when several of the following become true:

- cross-project search becomes a core feature;
- complex filtering is required at runtime;
- multiple tools or users write concurrently;
- an administrative interface is required;
- Git conflicts become frequent;
- aggregate files routinely exceed 10 MB;
- user-specific state is introduced;
- partial updates must occur without rebuilding static projections;
- relationship queries become too expensive or complex in generated indexes.

The total amount of JSON across the repository is not by itself a migration trigger if files remain partitioned and static delivery remains efficient.

---

## 22. Non-Functional Requirements

### 22.1 Portability

The repository must work from any local filesystem path.

### 22.2 Performance

- Loading one museum and its 100–200 exhibits must be effectively immediate in local tooling.
- Public consumers must not download the full project catalog to render one museum page.
- Generated indexes must support targeted reads.

### 22.3 Reliability

- Writes must be atomic.
- Invalid data must not be committed by automated tools.
- Generated assets and metadata must not become partially synchronized without an explicit error state.

### 22.4 Maintainability

- Domain rules must live in shared schemas and libraries.
- UI code must not duplicate validation logic.
- Build scripts must have clear inputs and outputs.

### 22.5 Scalability target

Version 1 must comfortably support:

- hundreds of museums;
- 100–200 exhibits per museum under normal conditions;
- tens of thousands of exhibits total;
- multiple media variants per exhibit;
- thousands of places, periods, events, and people;
- static CDN publication without a database.

---

## 23. Required Implementation Deliverables

The implementation milestone is complete only when the repository contains:

1. the target `data/source` and `data/generated` structure;
2. JSON Schemas for all Version 1 entities;
3. a project-wide validation command;
4. deterministic index generation;
5. a shared Python data-access layer;
6. ID generation and validation utilities;
7. one complete museum migration;
8. the complete Panzermuseum Munster exhibit aggregate containing all 99 exhibits;
9. media asset metadata for the migrated museum;
10. HUD Tracer read integration;
11. HUD Tracer atomic write integration;
12. tests for validation, indexing, and save rollback behavior;
13. documentation describing authoring and migration workflows.

---

## 24. Acceptance Criteria

### 24.1 Data integrity

- Every entity has a unique valid ID.
- Every reference resolves.
- Every source file validates against JSON Schema.
- No binary or Base64 media exists in domain JSON.
- No canonical record contains a machine-specific absolute path.

### 24.2 Panzermuseum pilot

- One museum record exists for Panzermuseum Munster.
- One place record exists for Munster, Lower Saxony.
- One exhibit aggregate contains all 99 exhibits.
- Each exhibit has a stable globally unique ID.
- Each available publication asset is represented by a media asset record.
- The complete dataset passes validation.

### 24.3 HUD Tracer

- HUD Tracer can open the project from an arbitrary clone path.
- HUD Tracer can list museums from canonical data.
- HUD Tracer can load all exhibits for a selected museum.
- HUD Tracer can generate media and attach it to an exhibit.
- Failed generation or validation leaves canonical data unchanged.
- Successful saves regenerate affected indexes.

### 24.4 Storage independence

- No frontend or tool consumer uses a JSON filename as an entity identity.
- Data access is routed through shared interfaces.
- A future D1 adapter can be added without changing domain entity IDs or consumer-facing object shapes.

---

## 25. Explicitly Forbidden Implementations

The following approaches are prohibited:

- one JSON file per exhibit;
- images or videos stored as BLOBs, Base64, or byte arrays in JSON;
- local absolute paths in canonical records;
- IDs derived dynamically from mutable display titles at runtime;
- manually maintained reverse indexes;
- duplicated complete entity objects inside related entities;
- direct editing of generated indexes;
- HUD Tracer private metadata that duplicates canonical project data;
- database-specific concepts leaking into the domain model;
- mixed repository migration, UI redesign, domain redesign, and publication redesign in one uncontrolled change set.

---

## 26. Implementation Guidance for Claude

When implementing this specification:

1. inspect the current Roads of Times and HUD Tracer repository structures before moving files;
2. preserve existing names and behavior unless a change is required by this contract;
3. separate repository migration from domain-model implementation into reviewable commits;
4. implement schemas and validation before bulk data migration;
5. migrate Panzermuseum Munster as the reference implementation;
6. do not rewrite the existing frontend during the first milestone;
7. generate compatibility JSON where the frontend currently expects legacy structures;
8. use full, working modules rather than fragments or pseudo-code;
9. add tests for every mutation path;
10. document assumptions and any deviations from this specification.

Any required deviation must be recorded in an Architecture Decision Record before implementation.

---

## 27. Final Architectural Decision

For the initial implementation phase:

- canonical structured data is stored as validated JSON in Git;
- exhibits are aggregated by museum;
- places represent all geographic and site-like entities, not only cities;
- historical time classification is represented by hierarchical periods;
- people and historical events are first-class entities from the beginning;
- media remains in file or object storage and is referenced through media asset metadata;
- HUD Tracer becomes a repository-integrated production tool, not an independent data owner;
- generated indexes and public projections support efficient static delivery;
- a future database migration must preserve the same domain model and stable IDs.

This architecture is the baseline for implementation after the repository migration and current UI/UX reorganization reach a stable point.
