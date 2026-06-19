# Local Record References

`reference()` resolves local IDs after every record has been constructed and
before validation hooks run:

```python
class LinkedContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline")
    parent = reference("Parent")
    related = reference("Related", many=True)
```

For this table:

```gherkin
| IDs      | 1    | 2     | 3     |
| Headline | Root | Child | Other |
| Parent   |      | 1     | 1     |
| Related  | 2, 3 |       | 2     |
```

`item_2.parent` is the parsed record for ID `1`, and `item_1.related` is a list
containing records `2` and `3`.

## Configuration

- `target="id"` selects the schema attribute used as the lookup key.
- `many=True` resolves a list rather than one record.
- `separator=","` controls list syntax for many references.
- Empty single references become `None`; empty many references become `[]`.

Reference targets must be unique. Missing targets produce source-aware errors
at the reference cell. Self-references and cycles are allowed by the resolver;
projects can reject them in `validate_record()` or `validate_records()`.

References currently resolve to source-aware schema records. When combined
with `output_model`, those schema records are passed as the reference field
values to the model constructor.
