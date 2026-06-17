# Custom output factories

`output_model` covers dataclasses, Pydantic models, and other keyword
constructors. Override `build_output()` when construction needs context,
selected fields, a factory service, or a different call signature:

```python
@classmethod
def build_output(cls, record, context):
    return context.user_data["factory"].create_user(
        name=record.name,
        source=record.table_source,
    )
```

The hook runs after field conversion, reference resolution, record validation,
and whole-table validation. Exceptions become source-aware `output_failed`
diagnostics. Variant schemas and variant field components can each provide
their own output builder.

