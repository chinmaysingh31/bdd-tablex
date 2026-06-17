# Declarative Numeric Group Expansion

This example uses reusable rules for a common grouped-column table:

```gherkin
| IDs       | 1..3            | 4                   |
| Type*     | 3:Article       | Poll                |
| Headline* | Shared headline | Is the market open? |
```

The schema declares both the syntax and its semantics:

```python
class NumericContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="IDs",
        range_rule=NumericRange(separator=".."),
        repeat_rule=PrefixRepeat(separator=":"),
    )

    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)
```

## What each object owns

`NumericRange` owns numeric range semantics:

- A value without `..` is one literal ID.
- `1..3` is an inclusive ascending integer range.
- Invalid or descending numeric ranges are rejected.

`PrefixRepeat` owns count-before-value semantics:

- `3:Article` repeats `Article` three times.
- The declared count must match the expanded ID group size.
- A value whose prefix is not an integer is ordinary text and is copied.

`ColumnGroupExpander` owns table mechanics:

- confirms that the first row is `IDs`
- confirms that the source table is rectangular
- expands each ID group
- copies normal values across groups
- validates rule return types and counts
- preserves every original source location
- builds the final `TableData`

## Error location

The executable example includes `1..3` with `2:Article`. The mismatch is
reported against the original repeat cell:

```text
Repeat expansion failed: Repeat count 2 does not match group size 3
(schema=NumericContentTable, row=2, column=2, value='2:Article')
```

No handwritten range loop or `transform_table()` override is needed for this
convention.
