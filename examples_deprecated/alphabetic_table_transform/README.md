# Declarative Alphabetic Group Expansion

This example configures the same table mechanics with different syntax and
semantics:

```gherkin
| Keys      | A-C           | D     |
| Kind*     | Article x3    | Poll  |
| Headline* | Regional news | Vote? |
```

```python
class AlphabeticContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="Keys",
        range_rule=AlphabeticRange(separator="-"),
        repeat_rule=SuffixRepeat(separator=" x"),
    )

    key = id_field("Keys")
    kind = field("Kind*", required=True)
    headline = field("Headline*", required=True)
```

## Alphabetic ranges

`AlphabeticRange` supports inclusive ranges such as `A-C` and `a-c`.
Endpoints must be single ASCII letters using the same case. Ordinary values
without the separator remain single keys.

## Suffix repeats

`SuffixRepeat` reads the count after the value. With separator `" x"`,
`Article x3` becomes three `Article` cells.

Changing the separator changes the surface syntax without changing the table
mechanics:

```python
SuffixRepeat(separator="*")  # Article*3
```

## Independent from the numeric convention

This schema does not configure one universal parser with a few flags. It
selects explicit rule objects whose names communicate their semantics. The
same `ColumnGroupExpander` only coordinates those rules and preserves source
locations.

The direct error example verifies that descending `C-A` points to the original
range cell at row 1, column 2.
