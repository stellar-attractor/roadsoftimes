# Engineering Handbook
Version 1.0
---

# Part I. Purpose

## Objective

This handbook defines the engineering conventions used across the entire project ecosystem.

Unlike the Repository Architecture Specification, which describes repository responsibilities, this handbook defines how projects are developed.

Its purpose is to ensure that every engineer, AI agent and automation workflow follows the same engineering practices.

---

## Scope

This handbook applies to every repository in the ecosystem.

Products

- RoadsOfTimes
- Nebulacast Site
- Nebulacast App
- Stellar Attractor

Production Tools

- Scientific Visualization Studio
- HUD Visual Composer
- HUD Playground

Research

- Attractor Lab
- AstroLab

Automation

- Automation Agents

---

## Philosophy

The engineering process is guided by several principles.

### Simplicity

Prefer the simplest solution that satisfies current requirements.

Avoid speculative abstractions.

---

### Modularity

Every component should have one clear responsibility.

Large modules are acceptable.

Large responsibilities are not.

---

### Reproducibility

Every published result should be reproducible.

Rendering pipelines, data processing and scientific visualizations should produce identical results when executed again.

---

### Explicitness

Prefer explicit configuration over hidden conventions.

File locations, schemas, identifiers and dependencies should always be discoverable.

---

### Evolution

Repositories evolve.

Architecture evolves.

Standards evolve.

Backward compatibility is valuable but should not prevent improvements.

# Part II. Repository Standards

## Repository Responsibilities

Each repository must have exactly one primary responsibility.

The repository description should fit into one sentence.

If it requires multiple paragraphs, responsibilities are probably mixed.

---

## Repository Layout

The preferred top-level layout is

```text
assets/
content/
configs/
data/
docs/
scripts/
src/
spec/
tests/
tools/
```

Not every repository requires every directory.

Unused directories should not be created.

---

## Documentation

Every repository should contain

README.md

describing

- purpose
- architecture
- setup
- build
- deployment
- dependencies

Large repositories should additionally contain

```text
docs/
```

with architecture specifications.

---

## Specifications

Long-lived engineering decisions belong in

```text
spec/
```

rather than inside README.

Specifications describe architecture.

README explains usage.

---

## Examples

Examples belong in

```text
examples/
```

Never inside production folders.

---

## Generated Files

Generated artifacts belong only in

```text
output/
exports/
```

They should never be edited manually.

# Part III. Naming Conventions

## Repository Names

Repositories use lowercase kebab-case.

Examples

```text
roadsoftimes
stellar-attractor
scientific-visualization-studio
hud-visual-composer
automation-agents
```

---

## Directory Names

Use descriptive plural nouns where appropriate.

Preferred

```text
animations
articles
assets
configs
content
datasets
docs
figures
fonts
images
media
scripts
spec
templates
tests
widgets
```

Avoid multiple synonyms for the same concept.

---

## Files

Python

```text
snake_case.py
```

Markdown

```text
Repository_Architecture.md
Migration_Plan.md
```

JSON

```text
museum.json
article.json
schema.json
```

YAML

```text
pipeline.yml
config.yml
```

---

## Identifiers

Stable identifiers should never depend on filenames.

Examples

```text
MUS_000145

ART_000932

DOI_2026_0042

HUD_0028
```

Names may change.

Identifiers do not.

---

## Assets

Prefer descriptive names.

Good

```text
solar_coronal_loops
orbital_mechanics
tank_hud_card
```

Avoid

```text
new2
final
last_final
copy_copy
```

# Part IV. Documentation Standards

## Documentation Hierarchy

Repository

↓

README

↓

Architecture Specification

↓

Engineering Specifications

↓

Implementation Notes

---

## README

Every README should answer five questions.

1. What is this repository?

2. Why does it exist?

3. How do I build it?

4. How do I use it?

5. Where is additional documentation?

---

## Specifications

Specifications describe systems rather than code.

They should explain

- architecture
- workflows
- interfaces
- responsibilities

Specifications should remain valid despite implementation changes.

---

## Comments

Comments explain intent.

They should not describe what the code obviously does.

Bad

```python
i += 1
# increment i
```

Good

```python
# Skip invalid observations because the
# instrument occasionally reports duplicates.
```

---

## Diagrams

Prefer simple ASCII diagrams whenever possible.

Example

```text
Research

↓

Visualization

↓

Product

↓

Publishing
```

Diagrams should communicate architecture rather than implementation details.

---

## Versioning

Major architectural documents use semantic versions.

Examples

```text
1.0

1.1

2.0
```

Minor edits should not create unnecessary versions.

# Part V. Git Workflow

## Branching Strategy

The ecosystem follows a lightweight branching model.

The default branch is always

```text
main
```

Feature development should occur in short-lived branches.

Examples:

```text
feature/hud-responsive-layout

feature/cloudflare-cache

feature/roadsoftimes-cms

fix/widget-overflow

docs/repository-specification

research/new-telemetry
```

Avoid long-lived feature branches.

---

## Commits

Commits should describe intent rather than implementation.

Good:

