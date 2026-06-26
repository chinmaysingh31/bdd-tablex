---
icon: lucide/regex
---

# CellDSL Patterns

Patterns use regular-expression `fullmatch`.

```python
from talika import CellDSL

cells = CellDSL()


@cells.pattern(r"(?P<count>\d+) words")
def generated_words(match, context):
    return context.user_data["faker"].words(int(match["count"]))
```

The whole cell must match the pattern. Use `.*` explicitly if your project
really wants substring behavior.

## Predicates

Use predicates when a rule is awkward to express as regex.

```python
@cells.when(lambda value, context: value.startswith("QA-"))
def qa_value(value, context):
    return value.removeprefix("QA-")
```

Predicates run after exact tokens and patterns.

## Fallback

A fallback handles values that match no explicit rule.

```python
@cells.fallback
def fallback(value, context):
    return value.upper()
```

A DSL with a fallback matches every value, which matters when composing DSLs.
