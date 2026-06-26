---
icon: lucide/columns-3
---

# Column Tables

Use `ColumnTable` when the first column contains labels and each later column is
one item.

```python
from talika import ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type", required=True)
    headline = field("Headline", required=True)
    category = field("Category")
```

```python
items = ContentTable.parse([
    ["IDs", "1", "2"],
    ["Type", "Article", "Poll"],
    ["Headline", "Hello", "Choose one?"],
    ["Category", "Markets", ""],
])
```

The first row must be the declared `id_field`. Item IDs are available in parsed
records and diagnostics.

```python
assert [item.id for item in items] == ["1", "2"]
```

## Missing optional rows

If an optional row is absent, its value is `None` unless you declared a default.

```python
items = ContentTable.parse([
    ["IDs", "1"],
    ["Type", "Article"],
    ["Headline", "Hello"],
])

assert items[0].category is None
```

## Duplicate IDs

Every item column needs a unique ID. Duplicate IDs raise `duplicate_id` with
the source cell location.
