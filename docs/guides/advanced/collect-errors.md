---
icon: lucide/list-checks
---

# Collect Errors

By default, Talika stops at the first table error.

```python
UserTable.parse(datatable)
```

Use collect mode when authors should fix several independent problems in one
pass.

```python
UserTable.parse(datatable, error_mode="collect")
```

## TableErrors

Collect mode raises `TableErrors`, an aggregate of `TableError` objects.

```text
Table contains 2 errors:
  1. Required field has an empty value (code=empty_required, schema=UserTable, field='name', row=2, column=1, value=''). Hint: Fill the cell, or remove required=True if an explicit empty value should be valid.
  2. Field parser failed: invalid literal for int() with base 10: 'old' (code=parser_failed, schema=UserTable, field='age', row=2, column=2, value='old'). Hint: Check the cell value or adjust the field parser for this syntax.
```

## Tooling value

Every contained error keeps its stable `code`, source coordinates, field, value,
and hint. That makes collect mode useful for CI, editor diagnostics, and feature
file linting.
