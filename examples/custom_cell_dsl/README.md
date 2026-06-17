# Custom Cell DSL Example

This example shows how a project can define cell syntax without teaching
`bdd-tablex` what that syntax means.

The feature table contains four kinds of values:

```gherkin
| Headline* | random | 3:word | A literal headline |
| Category  | random | Markets |                   |
```

- `random` is an exact token owned by the example project.
- `3:word` is matched by a project-owned regular expression.
- `A literal headline` and `Markets` match nothing and pass through unchanged.
- The empty category remains `""`; field parsers do not run for empty optional
  cells.

## Define the rules

```python
content_cells = CellDSL()


@content_cells.token("random")
def random_value(context):
    generator = context.user_data["generator"]
    return generator.random_for(context.field_name)


@content_cells.pattern(r"(?P<count>\d+):word")
def generated_words(match, context):
    generator = context.user_data["generator"]
    return generator.words(int(match["count"]))
```

The handlers are ordinary project functions. They may call Faker, fixture
helpers, API-data factories, or any other local implementation.

## Attach the DSL to selected fields

```python
class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True, parser=content_cells)
    category = field("Category", parser=content_cells)
```

Only `headline` and `category` use this DSL. The content type remains a plain
string, demonstrating that projects can apply different DSLs to different
fields.

## Supply project dependencies

```python
items = bdd_table.parse(
    datatable,
    schema=ContentTable,
    context={"generator": ExampleGenerator()},
)
```

Context is supplied per parse operation, so the schema and DSL definitions do
not depend on global state.

## Matching behavior

1. Exact tokens are checked first.
2. Patterns use full-cell matching in registration order.
3. The first matching pattern wins.
4. Unmatched values pass through unchanged.
5. A project may register one fallback handler to replace pass-through behavior.
6. Handler exceptions are wrapped as `BDDTableError` with table location details.
