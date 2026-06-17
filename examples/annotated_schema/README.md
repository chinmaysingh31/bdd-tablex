# Annotation-Driven Schemas

When a field has no explicit parser, `bdd-tablex` can infer common conversion
behavior from its Python annotation:

```python
class AnnotatedUserTable(RowTable):
    name: str = field("name")
    age: int | None = field("age")
    active: bool = field("active")
    tags: list[str] = field("tags")
```

Supported inference includes `str`, `int`, `float`, `bool`, `Decimal`, enums,
string `Literal` values, `list[T]`, and optionals containing one supported
non-`None` type.

`list[T]` uses comma-separated input. Optional inferred parsers convert empty,
`none`, and `null` values to `None`.

An explicit parser always wins:

```python
count: int = field("count", parser=my_project_count_parser)
```

Unsupported annotations leave the raw string unchanged. This avoids guessing
how arbitrary domain classes should be constructed.
