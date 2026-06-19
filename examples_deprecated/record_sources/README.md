# Record Source Metadata

Every schema record carries a read-only `RecordSource`:

```python
bob = users[1]

assert bob.table_source.row == 3
assert bob.table_source.column is None
assert bob.table_source.item_id is None
```

Use the schema attribute name to retrieve one original cell:

```python
role_cell = bob.source_for("role")

assert role_cell.source_row == 3
assert role_cell.source_column == 2
assert role_cell.source_value == "editor"
```

For column-oriented records, `table_source.column` identifies the source ID
column and `table_source.item_id` contains the parsed local ID.

Source metadata is most useful in project validation:

```python
raise BDDTableError.from_cell(
    "Duplicate role assignment",
    duplicate.source_for("role"),
    schema=type(duplicate),
)
```

Missing optional fields do not have source cells because no feature-file cell
exists for them. `source_for()` raises `KeyError` in that case.
