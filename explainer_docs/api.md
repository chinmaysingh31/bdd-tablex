# Public API

This document summarizes the supported public surface. Names not exported from
`bdd_tablex` should be treated as implementation details.

## Schema classes

- `RowTable`: first row contains field labels; later rows are records.
- `ColumnTable`: first column contains field labels; later columns are records.
- `TableFields`: reusable groups of fields, parsers, validation, and output
  configuration.

Both table orientations expose `parse()`, `parse_records()`, `describe()`,
`validate_record()`, `validate_records()`, `transform_table()`, and
`build_output()`. Use `parse()` for the normal public result, including output
models. Use `parse_records()` when callers specifically want validated schema
instances for static typing or intermediate inspection.

Functional equivalents are also exported:

- `parse_table(Schema, datatable)`: equivalent to `Schema.parse(datatable)`.
- `parse_table_records(Schema, datatable)`: equivalent to
  `Schema.parse_records(datatable)`.

The functional helpers are API-style conveniences. They delegate to the same
schema lifecycle rather than providing a separate parser implementation.

## Field declarations

- `field()`
- `id_field()`
- `reference()`
- `discriminator_field()` with `@Schema.variant(value)`
- `discriminator(..., variants={...})`

Fields support canonical labels, aliases, required values, static defaults,
default factories, explicit parsers, annotation inference, references, and
variant selection.

## Parsing and DSL helpers

- `CellDSL`, `CellDSLChain`, `compose_cell_dsls()`
- `string()`, `integer()`, `floating()`, `decimal()`, `boolean()`
- `choice()`, `split()`, `map_value()`, `optional()`, `compose()`, `each()`

## Table transformation

- `TableData`, `TableCell`
- `TableTransformer`, `TransformerPipeline`, `compose_transformers()`
- `ColumnGroupExpander`
- `NumericRange`, `AlphabeticRange`
- `PrefixRepeat`, `SuffixRepeat`
- `RangeRule`, `RepeatRule`

## Context and source metadata

- `ParseContext`: one read-only project data mapping per parse operation.
- `CellContext`: parser identity, source, item ID, and user data.
- `DefaultContext`: field identity, item ID, and user data for omitted fields.
- `RecordSource`: immutable record and field source locations.

## Diagnostics

- `BDDTableError`: one structured table failure.
- `BDDTableErrors`: aggregate raised by collect mode.
- `BDDTableErrorCode`: stable diagnostic categories.
- `SchemaDefinitionError`: invalid or ambiguous schema declarations.

## Tooling

- `Table.describe()` returns a machine-readable `TableContract`.
- `discover_feature_tables()` reads official Gherkin AST data tables.
- `check_feature()` validates feature tables without running scenarios.
- `bdd-tablex check` provides the command-line equivalent, with text or JSON
  output.
- `bdd-tablex describe` prints a schema contract as text or JSON.

## Stability

The schema declarations, lifecycle hooks, documented context objects,
structured error attributes, and exports listed here form the intended public
surface for the `0.1` series. Private names and generated variant class names
may change; use `variant_for()` and stable display names instead.
