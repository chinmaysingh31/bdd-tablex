# Examples Map

Every major capability has an executable example under `examples/`. This file
maps each folder to the concept it teaches.

## Quick Learning Path

1. `basic_users`: first row-oriented schema.
2. `content_table`: first column-oriented schema.
3. `field_parsers`: reusable conversion.
4. `custom_cell_dsl`: project-owned cell syntax.
5. `record_validation`: one-record validation.
6. `table_validation`: whole-table validation.
7. `record_references`: local links between records.
8. `content_variants`: explicit variants.
9. `complete_content_variants`: the broad showcase.
10. `static_feature_checking` and `cli_tools`: tool and CI workflows.

## Example Folders

### `basic_users`

Teaches the smallest useful flow:

- `RowTable`
- `field()`
- a custom parser
- `bdd_table` pytest fixture
- pytest-bdd `target_fixture`

Use it to explain the basic value of replacing raw table parsing with a schema.

### `content_table`

Teaches:

- `ColumnTable`
- `id_field()`
- first-column labels
- one parsed record per item column

Use it when a domain object has many fields and row-oriented tables become
wide.

### `functional_api`

Teaches:

- `Schema.parse(...)`
- `parse_table(...)`
- `parse_table_records(...)`
- pytest fixture style

Use it to show the same lifecycle through different calling styles.

### `field_parsers`

Teaches reusable parsers:

- `decimal()`
- `boolean()`
- `map_value()`
- `split()`
- `compose()`
- `each()`
- `string()`

Use it to show how cells become useful Python values without custom code in
each step.

### `annotated_schema`

Teaches parser inference from type annotations:

- `int`
- `bool`
- `Decimal`
- `list[str]`
- optional values

Use it to show the dataclass-like feel of schema declarations.

### `custom_cell_dsl`

Teaches `CellDSL`:

- exact tokens,
- regex patterns,
- context-aware generated values,
- pass-through for unmatched values.

Use it to show how project-specific table language can stay outside the core
package.

### `composable_dsl`

Teaches:

- field-scoped tokens,
- predicate rules,
- composed DSL chains,
- first-match behavior.

Use it when different teams or domains need shared syntax plus local syntax.

### `record_validation`

Teaches `validate_record()`.

Use it for rules involving multiple fields on one parsed record, such as "Poll
headlines must end with a question mark".

### `context_validation`

Teaches parse context in validation.

Use it when table rules depend on project policy or services supplied at parse
time.

### `table_validation`

Teaches `validate_records()`.

Use it for cross-record rules like uniqueness, at-least-one constraints, or
relationships across the whole table.

### `record_sources`

Teaches:

- `record.table_source`
- `record.source_for(...)`
- row/column/source value metadata

Use it when validators or tools need precise feature-file locations.

### `table_data`

Teaches:

- `TableData`
- `TableCell`
- one-based coordinates
- `with_value()` source preservation

Use it before writing custom transformations.

### `numeric_table_transform`

Teaches declarative grouped-column expansion:

- `ColumnGroupExpander`
- `NumericRange`
- `PrefixRepeat`
- compact `1..3` and `3:Article` syntax.

Use it for compact repeated content examples.

### `alphabetic_table_transform`

Teaches the same grouped-column mechanics with different syntax:

- `AlphabeticRange`
- `SuffixRepeat`
- compact `A-C` and `Article x3`.

Use it to show that separators are not semantics by themselves. Rule objects
define meaning.

### `custom_group_rules`

Teaches custom range and repeat objects:

- project syntax like `R1~R3`,
- project syntax like `[3]Article`,
- reuse of `ColumnGroupExpander` mechanics.

Use it to show extensibility without rewriting the whole transformer.

### `transformer_pipeline`

Teaches:

- `compose_transformers()`
- ordered structural transformations
- source preservation through multiple stages.

Use it when tables need label normalization before expansion or other staged
preprocessing.

### `field_components`

Teaches reusable `TableFields`.

