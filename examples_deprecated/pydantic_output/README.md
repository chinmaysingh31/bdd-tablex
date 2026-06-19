# Pydantic Output Models

Pydantic is an optional dependency. Install the package extra when a project
wants Pydantic model output:

```powershell
pip install "bdd-tablex[pydantic]"
```

Pydantic uses the same `output_model` interface as dataclasses:

```python
class UserModel(BaseModel):
    name: str
    age: int = Field(ge=18)


class UserTable(RowTable):
    output_model = UserModel

    name: str = field("name")
    age: int = field("age")
```

The schema annotation converts `age` to an integer. After schema and table
validation, `UserModel(**record.as_dict())` performs Pydantic validation.

Pydantic errors are wrapped in `BDDTableError` with the source record row or
item column and ID. The core package does not import Pydantic, so projects that
only use schema records or dataclasses do not need the dependency.
