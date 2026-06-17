# Output Models

Set `output_model` when callers should receive project domain objects instead
of lightweight schema records:

```python
@dataclass(frozen=True)
class User:
    name: str
    age: int


class UserTable(RowTable):
    output_model = User

    name = field("name")
    age = field("age", parser=integer())
```

The model is constructed with keyword arguments from the normalized record.
This works directly with dataclasses and other classes that accept matching
keyword arguments.

The lifecycle remains explicit:

1. parse and convert fields
2. construct source-aware schema records
3. run `validate_record()`
4. run `validate_records()`
5. construct `output_model` instances

Model construction failures become `BDDTableError`s with the source row or
item column. Pydantic models use the same interface and are demonstrated in a
separate optional-dependency example.
