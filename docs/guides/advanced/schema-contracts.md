---
icon: lucide/file-json
---

# Schema Contracts

Use `describe()` to inspect a schema without parsing a table.

```python
contract = UserTable.describe()

assert contract.orientation == "row"
```

The returned `TableContract` is frozen and machine-readable.

```python
payload = contract.as_dict()
```

Contracts include:

- schema name
- orientation
- fields
- variants
- policies
- transformer name
- output model name
- output builder name

## CLI describe

The CLI exposes the same contract:

```bash
talika describe app.schemas:UserTable
talika describe app.schemas:UserTable --format json
```

This is useful for generated docs, editor integrations, and schema drift checks
in CI.
