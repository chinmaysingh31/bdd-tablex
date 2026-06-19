# Context-Aware Validation Example

This example keeps changing project policy outside the table schema and passes
it into parsing as context.

```python
ACCESS_POLICY = {
    "admin": {"global"},
    "editor": {"eu", "us"},
}
```

The schema reads that policy from `context.user_data`:

```python
class UserAccessTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)
    region = field("region", required=True)

    def validate_record(self, context):
        policy = context.user_data["access_policy"]
        allowed_regions = policy.get(self.role)

        if allowed_regions is None:
            raise ValueError(f"Unknown role: {self.role}")
        if self.region not in allowed_regions:
            raise ValueError(
                f"Role {self.role!r} is not allowed in region {self.region!r}"
            )
```

The pytest-bdd step supplies the policy for that parse operation:

```python
users = bdd_table.parse(
    datatable,
    schema=UserAccessTable,
    context={"access_policy": ACCESS_POLICY},
)
```

This keeps the schema reusable across environments and avoids global mutable
configuration. For row-oriented tables, validation failures identify the
source row:

```text
Record validation failed: Role 'editor' is not allowed in region 'global'
(schema=UserAccessTable, row=2)
```
