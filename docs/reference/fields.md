---
icon: lucide/sliders-horizontal
---

# Fields

Field declarations are descriptors collected by schema classes.

## field

```python
field(
    label,
    *,
    required=False,
    default=MISSING,
    default_factory=MISSING,
    parser=None,
    aliases=(),
    empty="raw",
)
```

`empty` accepts:

- `"raw"`: keep `""`
- `"parse"`: send `""` to the parser
- `"none"`: return `None`
- `"error"`: reject `""`

Required fields cannot declare defaults.

## id_field

```python
id_field(label, *, parser=None, aliases=())
```

`ColumnTable` requires exactly one `id_field`. `RowTable` may use one when
parser context, default factories, or diagnostics need an `item_id`.

## discriminator_field

```python
discriminator_field(label, *, parser=None, aliases=())
```

Declares the field used to select explicit variants registered with
`@Table.variant(value)`.

## discriminator

```python
discriminator(label, *, variants, parser=None, aliases=())
```

`variants` maps parsed discriminator values to `TableFields` subclasses.
Talika composes those components with the base table schema.

## reference

```python
reference(
    label,
    *,
    target="id",
    many=False,
    separator=",",
    required=False,
    default=MISSING,
    aliases=(),
)
```

References resolve to records in the same parsed table.
