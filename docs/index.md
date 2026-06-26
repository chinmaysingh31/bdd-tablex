---
icon: lucide/table-properties
---

# Talika

## Typed data tables for pytest-bdd

Declare a table contract in Python. Talika turns pytest-bdd's raw
`list[list[str]]` into typed records with source-aware errors, without
replacing pytest or adding runtime dependencies.

Talika is the missing DataTableType-style layer for pytest-bdd: table-to-object
conversion, validation, and precise diagnostics for Python BDD teams.

```python
from talika import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    age: int = field("age")


users = UserTable.parse([
    ["name", "age"],
    ["Alice", "30"],
])

assert users[0].name == "Alice"
assert users[0].age == 30
```

## The raw datatable problem

pytest-bdd gives a step function a table as plain nested strings. That is a
useful starting point, but real suites quickly grow code like this:

```python
headers, *rows = datatable
users = [dict(zip(headers, row, strict=True)) for row in rows]

age = int(users[0]["age"])
role = users[0]["role"]
```

That code has no table contract, no typed output, and no way to tell a feature
author which source cell caused a `KeyError` or `ValueError`.

## What Talika adds

Talika makes the table shape explicit:

- **Contracts**: declare labels, required fields, aliases, defaults, parsers,
  validators, references, and variants in Python.
- **Typed records**: parse into schema records, dataclasses, Pydantic models, or
  any output object you build.
- **Source-aware errors**: failures carry stable codes plus row, column,
  field, value, and item ID when available.
- **Readable conventions**: tokens like `today`, `random`, `1..3`, or
  `admin|editor` can become documented project rules instead of scattered
  `if` statements.
- **Zero core dependencies**: install extras only for CLI checking or Pydantic
  output.

## A real error

```text
Required field has an empty value (code=empty_required, schema=UserTable, field='name', row=2, column=1, value=''). Hint: Fill the cell, or remove required=True if an explicit empty value should be valid.
```

That is the product: the person editing the feature file sees the row, column,
field, code, value, and hint.

## Next

Start with [Installation](start/install.md), then build your first contract in
[Quickstart](start/quickstart.md). If you are evaluating the fit, read
[Why Talika?](start/why.md).
