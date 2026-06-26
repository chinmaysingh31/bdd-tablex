---
icon: lucide/shield-check
---

# Record Validation

Use `validate_record()` for checks that involve one parsed record.

```python
from talika import RowTable, field


class UserTable(RowTable):
    name = field("name")
    role = field("role")

    def validate_record(self, context):
        if self.role not in {"admin", "editor"}:
            raise ValueError(f"Unsupported role: {self.role}")
```

Validation runs after parsers and defaults.

## Context-aware validation

```python
class UserTable(RowTable):
    role = field("role")

    def validate_record(self, context):
        if self.role not in context.user_data["allowed_roles"]:
            raise ValueError(f"Role {self.role!r} is not allowed")
```

```python
UserTable.parse(
    [["role"], ["editor"]],
    context={"allowed_roles": {"admin", "editor"}},
)
```

## Source-aware custom errors

Use `TableError.from_cell()` when the error should point at one field cell.

```python
from talika import TableError


raise TableError.from_cell(
    "Invalid role",
    self.source_for("role"),
    schema=type(self),
)
```

Ordinary exceptions are wrapped as `record_validation_failed`.
