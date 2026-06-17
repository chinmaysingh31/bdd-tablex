# Defaults, aliases, and parsing policies

This example covers table-contract evolution without embedding migration logic
inside step definitions.

## Default factories

A static `default=` is shared as an ordinary value. Use `default_factory=` for
generated values, mutable containers, or context-dependent defaults:

```python
role = field(
    "role",
    default_factory=lambda context: context.user_data["default_role"],
)
tags: list[str] = field("tags", default_factory=lambda context: [])
```

The factory runs only when the complete field row or column is absent. An
explicitly empty cell remains `""`, preserving the package's missing-versus-
empty distinction. `DefaultContext` provides the schema, field name, canonical
label, item ID when available, and project `user_data`.

## Aliases

Aliases accept older or alternate BDD wording while retaining one canonical
schema name:

```python
name = field("name", aliases=("full name",), required=True)
```

A table cannot contain both `name` and `full name`, because that would provide
two values for one field.

## Additional-field policies

Schemas default to `unknown_fields = "forbid"`. Alternatives are:

- `"ignore"`: accept and discard unknown fields.
- `"preserve"`: expose them through the immutable `record.table_extras` map.

Variant schemas provide the equivalent `inapplicable_fields` policy for values
that belong to another variant.

