# Feature Guide

This is the detailed feature map for `bdd-tablex`. It moves from the smallest
features to the larger composition features.

For a slower walkthrough with many more examples, including a deeper
explanation of transformers and pipelines, read
[Detailed Feature Guide](detailed-feature-guide.md).

## Row-Oriented Schemas

Use `RowTable` when the first row contains labels and each later row is one
record.

```gherkin
| name  | role   |
| Alice | admin  |
| Bob   | editor |
```

```python
class UserTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)
```

Best for:

- user lists,
- permissions,
- products,
- payments,
- compact tables where every record has the same shape.

Nuance: `RowTable` can still use `id_field()` if the project wants item IDs,
but only `ColumnTable` requires exactly one `id_field()`.

## Column-Oriented Schemas

Use `ColumnTable` when the first column contains labels and each later column is
one record.

```gherkin
| IDs       | 1       | 2       |
| Type*     | Article | Poll    |
| Headline* | Hello   | QA Poll |
```

```python
class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)
```

Best for:

- records with many fields,
- content examples,
- tables where item identity is central,
- tables that benefit from grouped column expansion.

Nuance: `ColumnTable` requires exactly one `id_field()`, and the first row must
be that ID field. Duplicate item IDs are rejected.

## Fields

`field()` declares the relationship between a schema attribute and a BDD table
label.

Options include:

- `required=True`
- `default=...`
- `default_factory=...`
- `parser=...`
- `aliases=(...)`

Validation happens at schema-definition time for invalid combinations such as
`required=True` with a default, duplicate aliases, or alias collisions.

## ID Fields

`id_field()` marks the item identifier in a `ColumnTable`.

It is always required and can use a parser:

```python
id = id_field("IDs", parser=integer())
```

Parsed IDs appear as normal attributes and as `record.table_source.item_id`.

## Reusable Field Parsers

The package provides small parser factories:

- `string(strip=False, lower=False, upper=False)`
- `integer(base=10)`
- `floating()`
- `decimal()`
- `boolean(...)`
- `choice(...)`
- `split(...)`
- `map_value(...)`
- `optional(...)`
- `compose(...)`
- `each(...)`

Example:

```python
tags = field("tags", parser=compose(split(","), each(string(strip=True))))
```

Nuance: parsers receive the current logical value and a `CellContext`. After a
table transformation, `value` may be `"Article"` while `context.source_value`
may still be `"3:Article"`.

## Annotation-Driven Conversion

If a field has no explicit parser, the schema metaclass can infer parsers from
supported annotations:

- `int`
- `float`
- `bool`
- `Decimal`
- enums
- string `Literal[...]`
- `list[T]`
- simple optionals like `int | None`

Explicit parsers always win.

Unsupported annotations leave values as raw strings. This is safer than
guessing.

## Defaults And Default Factories

`default=` supplies a static value when a field is missing.

`default_factory=` receives `DefaultContext` and is better for mutable values,
generated values, or context-dependent defaults.

```python
role = field(
    "role",
    default_factory=lambda context: context.user_data["default_role"],
)
```

Nuance: factories run only when the whole field is absent. Explicit empty cells
remain explicit input.

## Aliases

Aliases support historical or alternate table wording.

```python
name = field("name", aliases=("full name", "display name"))
```

Use aliases when:

- feature files are being migrated,
- domain vocabulary changed,
- different teams use different wording.

Do not use aliases to accept two values for the same field in one table. That
is rejected.

## Parsing Policies

`unknown_fields` controls labels not declared by the base schema or variants.

```python
class UserTable(RowTable):
    unknown_fields = "preserve"
```

Options:

- `"forbid"`: default, strict.
- `"ignore"`: accept and discard.
- `"preserve"`: accept and expose through `record.table_extras`.

`inapplicable_fields` is the variant equivalent. It controls non-empty values
that belong to a different selected variant.

## CellDSL

`CellDSL` groups project-owned cell syntax rules into a reusable parser.

Dispatch order:

1. exact tokens,
2. full-match regular expressions,
3. predicates registered with `when()`,
4. optional fallback,
5. pass-through when no rule matches.

Field-scoped exact tokens take precedence over global exact tokens.

Use it for:

- `"random"` or `"auto"` tokens,
- generated fixture data,
- compact syntax like `"12:word"`,
- project-specific references or lookups,
- readable feature-table values that map to richer Python values.

Nuance: `CellDSL` owns dispatch, not semantics. The project owns what each
token or pattern means.

## Composable Cell DSLs

`compose_cell_dsls(shared, project)` creates a first-match chain.

Use this to separate reusable organization-wide syntax from feature-specific
syntax.

Example:

```python
parser = compose_cell_dsls(shared_cells, content_cells)
```

The first DSL that matches returns the value. If none match, the original value
passes through.

## Custom Table Transformations

Override `transform_table()` when a project has compact table syntax that
should be normalized before schema parsing.

The hook receives `TableData` and `ParseContext`, and must return `TableData`.

Use `cell.with_value(new_value)` when changing values so diagnostics keep the
original source location and original source text.

Use this for:

- custom compact syntaxes,
- label normalization,
- expanding shorthand rows or columns,
- project-specific preprocessing.

## ColumnGroupExpander

`ColumnGroupExpander` is a reusable transformer for grouped column tables. It
expands one source column into several logical item columns.

Example syntax with built-in rules:

- `1..3` expands to IDs `1`, `2`, `3` through `NumericRange`.
- `3:Article` repeats `"Article"` three times through `PrefixRepeat`.
- `A-C` expands to `A`, `B`, `C` through `AlphabeticRange`.
- `Article x3` repeats through `SuffixRepeat`.

The expander owns:

