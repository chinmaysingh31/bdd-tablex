---
icon: lucide/square-function
---

# Parser Factories

Parser factories return callables for `field(parser=...)`.

```python
from talika import RowTable, compose, each, field, integer, split, string


class ScoreTable(RowTable):
    scores = field(
        "scores",
        parser=compose(split(","), each(compose(string(strip=True), integer()))),
    )
```

```python
record = ScoreTable.parse([["scores"], ["1, 2, 3"]])[0]
assert record.scores == [1, 2, 3]
```

## Scalar parsers

- `string(strip=True, lower=True, upper=True)`
- `integer(base=10)`
- `floating()`
- `decimal()`
- `boolean()`

## Vocabulary parsers

- `choice("Draft", "Published", case_sensitive=False)`
- `map_value({"high": 3, "low": 1})`

`choice()` returns the canonical string you configured. `map_value()` returns
the Python value from the mapping.

## List and pipeline parsers

- `split(",")` converts one cell into `list[str]`
- `compose(a, b, c)` runs parsers left-to-right
- `each(parser)` applies a parser to every item in a non-string iterable
- `optional(parser)` maps empty or null-like values to `None`

Parser failures are wrapped as `TableError` with the original cell location.
