---
icon: lucide/file-cog
---

# Schema

Schema classes declare table contracts.

## Classes

- `RowTable`: first row contains labels; later rows are records
- `ColumnTable`: first column contains labels; later columns are records
- `TableFields`: reusable field group for variants or mixins

## Parse methods

```python
Schema.parse(datatable, *, context=None, error_mode="first")
Schema.parse_records(datatable, *, context=None, error_mode="first")
```

`parse()` returns public output objects. `parse_records()` returns schema record
instances and skips output conversion.

`datatable` may be raw `list[list[str]]` or `TableData`.

`error_mode` accepts:

- `"first"`
- `"collect"`

## Hooks

```python
def validate_record(self, context): ...

@classmethod
def validate_records(cls, records, context): ...

@classmethod
def build_output(cls, record, context): ...

@classmethod
def transform_table(cls, table, context): ...
```

## Class attributes

```python
table_transformer = None
output_model = None
unknown_fields = "forbid"
inapplicable_fields = "forbid"
```

`unknown_fields` currently supports only `"forbid"`.

`inapplicable_fields` supports `"forbid"` and `"preserve"`.

## Variants

```python
@BaseTable.variant(value)
class ConcreteVariant(BaseTable):
    ...
```

Use `variant_for(value)` to retrieve a registered variant class.

Use `describe()` to return a `TableContract`.
