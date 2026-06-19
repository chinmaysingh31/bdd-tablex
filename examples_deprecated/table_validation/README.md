# Whole-Table Validation

`validate_record()` checks one normalized record. `validate_records()` runs
after every schema record has been built and can enforce relationships across
the complete table.

```python
@classmethod
def validate_records(cls, records, context):
    primary_users = [record for record in records if record.primary]
    if len(primary_users) != 1:
        raise ValueError("Exactly one primary user is required")
```

Validators receive schema records, not output models. This gives them access
to parsed attributes and source metadata:

```python
raise BDDTableError.from_cell(
    "Email must be unique",
    duplicate.source_for("email"),
    schema=cls,
)
```

Plain exceptions are wrapped as table-level `BDDTableError`s. Raising
`BDDTableError` directly is preferred when a validator can identify a precise
offending cell.
