# Custom Group Rules

`ColumnGroupExpander` provides reusable table mechanics without restricting a
project to the built-in numeric, alphabetic, prefix, or suffix conventions.

This example defines a different grammar:

```gherkin
| References | R1~R3         | R4    |
| Kind*      | [3]Article    | Poll  |
| Headline*  | Regional news | Vote? |
```

- `R1~R3` is a project reference range.
- `[3]Article` places the repeat count in brackets.
- Ordinary values are copied across their reference group.

## Custom range contract

A range rule exposes `expand(cell, context)` and returns `TableCell` values:

```python
class ReferenceRange:
    def expand(self, cell, context):
        if "~" not in cell.value:
            return [cell]

        # Parse and validate the project's syntax.
        return [
            cell.with_value("R1"),
            cell.with_value("R2"),
            cell.with_value("R3"),
        ]
```

Returning `[cell]` means that the value is a normal single key.

## Custom repeat contract

A repeat rule exposes `expand(cell, expected_count, context)`:

```python
class BracketRepeat:
    def expand(self, cell, expected_count, context):
        if not cell.value.startswith("["):
            return [cell] * expected_count

        # Parse [3]Article and validate the count.
        return [cell.with_value("Article") for _ in range(expected_count)]
```

The rule must return exactly one value for every expanded key.

## Combine custom rules with reusable mechanics

```python
class ReferenceContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="References",
        range_rule=ReferenceRange(),
        repeat_rule=BracketRepeat(),
    )

    reference = id_field("References")
    kind = field("Kind*", required=True)
```

The expander handles rectangular table checks, group iteration, count checks,
source preservation, and construction of the final `TableData`.

If a custom rule raises `ValueError`, the expander wraps it as a source-aware
`BDDTableError`. A custom rule may also raise `BDDTableError` directly when it
needs more control.

For a table shape that does not fit grouped columns, override
`transform_table()` instead. That lower-level escape hatch remains available.