```text
Add responsive HUD layout engine

Refactor weather aggregation pipeline

Introduce museum metadata schema

Fix orbital visualization scaling
```

Avoid:

```text
fix

update

changes

new

temp
```

---

## Atomic Commits

Each commit should represent one logical change.

Never combine:

- documentation
- refactoring
- bug fixes
- new features

into a single commit.

---

## Pull Requests

Every significant change should be reviewed before merging.

Pull Requests should explain

- purpose
- architectural impact
- migration considerations
- compatibility

---

## Tags

Stable milestones should be tagged.

Example

```text
v1.0.0

v1.2.0

v2.0.0
```

Repository tags describe repository evolution rather than product releases.

---

# Part VI. AI Agent Guidelines

## Purpose

AI agents are engineering assistants.

They should improve productivity without becoming sources of architectural inconsistency.

---

## Responsibility

Agents should

- implement specifications
- generate code
- review code
- explain architecture
- assist migration
- write documentation

Agents should never redefine architecture on their own.

---

## Source of Truth

Priority order:

1. Specifications

2. Engineering Handbook

3. Repository documentation

4. Existing implementation

If implementation conflicts with specifications,

the specification wins.

---

## Code Generation

Generated code should

- compile
- run
- follow repository conventions
- minimize dependencies
- preserve existing naming

Large rewrites require explicit approval.

---

## Refactoring

AI should prefer

small

incremental

reversible

changes.

Avoid architectural rewrites unless requested.

---

## Documentation

Whenever architecture changes,

documentation should be updated first,

implementation second.

---

## Decision Making

AI should distinguish between

Facts

Recommendations

Assumptions

Speculation

These should never be mixed.

---

# Part VII. Coding Standards

## General Philosophy

Readable code is preferred over clever code.

Future maintainability is more important than reducing the number of lines.

---

## Python

Preferred style

PEP8

with reasonable line lengths.

Use

```python
pathlib

dataclasses

typing

logging
```

instead of custom alternatives whenever appropriate.

---

## Imports

Standard library

↓

third-party libraries

↓

project modules

---

## Configuration

Avoid hardcoded paths.

Prefer

```text
configs/

settings/

environment variables
```

---

## Functions

Functions should perform one task.

Long functions should be decomposed.

Deep nesting should be avoided.

---

## Classes

Classes should represent domain concepts.

Avoid utility classes that only contain static methods.

---

## Exceptions

Errors should provide actionable information.

Prefer

```python
raise ValueError(
    f"Unknown museum id: {museum_id}"
)
```

instead of

```python
raise Exception()
```

---

## Logging

Use structured logging.

Messages should explain

- what happened
- where
- why

Avoid debug prints in production code.

---

## Dependencies

Prefer mature libraries.

Avoid introducing dependencies for trivial functionality.

---

# Part VIII. Content Standards

## Principle

Products own content.

Content should remain independent of rendering engines.

---

## Stable Structure

Every content directory should have predictable organization.

Example

```text
content/

    articles/

    figures/

    media/

    metadata/
```

---

## Metadata

Every published object should contain metadata.

Typical fields

```text
id

title

slug

created

updated

author

license

language

tags
```

Additional fields are product-specific.

---

## Identifiers

Identifiers are immutable.

Titles are editable.

Filenames may change.

Identifiers never change.

---

## Localization

Whenever practical,

language-dependent content should be separated from assets.

Example

```text
article/

    en.md

    ru.md

    images/

    metadata.json
```

---

## Media

Media should exist in publication-ready formats.

Intermediate working files belong in production tools,

not products.

---

## Generated Assets

Products should never regenerate published media during deployment.

Generation belongs to production pipelines.

Deployment only copies validated artifacts.

---

# Part IX. Release Process

## Goal

Every release should be reproducible.

The same inputs should produce the same outputs.

---

## Development Cycle

```text
Research

↓

Prototype

↓

Implementation

↓

Validation

↓

Publication

↓

Monitoring
```

---

## Validation

Before release verify

```text
□ builds successfully

□ documentation updated

□ specifications updated

□ tests pass

□ generated assets validated

□ obsolete outputs removed
```

---

## Publication

Products may publish to

- Cloudflare

- Blogger

- Static Hosting

- APIs

- Social Networks

Publishing pipelines should be fully automated whenever practical.

---

## Rollback

Every release should support rollback.

Generated assets should remain reproducible from source repositories.

---

# Part X. Architectural Decision Records

## Purpose

Not every engineering decision belongs inside a specification.

Major decisions should be documented as ADRs.

---

## ADR Structure

Each record should include

```text
Title

Status

Date

Context

Decision

Alternatives

Consequences
```

---

## Example

```text
ADR-0004

Move HUD rendering into
HUD Visual Composer

Status

Accepted
```

---

## Principles

Architectural decisions should be

- permanent
- searchable
- versioned

Old decisions are never deleted.

They may be superseded by newer ADRs.

---

## Location

Recommended directory

```text
docs/adr/
```

Naming

```text
ADR-0001.md

ADR-0002.md

ADR-0003.md
```

This creates a permanent engineering history explaining *why* the architecture evolved, not merely *how* it currently looks.

