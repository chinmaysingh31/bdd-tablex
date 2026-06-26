---
icon: lucide/wrench
---

# Custom Parsers

A parser receives the current cell value and a `CellContext`.

```python
from talika import RowTable, field


def parse_code(value, context):
    prefix = context.user_data["prefix"]
    return f"{prefix}{value}"


class CodeTable(RowTable):
    code = field("code", parser=parse_code)
```

```python
record = CodeTable.parse(
    [["code"], ["A1"]],
    context={"prefix": "user-"},
)[0]

assert record.code == "user-A1"
```

## CellContext

The context includes:

- `schema`
- `field_name`
- `field_label`
- `row`
- `column`
- `item_id`
- `source_value`
- `user_data`

`value` may already be transformed by a table transformer. `source_value`
records what was written in the original feature table.

## Parser failures

If a custom parser raises an ordinary exception, Talika wraps it:

```text
Field parser failed: not accepted (code=parser_failed, schema=CodeTable, field='code', row=2, column=1, value='bad')
```

Raise `TableError` yourself when you need full control over the diagnostic.
