# Concepts and Lifecycle

This document explains the mental model behind `bdd-tablex`: the objects that
matter, the order in which parsing happens, and the nuances that prevent many
BDD table bugs.

## Core Concepts

The following objects appear throughout the project and are the best starting
point for understanding the parser lifecycle.

### Raw Table

Most callers start with a raw table shaped like `list[list[str]]`. This is the
form provided by `pytest-bdd` step functions.

```python
[
    ["name", "role"],
    ["Alice", "admin"],
]
```

Schemas accept this directly.

### TableData And TableCell

Internally, raw strings become `TableData`, an immutable table of `TableCell`
objects. Each `TableCell` stores:

- `value`: the current logical value consumed by parsing.
- `source_row`: original one-based feature table row.
- `source_column`: original one-based feature table column.
- `source_value`: original feature-file text before transformations.

This is how a compact source cell like `"3:Article"` can become several logical
`"Article"` values while later errors still point to the original cell.

### Schema

A schema is a class that inherits from either `RowTable` or `ColumnTable`.

- `RowTable`: first row is labels; later rows are records.
- `ColumnTable`: first column is labels; later columns are records.

Schemas declare fields with `field()`, `id_field()`, `reference()`,
`discriminator_field()`, or `discriminator()`.

### TableFields

`TableFields` is a reusable field component. It does not parse tables by itself.
It contributes fields, validation, references, parsers, and output configuration
when mixed into a table schema or used as a declarative variant component.

### ParseContext

Every parse operation has one `ParseContext`. It exposes read-only
`user_data`. Parsers, table transformers, default factories, validators, and
output builders all receive data from this same context.

Use context for deterministic project services and policy:

```python
UserTable.parse(datatable, context={"allowed_roles": {"admin", "editor"}})
```

### CellContext

Field parsers receive a `CellContext` with schema identity, field name, field
label, row, column, item ID, original source value, and user data.

This lets custom parsers generate values or produce errors with knowledge of
where the value came from.

### DefaultContext

Default factories receive a `DefaultContext`. It has no source cell because the
field was missing from the table. It still includes schema identity, field
identity, item ID when available, and user data.

### TableRecord

Before optional output model conversion, parsed data is represented by a schema
record. It has:

- one attribute per declared field,
- `as_dict()`,
- `table_source`,
- `source_for(field_name)`,
- immutable `table_extras` for preserved unknown or inapplicable fields.

## Parsing Lifecycle

The high-level lifecycle is:

1. Normalize the supplied table into `TableData`.
2. Validate that the table is not empty and has a header/label area.
3. Run `transform_table()` or a configured `table_transformer`.
4. Validate the transformed table again.
5. Validate schema and table labels.
6. For each row or column record, choose the applicable variant if variants are
   configured.
7. Resolve each field value: required checks, defaults, empty-cell handling,
   explicit parser, or inferred parser.
8. Build source-aware schema records.
9. Resolve local `reference()` fields after all records exist.
10. Run each record's `validate_record()`.
11. Run the base schema's `validate_records()` across the full parsed table.
12. If `parse()` is used and output conversion is configured, construct output
    models or call `build_output()`.

`parse_records()` follows the same lifecycle but stops before output model
conversion and returns schema records.

## Missing Field Versus Empty Cell

This is one of the most important design nuances.

A missing field means the row or column label is absent from the table. For an
optional field, this produces:

- the configured `default`,
- the result of `default_factory`, or
- `None`.

An explicitly empty cell means the table author provided the field but left the
cell blank. For an optional field, this usually remains `""`.

```gherkin
| name  | active |
| Alice |        |
```

Here `active` is present, so a default does not apply. This distinction avoids
silently replacing intentional empty values.

Parsers normally do not receive explicit empty cells. Parser objects can opt in
by exposing `parse_empty=True`; `optional(...)` does this so empty strings can
become `None`.

## Required Fields

`required=True` rejects:

- a missing field label,
- an explicitly empty cell, unless a parser opts into empty parsing.

The package does not infer required behavior from label text. A label like
`"Headline*"` is just a label. The schema must declare `required=True`.

## Field Labels And Aliases

Each field has one canonical label and zero or more aliases.

Aliases help tables evolve without editing every old feature file:

```python
name = field("name", aliases=("full name",))
```

A table cannot provide both `name` and `full name`, because that would create
two values for one schema field.

## Unknown And Inapplicable Fields

Schemas default to `unknown_fields = "forbid"`. Unknown labels raise structured
errors. Alternatives:

- `"ignore"` accepts and discards unknown fields.
- `"preserve"` accepts unknown fields and exposes them through
  `record.table_extras`.

Variant schemas also have `inapplicable_fields` for fields that belong to a
different variant. Empty inapplicable cells are ignored. Non-empty
inapplicable cells are forbidden, ignored, or preserved depending on policy.

## Variants

Variants let one table contain several related record shapes. The base schema
declares a discriminator. The parsed discriminator value selects the concrete
record schema.

The selected variant controls:

- required fields,
- parsers and annotation inference,
- references,
- `validate_record()`,
- `output_model` or `build_output()`.

The table may contain the union of all variant-specific labels. Required fields
are checked only for the selected variant.

## References

`reference()` fields resolve scenario-local IDs to other records in the same
table. Resolution happens after all records are structurally valid and before
record validation.

Single empty references become `None`. Many references become `[]`.

References resolve to schema records, not final output models. This is
important when `output_model` is also configured: model constructors receive
record objects for reference fields.

## Validation Timing

Field parsers and defaults run before validation. References resolve before
validation. Output conversion runs after validation.

That means validators can rely on normalized field types and resolved local
links.

## Error Modes

The default `error_mode="first"` raises the first `BDDTableError`.

`error_mode="collect"` gathers independent errors and raises `BDDTableErrors`.
It collects while continuation is trustworthy. If structural or cell-level
errors make later stages unreliable, it stops before reference resolution,
record validation, table validation, and output conversion.

This prevents one bad table from producing a flood of misleading secondary
diagnostics.

## Source-Aware Diagnostics

Every `BDDTableError` has structured attributes:

- `code`
- `schema`
- `field`
- `row`
- `column`
- `item_id`
- `value`
- `hint`

Messages may improve over time, but codes are stable and intended for tooling.
The CLI and checker expose these diagnostics in text and JSON formats.

The current diagnostic code vocabulary is:

- `table_error`
- `schema_definition`
- `invalid_context`
- `table_empty`
- `header_empty`
- `ragged_row`
- `duplicate_label`
- `unknown_field`
- `missing_required`
- `empty_required`
- `default_factory_failed`
- `parser_failed`
- `transform_failed`
- `invalid_transform`
- `unknown_variant`
- `inapplicable_field`
- `duplicate_id`
- `reference_failed`
- `record_validation_failed`
- `table_validation_failed`
- `output_failed`

## Choosing The Parse API

Use `Schema.parse(datatable)` for normal application or test code. It returns
output models when configured.

Use `Schema.parse_records(datatable)` when you need schema records, source
metadata, references, `table_extras`, or type-checker-friendly attributes.

Use `parse_table(Schema, datatable)` or `parse_table_records(Schema, datatable)`
when a functional API reads better.

Use the `bdd_table` pytest fixture when dependency injection keeps step
definitions cleaner.
