---
icon: lucide/box
---

# Output Models

By default, Talika returns schema record objects. Set `output_model` when you
want your own types.

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

```python
users = UserTable.parse([
    ["name", "age"],
    ["Alice", "30"],
])

assert users == [User(name="Alice", age=30)]
```

## parse_records

`parse_records()` skips output conversion:

```python
records = UserTable.parse_records(datatable)
```

Use it when you need source metadata or schema record methods.

## Custom output builder

Override `build_output()` for custom factories:

```python
class UserTable(RowTable):
    name = field("name")

    @classmethod
    def build_output(cls, record, context):
        return {"user": record.name}
```

Pydantic v2 models work through the same `output_model` contract. Install
`talika[pydantic]` only when you use that integration.
