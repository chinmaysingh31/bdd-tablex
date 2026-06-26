---
icon: lucide/repeat
---

# Column Group Expansion

`ColumnGroupExpander` handles compact column-oriented tables where one source
column expands into several logical item columns.

```python
from talika import ColumnGroupExpander, NumericRange, PrefixRepeat

expander = ColumnGroupExpander(
    key_row="IDs",
    range_rule=NumericRange(".."),
    repeat_rule=PrefixRepeat(":"),
)
```

```python
from talika import ColumnTable, field, id_field


class ContentTable(ColumnTable):
    table_transformer = expander

    id = id_field("IDs")
    content_type = field("Type")
```

This source table:

```python
[
    ["IDs", "1..3"],
    ["Type", "3:Article"],
]
```

becomes:

```python
[
    ["IDs", "1", "2", "3"],
    ["Type", "Article", "Article", "Article"],
]
```

## Built-in rules

- `NumericRange("..")`: `1..3`
- `AlphabeticRange("-")`: `A-C`
- `PrefixRepeat(":")`: `3:Article`
- `SuffixRepeat(" x")`: `Article x3`

Custom rules can implement any project convention, but must return
`TableCell` objects so source metadata is preserved.
