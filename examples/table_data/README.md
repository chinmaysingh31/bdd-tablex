# TableData and TableCell

This example introduces the source-aware table model used by `bdd-tablex`.
Most projects do not need to construct it manually: `RowTable.parse()` and
`ColumnTable.parse()` still accept the ordinary list of lists supplied by
pytest-bdd.

The model becomes useful when a project needs to inspect or transform table
syntax while retaining useful error locations.

## Wrap a pytest-bdd table

```python
table = TableData.from_rows(datatable)
```

Every string is represented by a `TableCell`:

```python
cell = table.cell(row=3, column=2)

assert cell.value == "disabled"
assert cell.source_row == 3
assert cell.source_column == 2
assert cell.source_value == "disabled"
```

Rows and columns are one-based because those coordinates match feature files
and error messages.

## Change a value without losing its origin

Transformers should use `with_value()`:

```python
source = TableCell.from_value("3:Article", row=2, column=2)
article = source.with_value("Article")

assert article.value == "Article"
assert article.source_value == "3:Article"
```

One source cell may create several transformed cells. They can all point back
to the syntax that produced them.

## Build a transformed table

```python
transformed = TableData.from_cells(
    [
        [label_cell, first_value_cell],
        [other_label_cell, other_value_cell],
    ]
)
```

`from_cells()` expects existing `TableCell` objects and does not invent source
locations. `to_rows()` is available when ordinary current-value rows are
needed for logging or inspection.

## Parse it normally

```python
users = UserTable.parse(table)
```

Passing `TableData` does not change schema behavior. It only lets downstream
errors use the original source coordinates and source text.

Field parsers receive the current value as their first argument. When a table
has been transformed, `context.source_value` lets the parser inspect the
original compact syntax as well.
