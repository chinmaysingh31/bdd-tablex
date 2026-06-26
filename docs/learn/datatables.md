---
icon: lucide/table
---

# Data Tables

A pytest-bdd datatable is a table attached to a step. In Python, the step
receives it as a raw `list[list[str]]`.

```gherkin
Given the users:
  | name  | age |
  | Alice | 30  |
```

```python
[
    ["name", "age"],
    ["Alice", "30"],
]
```

That raw shape is simple and flexible. It is also where table glue starts to
spread across a test suite.

## The usual glue

```python
headers, *rows = datatable
users = [dict(zip(headers, row, strict=True)) for row in rows]

for user in users:
    user["age"] = int(user["age"])
```

This works until a field is renamed, a cell is empty, or one step uses
`active=yes` while another uses `active=true`.

## What Talika changes

Talika lets you keep the readable feature table and move the table rules into a
schema:

```python
from talika import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    age: int = field("age")
```

Now the table has a contract. Talika knows which labels are allowed, which
fields are required, how each value should be parsed, and where each value came
from.

## The important idea

Talika is not trying to make Gherkin clever. It is trying to keep the boundary
between human-authored table text and Python test code explicit.
