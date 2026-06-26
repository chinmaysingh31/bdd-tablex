---
icon: lucide/clipboard-check
---

# pytest-bdd

Talika does not replace pytest-bdd. It parses the datatable that pytest-bdd
already passes to a step function.

## Direct schema parsing

```python
from pytest_bdd import given


@given("the users:", target_fixture="users")
def users(datatable):
    return UserTable.parse(datatable)
```

## Fixture facade

Talika also registers a `talika` pytest fixture.

```python
@given("the users:", target_fixture="users")
def users(datatable, talika):
    return talika.parse(datatable, schema=UserTable)
```

Use `parse_records()` when the step needs schema records even if the schema has
an `output_model`.

```python
records = talika.parse_records(datatable, schema=UserTable)
```

## Functional API

Some teams prefer a function call with the schema as an argument:

```python
from talika import parse_table, parse_table_records

users = parse_table(UserTable, datatable)
records = parse_table_records(UserTable, datatable)
```

These helpers delegate to the schema methods. There is only one parsing
lifecycle.
