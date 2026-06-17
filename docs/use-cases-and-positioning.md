# Use Cases and Positioning

This document helps you explain or sell the project to another person.

## Short Pitch

`bdd-tablex` makes BDD data tables trustworthy. It turns raw Gherkin tables
into typed, validated Python records with precise cell-level diagnostics, so
feature files stay readable and step definitions stop carrying repetitive table
parsing code.

## Longer Pitch

BDD tables are a powerful way to describe examples, but in Python they usually
arrive as raw strings. Every test suite then invents its own mini parser inside
step definitions. That creates duplication, weak validation, inconsistent
conversions, and vague failure messages.

`bdd-tablex` gives those tables explicit schemas. A schema says which labels
are allowed, which values are required, how cells should be converted, what
relationships are valid, and how to report errors back to the feature file.
The result is better collaboration between feature authors, QA, developers,
and automation tooling.

## Who Benefits

### QA Automation Engineers

They get reusable parsing and clearer failures. Instead of debugging step
definition glue, they see exactly which row, column, field, item ID, and value
failed.

### Developers

They get typed Python objects and a cleaner separation between test setup and
business actions. Parsing rules become reusable code instead of repeated
string manipulation.

### Feature Authors

They keep readable tables and can use project-specific shorthand safely, such
as generated values or compact grouped columns.

### Tech Leads

They get a standard table contract across a suite, less parsing drift between
teams, and a path to static checks in CI.

### Tool Builders

They get schema introspection and JSON diagnostics that can power editor
extensions, documentation, linting, or pre-commit validation.

## High-Value Use Cases

### Typed BDD Test Data

Use schemas to convert raw table strings into typed records:

- booleans,
- integers,
- decimals,
- enums,
- lists,
- optional values.

This reduces ad hoc parsing in every step.

### Required Table Contracts

Use `required=True`, aliases, and unknown-field policies to make feature tables
explicit. Authors get immediate feedback when required labels are absent or
misspelled.

### Content Or Configuration Matrices

Column-oriented tables are ideal when one item has many fields. They keep
feature files readable while still producing one typed record per item.

### Mixed Record Shapes

Use variants when one table contains multiple related shapes:

- Articles and Polls,
- card and bank payments,
- create and update commands,
- user types,
- product variants.

The selected variant controls required fields, validation, references, and
output models.

### Compact Table Authoring

Use `ColumnGroupExpander` or custom `transform_table()` hooks when feature
authors want compact syntax:

```gherkin
| IDs       | 1..3      |
| Type*     | 3:Article |
| Headline* | Shared    |
```

This can expand to three logical records without losing source coordinates.

### Generated Or Symbolic Cell Values

Use `CellDSL` for project-owned tokens and patterns:

- `"random"` for deterministic generated data,
- `"12:word"` for generated text,
- `"today"` or `"tomorrow"` in date-heavy tests,
- `"existing:user"` for fixtures,
- domain aliases that map to richer objects.

The parser dispatch is reusable, but semantics stay in the project.

### Context-Aware Validation

Use parse context for project policy and deterministic services:

- allowed roles,
- minimum word counts,
- fake data generators,
- environment-specific rules,
- fixtures or repositories.

This keeps schemas reusable while still project-aware.

### Local Relationship Modeling

Use `reference()` when records in the same scenario point to each other:

- parent/child content,
- related items,
- manager/user relationships,
- workflow dependencies,
- graph-like scenario setup.

References resolve before validation, so validators can reason about linked
records instead of raw ID strings.

### Domain Model Output

Use `output_model` or `build_output()` when tests should receive real project
objects instead of schema records.

This is useful when table parsing is setup, but the rest of the test expects
dataclasses, Pydantic models, commands, or DTOs.

### Static Feature Checking

Use `bdd-tablex check` in CI or pre-commit to validate feature tables before
running scenarios. This catches many authoring errors earlier and produces JSON
for tooling.

### Schema Documentation

Use `Table.describe()` or `bdd-tablex describe` to generate schema contracts.
This is useful for onboarding, review, or editor hints.

## Before And After Story

Before `bdd-tablex`:

- every step parses headers itself,
- missing fields are discovered late,
- parser errors point to Python code,
- compact syntax is hand-rolled,
- changes to table vocabulary are risky,
- feature-file linting is hard.

After `bdd-tablex`:

- schemas are reusable contracts,
- conversions are centralized,
- validators run at the right lifecycle point,
- diagnostics point to table cells,
- compact syntax preserves source metadata,
- CLI checking can run without executing scenarios.

## Demo Flow

1. Start with a simple `RowTable` for users.
2. Add `required=True` and annotation-driven conversion.
3. Show an invalid table and the row/column diagnostic.
4. Move to a `ColumnTable` for content.
5. Add a `CellDSL` token like `"random"`.
6. Add `ColumnGroupExpander` to turn `1..2` and `2:Article` into records.
7. Add variants for Article and Poll.
8. Add `reference()` and validation.
9. Show `parse_records()` source metadata.
10. Run `bdd-tablex check --format json`.

This demonstrates the project growing from a small convenience into a complete
table-contract layer.

## Objections And Answers

### "Can We Just Parse Tables By Hand?"

Yes, for one small table. The value appears when there are many steps, repeated
rules, authoring mistakes, variants, reusable syntax, or a need for better
diagnostics. `bdd-tablex` pays off by standardizing that work.

### "Does This Force A DSL On Us?"

No. The package does not define a universal table grammar. It gives you
schema, parser, transformation, and diagnostic mechanics. Your project decides
what cell syntax means.

### "Is This Tied To pytest-bdd?"

No. Direct parsing accepts raw rows or `TableData`. The pytest fixture is a
small convenience layer. Static checking uses Gherkin only when the optional
CLI extra is installed.

### "Will It Hide Business Logic In Tests?"

The design encourages the opposite. Schemas handle input contracts and
validation. Business actions remain outside the parser.

### "What If Our Tables Are Weird?"

Use `transform_table()` for full control, or implement custom range/repeat
rules for grouped columns. The source-aware data model exists for exactly this
kind of extension.

## Adoption Strategy

Start small:

1. Convert one noisy step definition to a `RowTable`.
2. Add parsers and required fields.
3. Move repeated conversion into reusable parser factories or `CellDSL`.
4. Add validation hooks for domain rules currently buried in step code.
5. Add aliases and policies during vocabulary migration.
6. Add static checking in CI once schemas stabilize.

This lets a team adopt the package without rewriting every feature file at
once.

## Best Selling Points

- Clearer failures for feature authors.
- Less repeated glue code.
- Typed records from readable tables.
- Compact authoring without losing diagnostics.
- Project-owned syntax, not forced syntax.
- Same schemas usable in tests, CLI checks, and docs.
- Works from simple row tables to complex mixed-record examples.

## What Not To Oversell

Do not present it as:

- a replacement for pytest-bdd,
- a full test data factory framework,
- a business workflow engine,
- a general spreadsheet processor,
- a universal Gherkin linter.

Its strength is narrower and more useful: reliable, reusable, source-aware BDD
table parsing.
