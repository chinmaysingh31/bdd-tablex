---
icon: lucide/repeat
---

# Transformers

Transformers convert `TableData` before schema parsing.

## Protocol

```python
def transform(self, table, context, *, schema=None):
    ...
```

Return `TableData`. Use `TableCell.with_value()` when derived values should
keep original source coordinates.

## Pipeline

```python
TransformerPipeline([first, second])
compose_transformers(first, second)
```

Transformers run left-to-right.

## Column group expansion

```python
ColumnGroupExpander(
    key_row,
    range_rule,
    repeat_rule,
)
```

Built-in range rules:

- `NumericRange(separator="..")`
- `AlphabeticRange(separator="-")`

Built-in repeat rules:

- `PrefixRepeat(separator=":")`
- `SuffixRepeat(separator=" x")`

Custom `RangeRule` and `RepeatRule` objects must return `TableCell` values.
