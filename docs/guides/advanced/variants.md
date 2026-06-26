---
icon: lucide/git-branch
---

# Variants

Use variants when one table contains records with different shapes.

```python
from talika import ColumnTable, TableFields, discriminator, field, id_field, split


class ArticleFields(TableFields):
    body = field("Body", required=True)


class PollFields(TableFields):
    options = field("Options", required=True, parser=split(","))


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = discriminator(
        "Type",
        variants={"Article": ArticleFields, "Poll": PollFields},
    )
    headline = field("Headline", required=True)
```

```python
items = ContentTable.parse([
    ["IDs", "1", "2"],
    ["Type", "Article", "Poll"],
    ["Headline", "News", "Choose"],
    ["Body", "Article body", ""],
    ["Options", "", "Yes, No"],
])
```

Each record is an instance of the base table and the selected `TableFields`
component.

## Explicit variant classes

Use `discriminator_field()` plus decorators when you want named classes:

```python
class PaymentTable(RowTable):
    payment_type = discriminator_field("type")
    amount: int = field("amount", required=True)


@PaymentTable.variant("card")
class CardPayment(PaymentTable):
    last_four = field("last_four", required=True)
```

The discriminator parser runs before variant lookup, so register parsed values.
