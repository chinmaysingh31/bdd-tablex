# Reusable Field Parsers

Field parsers convert one logical table cell after table transformation and
before record validation. `bdd-tablex` includes small parser factories for
common conversions while preserving support for ordinary custom functions.

```python
class ProductTable(RowTable):
    sku = field("sku", parser=string(strip=True, upper=True))
    price = field("price", parser=decimal())
    active = field("active", parser=boolean())
```

Available parser helpers include `string`, `integer`, `floating`, `decimal`,
`boolean`, `choice`, `split`, `map_value`, and `optional`.

## Composition

`compose()` runs parsers from left to right. `each()` applies a parser to every
member of an iterable:

```python
tags = field(
    "tags",
    parser=compose(
        split(","),
        each(string(strip=True, lower=True)),
    ),
)
```

The cell `"news, Featured"` becomes `["news", "featured"]`.

## Optional values

`optional(parser)` maps an explicit empty cell and the tokens `none` or `null`
to `None`, then delegates other values:

```python
age = field("age", parser=optional(integer()))
```

This opt-in behavior does not change the package default: an empty optional
cell remains `""` unless its parser explicitly handles empty cells.

Parser exceptions are wrapped in `BDDTableError` with the source field, row,
column, item ID where available, and original cell text.
