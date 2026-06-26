---
icon: lucide/box
---

# Typed Records

By default, `parse()` returns instances of your schema class.

```python
users = UserTable.parse([
    ["name", "age"],
    ["Alice", "30"],
])

assert users[0].name == "Alice"
assert users[0].age == 30
```

Those records are lightweight objects built after parsing and validation.

## Record helpers

Use `as_dict()` when you need declared fields as a plain dictionary:

```python
assert users[0].as_dict() == {"name": "Alice", "age": 30}
```

Use `source_for()` when custom validation needs to raise an error at a specific
cell:

```python
cell = users[0].source_for("age")
```

## Output models

Schemas can return your own objects:

```python
from dataclasses import dataclass
from talika import RowTable, field


@dataclass(frozen=True)
class User:
    name: str
    age: int


class UserTable(RowTable):
    output_model = User

    name = field("name")
    age: int = field("age")
```

`UserTable.parse(...)` now returns `list[User]`. `parse_records()` still returns
schema records when you need source metadata or intermediate values.