- rectangular table checks,
- key row checks,
- group iteration,
- count validation,
- source-preserving `TableData` construction.

Range and repeat rules own syntax recognition.

## Custom Range And Repeat Rules

Projects can supply objects that implement:

```python
range_rule.expand(cell, context) -> Sequence[TableCell]
repeat_rule.expand(cell, expected_count, context) -> Sequence[TableCell]
```

Use this when the project wants syntax like `R1~R3` or `[3]Article` while still
reusing the `ColumnGroupExpander` mechanics.

Nuance: custom rules must return `TableCell` values. Repeat rules must return
exactly the expected group size.

## Transformer Pipelines

`compose_transformers()` runs reusable table transformers left to right.

Use it when table preparation naturally has stages:

```python
table_transformer = compose_transformers(
    NormalizeLabels(),
    ColumnGroupExpander(...),
)
```

Each stage must return `TableData`. Unexpected failures are wrapped with the
stage number and transformer class name.

## Record Validation

Override `validate_record()` for rules involving several fields on one record.

It runs after:

- field parsing,
- defaults,
- reference resolution.

Use it for:

- "poll headlines must end with question mark",
- "article body must be at least 10 words",
- "role must be allowed by project policy",
- "record cannot reference itself".

Plain exceptions are wrapped as `BDDTableError` with record location. Validators
can also raise `BDDTableError.from_cell(...)` for precise field-specific source
locations.

## Whole-Table Validation

Override `validate_records()` for rules involving several records.

Use it for:

- uniqueness checks,
- at least one primary record,
- no invalid combinations across records,
- graph or relationship rules.

It receives the full list of parsed schema records and the parse context.

## Local Record References

`reference()` resolves IDs to records in the same parsed table.

```python
parent = reference("Parent")
related = reference("Related", many=True)
```

Options:

- `target="id"` selects the target schema attribute.
- `many=True` creates a list.
- `separator=","` controls list splitting.

Targets must be unique. Missing targets produce errors at the reference cell.
Self-references and cycles are allowed by the resolver and can be rejected by
validators if the domain needs that.

## Field Components

`TableFields` lets schemas share groups of declarations.

```python
class AuditFields(TableFields):
    created_by = field("created_by")
    trace_id = field("trace_id")


class ArticleTable(RowTable, AuditFields):
    headline = field("headline")
```

Use this for audit fields, ownership fields, common validation, and variant
field sets.

## Discriminated Variants

Variants let one table contain several related record shapes.

Explicit style:

```python
class PaymentTable(RowTable):
    payment_type = discriminator_field("type")


@PaymentTable.variant("card")
class CardPayment(PaymentTable):
    last_four = field("last_four", required=True)
```

Declarative style:

```python
class PaymentTable(RowTable):
    payment_type = discriminator(
        "type",
        variants={"card": CardFields, "bank": BankFields},
    )
```

Use variants for:

- content types,
- payment methods,
- user/account types,
- commands with different payloads,
- rows or columns that share a common envelope.

Nuance: discriminator parsers run before variant lookup, so register parsed
values such as enum members or normalized strings.

## Output Models

Set `output_model` to construct project objects after validation.

```python
@dataclass(frozen=True)
class User:
    name: str
    age: int


class UserTable(RowTable):
    output_model = User
```

This works for dataclasses, Pydantic models, and other keyword-constructed
classes. Pydantic is not special-cased by the parser; it uses the same keyword
construction contract.

`parse_records()` skips output conversion and returns schema records.

## Custom Output Factories

Override `build_output(record, context)` when output construction needs:

- selected fields,
- a custom constructor signature,
- source metadata,
- context services,
- variant-specific factories.

Output conversion is the final stage. Errors include record location and use
the `output_failed` code.

## Source Metadata

Every schema record exposes:

- `record.table_source.row`
- `record.table_source.column`
- `record.table_source.item_id`
- `record.source_for("field_name")`

This is useful for custom validators and tools that need to point back to the
feature table.

## Error Collection

Use `error_mode="collect"` to collect independent diagnostics:

```python
try:
    UserTable.parse(datatable, error_mode="collect")
except BDDTableErrors as errors:
    for error in errors:
        print(error.code, error.row, error.column)
```

Each individual error keeps its structured attributes and cause.

## Schema Introspection

`Table.describe()` returns a `TableContract` with:

- schema name,
- orientation,
- fields,
- aliases,
- defaults,
- parser names,
- references,
- policies,
- variants,
- transformer identity,
- output model,
- output builder.

Use this for documentation generators, editor tooling, schema discovery, and
CLI inspection.

## Functional API

`parse_table(schema, datatable)` and `parse_table_records(schema, datatable)`
delegate to schema methods. They are not a second lifecycle.

Use them when explicit parser-function style reads better in a codebase.

## Pytest Fixture

Installing the package registers a `bdd_table` fixture.

```python
def users_exist(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=UserTable)
```

The fixture is a small facade. It delegates to the schema class and does not
own a separate parser registry.

## Static Feature Checking

The optional CLI/checker parses `.feature` files with the official Gherkin
parser and validates matching data tables without executing pytest scenarios.

Programmatic:

```python
diagnostics = check_feature(
    "users.feature",
    schema=UserTable,
    step="the following users:",
)
```

CLI:

```powershell
bdd-tablex check users.feature `
  --schema tests/support/schemas.py:UserTable `
  --step "the following users:" `
  --format json
```

Use this for CI, pre-commit checks, editor integrations, and faster feedback to
feature authors.

Nuance: static checking validates the data tables found in the feature file; it
does not expand scenario-outline substitutions.

## CLI Describe

`bdd-tablex describe module:Schema` prints the schema contract. JSON output is
available for tools.

This is useful when someone wants to know what a table should look like without
reading Python source.
