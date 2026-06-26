---
icon: lucide/binary
---

# Type Annotations

Talika can infer parsers from common Python annotations.

```python
from decimal import Decimal
from enum import Enum
from typing import Literal

from talika import RowTable, field


class Status(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class ProductTable(RowTable):
    count: int = field("count")
    ratio: float = field("ratio")
    price: Decimal = field("price")
    active: bool = field("active")
    status: Status = field("status")
    state: Literal["draft", "published"] = field("state")
```

Supported inference:

- `int`
- `float`
- `bool`
- `Decimal`
- enums
- string `Literal[...]`
- simple optionals such as `int | None`

## Optionals

```python
class UserTable(RowTable):
    age: int | None = field("age")
```

Empty strings and configured null-like tokens become `None`.

## Lists are explicit

Talika does not infer a cell syntax for `list[T]`.

```python
class UserTable(RowTable):
    tags: list[str] = field("tags")
```

The value remains the raw cell text. Use `split()`, `each()`, or a custom parser
when a cell should become a list.

## Explicit parsers win

```python
from talika import string


class UserTable(RowTable):
    code: int = field("code", parser=string(upper=True))
```

The explicit parser is used instead of annotation inference.
