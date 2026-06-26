---
icon: lucide/file-cog
---

# Table Contracts

A Talika schema is a table contract written as a Python class.

```python
from talika import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    age: int = field("age")
```

The contract says:

- the table may contain a `name` column
- `name` is required
- the table may contain an `age` column
- `age` should be parsed as an `int`

## Labels and attributes

The label is what appears in the feature table:

```python
name = field("Full name", required=True)
```

The attribute is what Python code reads:

```python
user.name
```

This lets feature files use readable labels while test code keeps normal Python
names.

## Parse APIs

Use `parse()` for normal test code:

```python
users = UserTable.parse(datatable)
```

Use `parse_records()` when you specifically want schema record objects before
output conversion:

```python
records: list[UserTable] = UserTable.parse_records(datatable)
```

The functional APIs are thin delegates for teams that prefer schema-as-argument
style:

```python
from talika import parse_table

users = parse_table(UserTable, datatable)
```
