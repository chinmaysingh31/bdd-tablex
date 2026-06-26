---
icon: lucide/map-pin
---

# Source-Aware Errors

Talika errors are designed for feature authors and tools.

```text
Required field has an empty value (code=empty_required, schema=UserTable, field='name', row=2, column=1, value=''). Hint: Fill the cell, or remove required=True if an explicit empty value should be valid.
```

The message is readable, but the structured attributes are the important
contract.

## TableError

`TableError` represents one diagnostic. It can include:

- `code`
- `schema`
- `field`
- `row`
- `column`
- `item_id`
- `value`
- `hint`

## TableErrors

Use collect mode to find multiple independent problems in one parse:

```python
UserTable.parse(datatable, error_mode="collect")
```

Example output:

```text
Table contains 2 errors:
  1. Required field has an empty value (code=empty_required, schema=UserTable, field='name', row=2, column=1, value=''). Hint: Fill the cell, or remove required=True if an explicit empty value should be valid.
  2. Field parser failed: invalid literal for int() with base 10: 'old' (code=parser_failed, schema=UserTable, field='age', row=2, column=2, value='old'). Hint: Check the cell value or adjust the field parser for this syntax.
```

## Stable codes

Human messages may improve over time. Integrations should use stable error
codes such as `missing_required`, `empty_required`, `parser_failed`,
`reference_failed`, and `unknown_variant`.
