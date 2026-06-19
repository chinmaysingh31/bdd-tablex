# Collected diagnostics

Normal parsing remains fail-fast. Pass `error_mode="collect"` when authors
benefit from fixing several independent cells in one edit:

```python
try:
    UserTable.parse(datatable, error_mode="collect")
except BDDTableErrors as errors:
    for error in errors:
        print(error.code, error.row, error.column, error.message)
```

Each contained `BDDTableError` keeps its schema, field, row, column, item ID,
source value, cause, and stable error code. Parsing collects errors only while
continuation is trustworthy. It does not run reference or table validators on
a partial record set, because those secondary failures would be misleading.

