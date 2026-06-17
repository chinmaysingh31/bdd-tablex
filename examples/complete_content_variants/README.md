# Complete discriminated content example

This folder is the broad showcase for record variants. It intentionally uses
project-owned content language while `bdd-tablex` supplies only schema,
dispatch, conversion, validation, and source-aware plumbing.

## Concise variant declaration

Variant field sets are ordinary `TableFields` components:

```python
class ArticleFields(TableFields):
    body = field("Body*", required=True, parser=content_cells)
    related = reference("Related", many=True)


class PollFields(TableFields):
    options: list[str] = field("Options*", required=True)
    closes_after_hours: int = field("Closes after hours", default=24)
```

The base table maps discriminator values to those components:

```python
class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = discriminator(
        "Type*",
        variants={
            "Article": ArticleFields,
            "Poll": PollFields,
        },
    )
    headline = field("Headline*", required=True, parser=content_cells)
```

Internally, the package composes a schema class for each mapping entry and
registers it with the existing variant engine. There is no separate parser
lifecycle. A parsed Article is both a `ContentTable` and an `ArticleFields`
instance:

```python
assert isinstance(article, ContentTable)
assert isinstance(article, ArticleFields)
```

Use `ContentTable.variant_for("Article")` when code needs the generated
concrete schema class.

## What the first scenario demonstrates

The compact feature table combines:

- `1..2` grouped IDs and `2:Article` repeats through `ColumnGroupExpander`
- exact `random` and regex `12:word` rules through a project `CellDSL`
- shared fields on `ContentTable`
- conditional required fields from `ArticleFields` and `PollFields`
- inferred `bool`, `int`, and `list[str]` conversion
- dependencies supplied through parse context
- variant-specific `validate_record()` methods
- scenario-local `reference()` resolution
- original source metadata after group expansion
- pytest-bdd `target_fixture` injection

The package still knows nothing about Articles, Polls, generated headlines,
word counts, or the project's validation policy.

## Output models

The second scenario uses another declarative variant schema where each field
component selects its own dataclass:

```python
class ArticleCommandFields(TableFields):
    output_model = ArticleCommand
    body = field("Body*", required=True)


class PollCommandFields(TableFields):
    output_model = PollCommand
    options: list[str] = field("Options*", required=True)
```

The returned list may therefore contain different project model types. Model
construction remains the final parsing stage, after schema validation.

## Concise or explicit style

Use `discriminator(..., variants={...})` when variants are naturally reusable
field-and-policy components. Use the existing decorator style when explicit
schema class names are more important:

```python
class ContentTable(ColumnTable):
    content_type = discriminator_field("Type*")


@ContentTable.variant("Article")
class ArticleContent(ContentTable):
    body = field("Body*", required=True)
```

Both styles use the same selection, validation, reference, error, and output
model machinery.

Run the complete example:

```powershell
uv run pytest -p no:cacheprovider examples/complete_content_variants -q
```

