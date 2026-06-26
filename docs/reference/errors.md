---
icon: lucide/alert-triangle
---

# Errors

Talika errors are structured diagnostics.

## TableError

Attributes:

- `message`
- `schema`
- `field`
- `row`
- `column`
- `item_id`
- `value`
- `code`
- `hint`

Use `TableError.from_cell(message, cell, ...)` to create a diagnostic at a
specific source cell.

## TableErrors

`TableErrors` aggregates multiple `TableError` objects in collect mode.

```python
try:
    UserTable.parse(datatable, error_mode="collect")
except TableErrors as exc:
    for error in exc:
        print(error.code, error.row, error.column)
```

## Error codes

Stable `TableErrorCode` values:

- `table_error`
- `schema_definition`
- `invalid_context`
- `table_empty`
- `header_empty`
- `ragged_row`
- `duplicate_label`
- `unknown_field`
- `missing_required`
- `empty_required`
- `empty_optional`
- `default_factory_failed`
- `parser_failed`
- `transform_failed`
- `invalid_transform`
- `unknown_variant`
- `inapplicable_field`
- `duplicate_id`
- `reference_failed`
- `record_validation_failed`
- `table_validation_failed`
- `output_failed`

Tools should use codes instead of scraping human-readable error text.
