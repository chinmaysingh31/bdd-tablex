# bdd-tablex Zensical Documentation Strategy

## Summary
Build the docs around one story: `bdd-tablex` turns raw Gherkin/pytest-bdd data tables into typed, validated, source-aware Python records, so step definitions stay clean and feature-table mistakes point to the exact cell.

Research takeaways:
- Use a Diátaxis-style split: tutorials, how-to guides, reference, and explanation, as used by [pytest](https://docs.pytest.org/en/stable/) and [Hypothesis](https://hypothesis.readthedocs.io/en/latest/).
- Lead with a tiny working example, then upgrade it, like [FastAPI](https://fastapi.tiangolo.com/) and [Typer](https://typer.tiangolo.com/).
- Separate concepts, examples, API, and errors, like [Pydantic](https://docs.pydantic.dev/latest/).
- Include “why not / what this is not” positioning, like [attrs](https://www.attrs.org/en/stable/).
- Make the need obvious from pytest-bdd’s raw `datatable` shape: it returns list-of-lists, which `bdd-tablex` upgrades into schemas and diagnostics. See [pytest-bdd datatables](https://pytest-bdd.readthedocs.io/en/latest/).
- Use Zensical navigation tabs, section index pages, code copy, content tabs, diagrams, and optional mkdocstrings API pages. See [Zensical navigation](https://zensical.org/docs/setup/navigation/), [code blocks](https://zensical.org/docs/authoring/code-blocks/), [content tabs](https://zensical.org/docs/authoring/content-tabs/), [diagrams](https://zensical.org/docs/authoring/diagrams/), and [mkdocstrings](https://zensical.org/docs/setup/extensions/mkdocstrings/).

## Site Architecture
Top navigation should be:

1. **Start**
   - `index.md`: bdd-tablex
   - `start/why.md`: Why bdd-tablex?
   - `start/install.md`: Installation
   - `start/quickstart.md`: Quickstart
   - `start/adoption.md`: Adoption Path

2. **Learn**
   - `learn/concepts.md`: Core Concepts
   - `learn/lifecycle.md`: Parsing Lifecycle
   - `learn/table-orientations.md`: Row vs Column Tables
   - `learn/source-aware-diagnostics.md`: Source-Aware Diagnostics
   - `learn/mental-model.md`: What bdd-tablex Is Not

3. **Guides**
   - `guides/fields.md`: Define Fields
   - `guides/parsers.md`: Convert Cell Values
   - `guides/defaults-aliases-policies.md`: Defaults, Aliases, and Policies
   - `guides/validation.md`: Validate Records and Tables
   - `guides/cell-dsl.md`: Build a Cell DSL
   - `guides/variants.md`: Model Record Variants
   - `guides/references.md`: Link Records
   - `guides/transformations.md`: Transform Compact Tables
   - `guides/output-models.md`: Return Domain Objects
   - `guides/static-checking.md`: Check Feature Files in CI

4. **Examples**
   - `examples/index.md`: Examples Map
   - `examples/basic-users.md`: Basic User Table
   - `examples/content-table.md`: Column Content Table
   - `examples/generated-values.md`: Generated Cell Values
   - `examples/variants.md`: Mixed Record Shapes
   - `examples/full-content-demo.md`: Full Content Scenario
   - `examples/cli-ci.md`: CLI and CI Workflow

5. **Reference**
   - `reference/index.md`: Reference Overview
   - `reference/schema.md`: Schema Classes
   - `reference/fields.md`: Field Declarations
   - `reference/parsers.md`: Parser Factories
   - `reference/dsl.md`: CellDSL
   - `reference/transformers.md`: Transformations
   - `reference/context.md`: Context and Source Objects
   - `reference/errors.md`: Errors and Error Codes
   - `reference/cli.md`: CLI
   - `reference/api.md`: Public API

6. **Project**
   - `project/architecture.md`: Architecture
   - `project/stability.md`: Stability and Compatibility
   - `project/changelog.md`: Changelog
   - `project/contributing.md`: Contributing

## Page Flow
Homepage headings:
- `# bdd-tablex`
- `## Typed schemas for BDD data tables`
- `## The problem: raw tables become glue code`
- `## The fix: declare the table contract once`
- `## Before and after`
- `## What you get`
- `## Where it fits`
- `## Start with a 5-minute example`

Quickstart headings:
- `# Quickstart`
- `## Install`
- `## Parse your first row table`
- `## Use it in a pytest-bdd step`
- `## Add required fields and typed conversion`
- `## Read a cell-level error`
- `## Next: choose your table shape`

Core concept pages should follow: problem, minimal example, explanation, common mistake, link to deeper guide.

Guide pages should follow: when to use it, compact code example, full example, behavior notes, related reference.

Reference pages should be terse and stable: signatures, parameters, lifecycle timing, return values, raised errors, examples.

## Content Decisions
- Put the “need/use” argument in `start/why.md`, not only on the homepage.
- Make `RowTable` the first tutorial because it is the smallest useful path.
- Introduce `ColumnTable` immediately after, because many package features become clearer with item IDs and vertical content tables.
- Keep advanced features out of quickstart: variants, transformations, references, collect mode, introspection, and CLI checking belong in guides.
- Create one lifecycle Mermaid diagram showing: raw datatable -> `TableData` -> transform -> schema parse -> validation -> references -> output model.
- Use content tabs for equivalent APIs: `Schema.parse`, `parse_table`, and `bdd_table` fixture.
- Use code annotations for non-obvious examples, especially parser context, defaults, transformations, and source preservation.
- Keep API docs generated or semi-generated from the public `bdd_tablex.__all__` surface; do not document private modules as public contract.

## Assumptions
- Primary audience: Python developers and QA automation engineers using Gherkin/pytest-bdd data tables.
- Tone: technical, calm, example-first, with strong “why this exists” framing.
- Zensical setup, theme config, and deployment are handled separately by you.
- Docs should optimize for adoption of `0.1.x`, so stability notes should be explicit but not apologetic.
