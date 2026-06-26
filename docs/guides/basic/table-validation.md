---
icon: lucide/list-checks
---

# Table Validation

Use `validate_records()` for checks that need the whole parsed table.

```python
from talika import RowTable, TableError, field


class UserTable(RowTable):
    email = field("email", required=True)

    @classmethod
    def validate_records(cls, records, context):
        seen = {}
        for record in records:
            if record.email in seen:
                raise TableError.from_cell(
                    "Duplicate email",
                    record.source_for("email"),
                    schema=cls,
                    field="email",
                )
            seen[record.email] = record
```

Table validation runs after records are parsed and after local references are
resolved.

## When to use it

Use table validation for:

- duplicate checks
- cross-record rules
- aggregate constraints
- rules that need references to be resolved first

Use `validate_record()` for rules local to one record.
