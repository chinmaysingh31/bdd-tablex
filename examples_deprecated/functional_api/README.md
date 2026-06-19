# Functional API

Most examples use the schema class directly:

```python
users = UserTable.parse(datatable)
```

`bdd-tablex` also exposes a functional style for teams that prefer explicit
parser calls:

```python
users = parse_table(UserTable, datatable)
records = parse_table_records(UserTable, datatable)
```

The functional helpers do not implement a separate parser. They delegate to
the same schema lifecycle, so required fields, type conversion, validation,
source metadata, output models, context, and collect mode behave exactly the
same.

In pytest or pytest-bdd projects, the fixture style remains available:

```python
users = bdd_table.parse(datatable, schema=UserTable)
records = bdd_table.parse_records(datatable, schema=UserTable)
```

Recommended mental model:

1. Use `Schema.parse()` as the default.
2. Use `parse_table()` when functional style reads better in your codebase.
3. Use the `bdd_table` fixture when pytest dependency injection makes a step
   cleaner.
