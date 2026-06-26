---
icon: lucide/map-pin
---

# Source And Context

## TableCell

```python
TableCell(value, source_row, source_column, source_value)
```

Use `TableCell.from_value(value, row=..., column=...)` for untransformed cells.
Use `cell.with_value(new_value)` inside transformations to preserve source
coordinates.

## TableData

```python
TableData.from_rows(rows)
TableData.from_cells(rows)
TableData.ensure(table)
table.cell(row, column)
table.to_rows()
```

`cell(row, column)` uses one-based indexes.

## RecordSource

Parsed records expose:

```python
record.table_source
record.source_for("field_name")
```

Missing optional fields have no source cell.

## ParseContext

```python
ParseContext.from_value(value)
```

Normalizes `None`, mappings, and existing `ParseContext` objects. User mappings
are copied into read-only `user_data`.

## CellContext

Passed to field parsers. Contains schema, field name, label, source row,
source column, item ID, source value, and user data.

## DefaultContext

Passed to default factories. Contains schema, field name, label, item ID, and
user data.
