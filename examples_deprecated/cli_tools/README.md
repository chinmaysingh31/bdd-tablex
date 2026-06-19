# CLI tools

This example shows the two command-line features that help before a scenario
executes:

- `bdd-tablex check` validates feature-file tables against a schema.
- `bdd-tablex describe` prints the schema contract for humans or tools.

The schema is intentionally small:

```python
class UserTable(RowTable):
    name = field("name", required=True)
    age: int = field("age")
```

Run a static check with JSON output:

```powershell
bdd-tablex check examples/cli_tools/users.feature `
  --schema examples/cli_tools/schemas.py:UserTable `
  --step "the following CLI users:" `
  --format json
```

The JSON payload includes `status`, `matched_tables`, `error_count`, and one
structured object per diagnostic. Each diagnostic includes the stable error
`code`, source row and column, field label, offending value when available, and
an optional human hint.

Inspect the schema contract:

```powershell
bdd-tablex describe examples/cli_tools/schemas.py:UserTable
bdd-tablex describe examples/cli_tools/schemas.py:UserTable --format json
```

The text form is quick to read in a terminal. The JSON form is designed for
documentation generators, editor extensions, and CI tools.
