---
icon: lucide/combine
---

# CellDSL Composition

Use composition when you have shared table vocabulary plus feature-specific
rules.

```python
from talika import CellDSL, compose_cell_dsls

shared = CellDSL()
content = CellDSL()


@shared.token("none")
def none_value(context):
    return None


@content.token("random", fields=("headline",))
def random_headline(context):
    return context.user_data["faker"].headline()


parser = compose_cell_dsls(content, shared)
```

The first DSL that matches owns the value. If none match, the original text
passes through.

## Precedence

Dispatch order inside one DSL is:

1. exact tokens
2. patterns
3. predicates
4. fallback

Composition adds one more layer: DSLs are consulted left-to-right.
