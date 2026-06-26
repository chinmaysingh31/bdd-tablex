---
icon: lucide/sliders-horizontal
---

# Fields

Fields map human-facing table labels to Python attributes.

```python
from talika import RowTable, field


class UserTable(RowTable):
    name = field("Full name", required=True)
```

The feature table uses `Full name`. Python code reads `user.name`.

## Required fields

```python
name = field("name", required=True)
```

Required fields must be present and non-empty.

## Aliases

Aliases let feature vocabulary evolve without breaking old tables.

```python
name = field("name", aliases=("full name", "display name"), required=True)
```

The canonical label and one of its aliases cannot appear in the same table.
Talika reports that as `duplicate_label`.

## Unknown fields

Talika rejects undeclared labels by default and today supports only:

```python
unknown_fields = "forbid"
```

That is intentional for now: unexpected table columns should be visible because
they often mean a typo, stale feature file, or schema drift.

## Labels are literal

Characters such as `*` have no built-in meaning.

```python
headline = field("Headline*", required=True)
```

The `*` is just part of the label. `required=True` is what makes the field
required.
