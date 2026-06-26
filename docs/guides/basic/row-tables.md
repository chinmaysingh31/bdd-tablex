---
icon: lucide/rows-3
---

# Row Tables

Use `RowTable` when the first row contains labels and each later row is one
record.

```python
from talika import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)
    active = field("active", default=True)
```

```python
users = UserTable.parse([
    ["name", "role", "active"],
    ["Alice", "admin", "yes"],
    ["Bob", "editor", ""],
])
```

`users[0]` is a `UserTable` record. Declared fields become attributes:

```python
assert users[0].name == "Alice"
assert users[0].role == "admin"
```

## Missing optional fields

If an optional field is absent from the header row, Talika uses its default or
`None`.

```python
users = UserTable.parse([
    ["name", "role"],
    ["Alice", "admin"],
])

assert users[0].active is True
```

## Required fields

A required field must be present and non-empty.

```text
Required field is missing (code=missing_required, schema=UserTable, field='role')
```

For empty cells, the error includes the row and column.
