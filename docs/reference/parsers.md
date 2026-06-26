---
icon: lucide/square-function
---

# Parsers

Parsers are callables with this shape:

```python
def parser(value, context):
    ...
```

`context` is a `CellContext`.

## Factories

```python
string(strip=False, lower=False, upper=False)
integer(base=10)
floating()
decimal()
boolean(true_values=("true", "yes", "1", "on"), false_values=("false", "no", "0", "off"), case_sensitive=False)
choice(*values, case_sensitive=True)
split(separator=",", strip_items=True, keep_empty=False)
map_value(values, case_sensitive=True)
compose(*parsers)
each(parser)
optional(parser, none_values=("none", "null"), case_sensitive=False)
```

Configuration errors raise `ValueError` when the parser is built.

Runtime parser failures are wrapped as `TableError` with source-cell details.

## Annotation inference

Talika infers parsers for:

- `int`
- `float`
- `bool`
- `Decimal`
- enums
- string `Literal[...]`
- simple optionals such as `int | None`

Explicit `field(parser=...)` always wins.

Unsupported annotations leave the value unchanged. `list[T]` does not infer a
cell syntax.
