# Column-oriented content variants

This example shows one table containing records with different shapes. All
content has an ID, type, and headline, but only an Article has a body and only
a Poll has options.

The base schema declares shared fields and marks the selector explicitly:

```python
class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = discriminator_field("Type*")
    headline = field("Headline*", required=True)
```

Normal schema subclasses define each supported variant:

```python
@ContentTable.variant("Article")
class ArticleContent(ContentTable):
    body = field("Body*", required=True)


@ContentTable.variant("Poll")
class PollContent(ContentTable):
    options: list[str] = field("Options*", required=True)
```

The table may contain the union of all variant rows. Empty cells belonging to
another variant are ignored. A non-empty value in an inapplicable row is
rejected, because it usually indicates that the scenario author put data in
the wrong place.

The parser returns the selected schema class for each item. This keeps
variant-specific fields and `validate_record()` methods local to their type:

```python
article, poll = ContentTable.parse(datatable)

assert isinstance(article, ArticleContent)
assert isinstance(poll, PollContent)
```

The discriminator parser runs before lookup. If it converts raw strings to an
enum, register enum members in `@ContentTable.variant(...)` rather than the raw
strings.

Run this example alone:

```powershell
uv run pytest -p no:cacheprovider examples/content_variants -q
```

