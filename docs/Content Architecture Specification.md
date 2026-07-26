# Content Architecture Specification
Version 1.0

---

# Part I. Purpose

## Objective

This specification defines how content is organized across the entire ecosystem.

Unlike software source code, content represents the actual knowledge, media and publications delivered to end users.

The goal is to make every product use a predictable, scalable and reusable content structure.

---

## Scope

Applies to:

- RoadsOfTimes
- Nebulacast Site
- Nebulacast App
- Stellar Attractor

Production Tools generate content but never own published content.

---

## Philosophy

Content is a first-class citizen.

Applications exist to create,

manage,

publish,

and visualize content.

Content must therefore have a stable architecture independent of implementation.

---

# Part II. Core Principles

## Principle 1

Products own content.

Production tools generate content.

Research produces knowledge.

Automation moves content.

---

## Principle 2

Every published object has exactly one owner.

Examples

Museum

↓

RoadsOfTimes

Article

↓

Nebulacast

Episode

↓

Stellar Attractor

---

## Principle 3

Content survives software.

Applications may change.

Frameworks may change.

Rendering engines may change.

Content should remain valid.

---

## Principle 4

Content must be portable.

Every content object should be movable between storage systems without modification.

---

## Principle 5

Content should be self-describing.

Metadata should explain

- identity

- ownership

- language

- publication status

without relying on directory names.

# Part III. Universal Content Model

Every product stores content inside

```text
content/
```

The internal organization differs by domain,

but follows common conventions.

---

## Content Object

Every content object consists of

```text
metadata

text

media

relations
```

---

## Metadata

Metadata describes the object.

Typical fields

```yaml
id:
title:
slug:
status:
language:
created:
updated:
author:
license:
tags:
```

---

## Text

Text is stored separately from metadata.

Preferred formats

```text
Markdown

HTML

JSON

YAML
```

---

## Media

Media remains inside the object whenever possible.

Example

```text
article/

    article.md

    metadata.json

    images/

    videos/

    figures/
```

---

## Relations

Objects should reference other objects using identifiers.

Never filenames.

Example

```yaml
period:

PER_0014

place:

PLC_0042
```
# Part IV. Stable Identifiers

## Principle

Identifiers never change.

Titles may change.

Slugs may change.

Directories may change.

Identifiers remain permanent.

---

## Repository Prefixes

Examples

```text
MUS_

Museum

EXH_

Exhibit

PER_

Historical Period

PLC_

Place

ART_

Article

FIG_

Figure

ANI_

Animation

HUD_

HUD Component

EP_

Episode

SCN_

Scene

CHR_

Character
```

---

## Example

```text
EXH_000241
```

Metadata

```yaml
id: EXH_000241

title: Panther Ausf. G

slug: panther-ausf-g
```

Only the title changes over time.

# Part V. Content Relationships

Objects should reference one another.

The filesystem should not encode relationships.

---

Example

```text
Museum

↓

contains

↓

Exhibits
```

Example

```text
Historical Period

↓

contains

↓

Places

↓

Museums

↓

Exhibits
```

Example

```text
Article

↓

uses

↓

Figures

↓

Animations

↓

HUD Widgets
```

Relationships are stored in metadata.

Not inferred from directory hierarchy.

---

## Why

Directories describe storage.

Metadata describes meaning.

These are different concerns.

# Part VI. Product-Specific Structures

## RoadsOfTimes

```text
content/

    museums/

    exhibits/

    periods/

    places/

    routes/

    articles/

    media/
```

---

## Nebulacast

```text
content/

    articles/

    papers/

    figures/

    animations/

    observations/

    datasets/

    media/
```

---

## Stellar Attractor

```text
content/

    episodes/

    scenes/

    lore/

    characters/

    locations/

    technology/

    media/
```

Each product extends the common model,

but never violates it.

