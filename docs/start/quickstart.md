---
icon: lucide/rocket
---

# Quickstart

This page starts with a plain pytest-bdd datatable shape and adds one Talika
contract.

## 1. Start with the table

pytest-bdd supplies a datatable as nested strings:

```python
datatable = [
    ["name", "age"],
    ["Alice", "30"],
]
```

## 2. Declare a row table

```python
from talika import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    age: int = field("age")
```

The field labels are the words in the feature table. The Python attribute names
are what your test code uses.

## 3. Parse typed records

```python
users = UserTable.parse(datatable)

assert users[0].name == "Alice"
assert users[0].age == 30
```

The `age: int` annotation gives Talika an integer parser. Explicit parsers are
available when you want project-specific syntax.

## 4. See the error

```python
UserTable.parse([
    ["name", "age"],
    ["", "old"],
])
```

The first failure is source-aware:

```text
Required field has an empty value (code=empty_required, schema=UserTable, field='name', row=2, column=1, value=''). Hint: Fill the cell, or remove required=True if an explicit empty value should be valid.
```

Use collect mode when authors should see every independent problem in one pass:

```python
UserTable.parse(datatable, error_mode="collect")
```

## 5. Use it in a pytest-bdd step

```python
from pytest_bdd import given


@given("the users:", target_fixture="users")
def users(datatable):
    return UserTable.parse(datatable)
```

Talika does not replace pytest-bdd. It handles the table boundary and returns
objects your tests can use.
