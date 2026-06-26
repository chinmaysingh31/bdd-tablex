---
icon: lucide/eraser
---

# Missing, Empty, Defaults

Talika treats a missing field and an explicit empty cell differently.

## Missing field

A field is missing when its label is not present in the table.

```python
class UserTable(RowTable):
    active = field("active", default=True)
```

```python
user = UserTable.parse([["name"], ["Alice"]])[0]
assert user.active is True
```

## Default factory

Factories run only when an optional field is absent.

```python
def generated(context):
    return f"generated-{context.item_id}"


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline", default_factory=generated)
```

Factories receive `DefaultContext`, including the schema, field, item ID, and
read-only parse context data.

## Explicit empty cells

For optional fields, choose an empty-cell policy:

```python
field("value", empty="raw")    # keep ""
field("value", empty="parse")  # send "" to the parser
field("value", empty="none")   # return None
field("value", empty="error")  # reject ""
```

Required fields always reject explicit empty cells.
