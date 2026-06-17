# Architecture

`bdd-tablex` is small by design. Most modules own one concept, and extension
points are ordinary Python callables or tiny protocols.

## Package Layout

### `__init__.py`

Defines the supported public surface. Names exported from `bdd_tablex` are the
intended public API. Non-exported names should be treated as implementation
details.

### `fields.py`

Owns field declarations:

- `Field`
- `ReferenceSpec`
- `field()`
- `id_field()`
- `reference()`
- `discriminator_field()`
- `discriminator()`

It validates declaration options early, such as duplicate aliases, empty
labels, conflicting defaults, and invalid reference separators.

### `schema.py`

This is the core parser lifecycle.

Main responsibilities:

- collect field declarations through `SchemaMeta`,
- infer parsers from annotations,
- compose declarative variant components,
- validate schema and table labels,
- parse row-oriented tables,
- parse column-oriented tables,
- select variants,
- apply defaults and parsers,
- build source-aware records,
- resolve local references,
- run validators,
- construct output models.

Important classes:

- `TableFields`
- `BaseTable`
- `RowTable`
- `ColumnTable`

The module is intentionally the center of orchestration. Most other modules
provide focused data structures or helper protocols.

### `records.py`

Owns `TableRecord`, the lightweight schema-record type produced before output
model conversion.

Records are created without calling a user initializer. Attributes are assigned
from parsed field values, and immutable source metadata is attached.

### `context.py`

Owns context objects:

- `ParseContext`
- `CellContext`
- `DefaultContext`

The parse context copies user data into a read-only mapping so every stage sees
the same stable project dependencies.

### `table.py`

Owns source-aware table data:

- `TableCell`
- `TableData`

`TableData` is not a general dataframe. It exists so transformations can change
current values while preserving original feature-file locations.

### `sources.py`

Owns `RecordSource`, the immutable link from a parsed record back to original
table cells.

### `errors.py`

Owns structured diagnostics:

- `BDDTableErrorCode`
- `BDDTableError`
- `BDDTableErrors`
- `SchemaDefinitionError`

The design separates stable machine-readable error attributes from human error
messages. This supports CLI output, tests, and editor integrations.

### `parsers.py`

Owns reusable value parsers and parser composition. Parsers all follow the same
contract:

```python
parser(value, cell_context) -> parsed_value
```

Parser factories return plain callables rather than requiring inheritance.

### `annotations.py`

Maps supported Python type annotations to parser callables. It is intentionally
conservative: unsupported annotations return `None`, leaving raw values
unchanged.

### `dsl.py`

Owns `CellDSL`, `CellDSLChain`, and `compose_cell_dsls()`.

This module provides reusable dispatch mechanics for project-owned cell syntax.
It does not define domain syntax itself.

### `group_expansion.py`

Owns grouped-column expansion:

- `RangeRule`
- `RepeatRule`
- `NumericRange`
- `AlphabeticRange`
- `PrefixRepeat`
- `SuffixRepeat`
- `ColumnGroupExpander`

`ColumnGroupExpander` handles table mechanics. Rule objects handle syntax.

### `transformers.py`

Owns generic table transformation composition:

- `TableTransformer`
- `TransformerPipeline`
- `compose_transformers()`

Each transformer receives `TableData` and `ParseContext`, then returns
`TableData`.

### `introspection.py`

Owns immutable schema contracts:

- `FieldContract`
- `VariantContract`
- `TableContract`
- `describe_schema()`

These contracts power `Table.describe()` and CLI `describe`.

### `checker.py`

Owns static `.feature` file discovery and checking. It imports the official
Gherkin parser lazily so normal runtime parsing has no Gherkin dependency.

Main objects:

- `FeatureTable`
- `FeatureDiagnostic`
- `discover_feature_tables()`
- `check_feature()`

### `cli.py`

Owns the command-line interface:

- `bdd-tablex check`
- `bdd-tablex describe`

It supports text and JSON output, schema imports by `module:Schema` or
`path.py:Schema`, and optional context factories.

### `pytest_plugin.py`

Owns the `bdd_table` pytest fixture. The fixture is deliberately thin and
delegates to schema methods.

### `parsing.py`

Owns functional helpers:

- `parse_table()`
- `parse_table_records()`

These helpers exist for API style and reuse the same schema lifecycle.

## Dependency Shape

The base project declares no runtime dependencies. Optional integrations are
separated:

- `test`: pytest and pytest-bdd for examples/tests.
- `pydantic`: Pydantic for users who want Pydantic output models.
- `cli`: official Gherkin parser for static feature-file checking.

The checker imports Gherkin lazily. Output models are constructed through a
generic keyword-constructor contract, so dataclasses and Pydantic models use the
same path.

## Metaclass Design

`SchemaMeta` collects `Field` declarations from base classes and the class
namespace. It clones inherited fields so subclasses and generated variants can
own independent declarations.

During class creation it also:

- validates duplicate labels and aliases,
- validates schema policies,
- applies annotation-driven parser inference,
- registers declarative variants from `discriminator(..., variants={...})`.

This means many schema mistakes fail early, before a feature table is parsed.

## Variant Architecture

There is one variant engine.

The explicit form:

```python
@ContentTable.variant("Article")
class ArticleContent(ContentTable):
    ...
```

The declarative form:

```python
content_type = discriminator("Type", variants={"Article": ArticleFields})
```

Both end up registering concrete schema classes in `__variants__`. Declarative
variants are generated by composing the `TableFields` component with the base
table schema.

This avoids a second parser lifecycle.

## Error Architecture

The parser uses `BDDTableError` for one failure and `BDDTableErrors` for
collected failures.

Source-aware errors can be created from a `TableCell`:

```python
BDDTableError.from_cell("Invalid range", cell, schema=ContentTable)
```

That helper uses the cell's original source row, column, and source value.

Collect mode uses `_report()` internally to either raise immediately or append
recoverable diagnostics. It intentionally raises collected structural/cell
errors before running dependent lifecycle stages.

## Extension Contracts

Most extension points are intentionally small:

- field parser: `parser(value, CellContext) -> Any`
- default factory: `factory(DefaultContext) -> Any`
- table transformer: `transform(TableData, ParseContext, schema=...) -> TableData`
- range rule: `expand(TableCell, ParseContext) -> Sequence[TableCell]`
- repeat rule: `expand(TableCell, expected_count, ParseContext) -> Sequence[TableCell]`
- record validator: `validate_record(self, ParseContext) -> None`
- table validator: `validate_records(cls, records, ParseContext) -> None`
- output builder: `build_output(cls, record, ParseContext) -> Any`

This is why projects can customize behavior without subclassing a large
framework.

## Testing Strategy

The tests cover both unit-level behavior and executable examples.

Unit tests verify:

- row and column parsing,
- field declaration errors,
- parser behavior,
- annotation inference,
- source metadata,
- transformations,
- grouped expansion,
- references,
- variants,
- output models,
- collected diagnostics,
- CLI/checker behavior,
- public API typing.

Examples under `examples/` act as runnable documentation for user-facing
features. This is useful because many capabilities are best understood in the
shape of real BDD steps.
