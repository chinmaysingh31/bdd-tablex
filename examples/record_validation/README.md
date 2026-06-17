# Record Validation Example

This example validates relationships between fields after a complete content
record has been parsed.

Field declarations can validate individual cells, but they cannot answer rules
such as:

- A Poll headline must end with `?`.
- An Article must have a category.

Those rules belong in `validate_record()`:

```python
class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)
    category = field("Category")

    def validate_record(self, context):
        if self.content_type == "Poll" and not self.headline.endswith("?"):
            raise ValueError("Poll headlines must end with a question mark")

        if self.content_type == "Article" and not self.category:
            raise ValueError("Articles must have a category")
```

The hook runs after cell parsers and defaults, so it sees the final normalized
record values. Returning normally means the record is valid.

## Failure diagnostics

For this invalid Poll:

```python
[
    ["IDs", "1", "2"],
    ["Type*", "Article", "Poll"],
    ["Headline*", "Market update", "Choose one"],
    ["Category", "Markets", ""],
]
```

the package raises a `BDDTableError` similar to:

```text
Record validation failed: Poll headlines must end with a question mark
(schema=ContentTable, column=3, item_id='2')
```

The original `ValueError` remains available as the exception cause.
