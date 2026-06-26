---
icon: lucide/wand-sparkles
---

# Transform Tables

Use table transformations when the authored table shape is not the shape your
schema should parse directly.

```python
from talika import RowTable, TableData, field


class UpperTable(RowTable):
    value = field("value")

    @classmethod
    def transform_table(cls, table, context):
        rows = []
        for row in table.rows:
            rows.append([cell.with_value(cell.value.upper()) for cell in row])
        return TableData.from_cells(rows)
```

`transform_table()` receives `TableData` and must return `TableData`.

## Reusable transformers

Reusable transformer objects implement:

```python
def transform(self, table, context, *, schema=None):
    ...
```

Attach them with `table_transformer`:

```python
class MyTable(RowTable):
    table_transformer = my_transformer
```

Use `TransformerPipeline` or `compose_transformers()` to run several
transformers left-to-right.

## Source preservation

When a transformed value fails later, Talika reports the original source cell if
you used `with_value()`.
