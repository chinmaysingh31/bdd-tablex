---
icon: lucide/braces
---

# CellDSL Tokens

`CellDSL` lets a project promote table vocabulary into reusable parser rules.

```python
from talika import CellDSL

cells = CellDSL()


@cells.token("random", fields=("headline",))
def random_headline(context):
    return context.user_data["faker"].headline()
```

Attach the DSL as a field parser:

```python
class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline", parser=cells)
```

Now `random` has a documented meaning for `headline`.

## Field scoping

Scopes use Python field names, not table labels.

```python
headline = field("Headline")
```

The scope is `"headline"`.

Field-scoped tokens take precedence over global tokens with the same value.