Use it for shared audit fields, common metadata, ownership fields, or reusable
variant components.

### `content_variants`

Teaches explicit variant classes:

- `discriminator_field()`
- `@Schema.variant(value)`
- selected variant fields,
- variant-specific validation.

Use it when named variant schema classes make code easier to read.

### `payment_variants`

Teaches row-oriented variants with per-variant output models.

Use it to show heterogeneous domain model output from one table.

### `complete_content_variants`

This is the broad showcase.

It combines:

- declarative variants with `discriminator(..., variants={...})`,
- `TableFields` components,
- `ColumnGroupExpander`,
- `CellDSL`,
- annotation conversion,
- context-aware validation,
- local references,
- source metadata,
- pytest-bdd fixtures,
- per-variant output models.

Use this as the anchor demo for the full project.

### `defaults_aliases_policies`

Teaches:

- `default=`,
- `default_factory=`,
- aliases,
- `unknown_fields`,
- `inapplicable_fields`,
- `table_extras`.

Use it for evolving table contracts safely.

### `collected_errors`

Teaches `error_mode="collect"` and `BDDTableErrors`.

Use it for authoring tools and workflows where fixing several independent
errors at once is better than fail-fast.

### `schema_introspection`

Teaches `Table.describe()`.

Use it for documentation generation, editor support, and CLI inspection.

### `output_models`

Teaches dataclass output construction through `output_model`.

Use it when tests should receive project objects rather than schema records.

### `pydantic_output`

Teaches Pydantic output models through the same `output_model` contract.

Use it when a project already uses Pydantic for validation or DTOs.

### `output_factory`

Teaches custom `build_output(record, context)`.

Use it when output construction needs a custom signature, source metadata, or
context services.

### `record_references`

Teaches `reference()`.

Use it to model parent/child or related-record relationships inside one
scenario table.

### `static_feature_checking`

Teaches programmatic checking of `.feature` tables through:

- `discover_feature_tables()`
- `check_feature()`

Use it for CI or tooling that validates feature files before scenario
execution.

### `cli_tools`

Teaches:

- `bdd-tablex check`,
- `bdd-tablex describe`,
- text diagnostics,
- JSON diagnostics,
- schema description output.

Use it for demos involving command-line workflows, CI, or editor integration.

## Unit Test Map

The `tests/` folder covers the fine details behind the examples:

- `test_row_table.py`: row parsing, defaults, required fields, empty required
  cells.
- `test_column_table.py`: column parsing, IDs, duplicate IDs, required rows.
- `test_fields.py`: declaration validation and literal label behavior.
- `test_parsers.py`: parser factories and composition.
- `test_annotations.py`: annotation inference.
- `test_custom_parsers.py`: parser context and parser failures.
- `test_cell_dsl.py`: tokens, patterns, fallback, errors.
- `test_composition.py`: scoped DSL rules and transformer pipelines.
- `test_table_data.py`: `TableData`, `TableCell`, source preservation.
- `test_table_transform.py`: custom transformation hook behavior.
- `test_group_expansion.py`: range/repeat rules and grouped columns.
- `test_record_validation.py`: per-record validation.
- `test_table_validation.py`: cross-record validation.
- `test_references.py`: local reference resolution.
- `test_variants.py`: explicit and declarative variants.
- `test_defaults_aliases_policies.py`: defaults, aliases, and policies.
- `test_error_collection.py`: collect mode.
- `test_output_models.py`: dataclass output.
- `test_pydantic_output.py`: Pydantic output.
- `test_output_factory.py`: custom output builders.
- `test_introspection.py`: schema contracts.
- `test_checker.py`: static Gherkin table discovery and CLI behavior.
- `test_pytest_plugin.py`: pytest fixture facade.
- `test_functional_api.py`: functional helpers.
- `tests/typing/public_api.py`: static typing smoke sample.

Use the examples for narrative understanding and the unit tests for exact edge
case behavior.
