---
icon: lucide/link
---

# References

Use `reference()` for local links between records in the same table.

```python
from talika import ColumnTable, field, id_field, reference


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline")
    parent = reference("Parent", target="id")
    related = reference("Related", target="id", many=True)
```

```python
items = ContentTable.parse([
    ["IDs", "1", "2", "3"],
    ["Headline", "Root", "Child", "Other"],
    ["Parent", "", "1", "1"],
    ["Related", "2, 3", "", "2"],
])
```

```python
assert items[1].parent is items[0]
assert items[0].related == [items[1], items[2]]
```

## Local by design

References resolve only within the table being parsed. There is no global
registry, no scenario-to-scenario state, and no external lookup.

## Typed IDs

Reference keys are parsed with the target field parser before lookup.

```python
from talika import integer


class ContentTable(ColumnTable):
    id = id_field("IDs", parser=integer())
    parent = reference("Parent")
```

The raw cell `"1"` resolves to the record whose parsed `id` is `1`.
