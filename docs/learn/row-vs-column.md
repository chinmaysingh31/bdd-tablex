---
icon: lucide/table
---

# Row vs Column Tables

Talika supports both common ways of writing BDD data tables.

## RowTable

Use `RowTable` when the first row contains labels and each later row is one
record.

```gherkin
| name  | role   |
| Alice | admin  |
| Bob   | editor |
```

```python
from talika import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)
```

This is the familiar spreadsheet shape.

## ColumnTable

Use `ColumnTable` when the first column contains labels and each later column
is one record.

```gherkin
| IDs      | 1       | 2      |
| Type     | Article | Poll   |
| Headline | News    | Vote?  |
```

```python
from talika import ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type", required=True)
    headline = field("Headline", required=True)
```

Column tables are often easier to read when each item has many fields, or when
non-developers naturally think of each item as a vertical card.

## IDs

`ColumnTable` requires exactly one `id_field`. The first row must be that ID
row, and each item column must have a unique ID.

`RowTable` may also use an `id_field` when parsers, defaults, or diagnostics
need a stable item ID.
