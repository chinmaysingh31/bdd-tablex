---
icon: lucide/map-pin
---

# Source Model

Talika accepts raw rows, then upgrades them to source-aware objects.

```python
from talika import TableData

table = TableData.from_rows([
    ["name"],
    ["Alice"],
])
```

Every cell has current value and original source information.

```python
cell = table.cell(2, 1)
assert cell.value == "Alice"
assert cell.source_row == 2
assert cell.source_column == 1
assert cell.source_value == "Alice"
```

## Transforming values

Use `with_value()` when a transformer changes a value.

```python
changed = cell.with_value("ALICE")
assert changed.value == "ALICE"
assert changed.source_value == "Alice"
```

That is how later errors can point to the feature text that caused the logical
value.

## Records

Parsed records expose source metadata:

```python
source_cell = record.source_for("name")
item_id = record.table_source.item_id
```
