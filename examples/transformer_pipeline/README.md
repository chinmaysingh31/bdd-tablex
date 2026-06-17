# Transformer pipelines

`compose_transformers()` runs reusable structural operations from left to
right:

```python
table_transformer = compose_transformers(
    RenameContentIDs(),
    ColumnGroupExpander(...),
)
```

Every stage receives `TableData`, `ParseContext`, and the schema identity.
Changed cells should use `with_value()` so later errors continue pointing to
the syntax in the feature file. A stage returning anything other than
`TableData` fails with a structured `invalid_transform` diagnostic.

