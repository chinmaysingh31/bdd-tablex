---
icon: lucide/circle-help
---

# Why Talika?

pytest-bdd gives Python teams Gherkin and pytest together. The gap is data
tables.

Cucumber ecosystems have a DataTableType-style layer for turning authored
tables into domain objects. pytest-bdd exposes the table as raw
`list[list[str]]`. Talika fills that missing layer for Python: table contracts,
typed records, validation, and diagnostics that point back to the source cell.

## The pain Talika removes

Without Talika, table parsing often starts as simple glue:

```python
headers, *rows = datatable
users = [dict(zip(headers, row, strict=True)) for row in rows]
```

Then the suite grows:

```python
age = int(user["age"])
roles = user["roles"].split("|")
if user["active"].lower() not in {"yes", "no"}:
    raise ValueError("bad active value")
```

The problem is not that this code is hard once. The problem is that every step
function invents its own parser, its own defaults, its own conventions, and its
own weak error messages.

## The Talika layer

Talika puts those rules in one contract:

```python
from talika import RowTable, boolean, field, split


class UserTable(RowTable):
    name = field("name", required=True)
    age: int = field("age")
    roles = field("roles", parser=split("|"))
    active = field("active", parser=boolean(), default=True)
```

Now the authored table stays readable, while the test receives validated
records.

## Comparison

| Tool | Good at | Gap Talika covers |
| --- | --- | --- |
| Raw pytest-bdd datatable | Passing table text into a step | No contract, typed output, validation layer, or source-aware diagnostics |
| Scenario Outlines | Generating separate scenarios | Not for structured multi-record data inside one scenario |
| factory_boy | Creating data in Python | Does not validate human-authored `.feature` tables |
| Cucumber DataTableType | Table conversion in Cucumber stacks | Not the pytest-bdd Python table contract layer |
| Talika | Compiling pytest-bdd tables into typed records | Focused on tables only, not a test runner or fixture framework |

## Why source-aware errors matter

Feature files are edited by humans. A useful failure should tell them where to
look:

```text
Field parser failed: invalid literal for int() with base 10: 'old' (code=parser_failed, schema=UserTable, field='age', row=2, column=2, value='old'). Hint: Check the cell value or adjust the field parser for this syntax.
```

That stable `code` is useful to humans, CI, editors, and future tooling. Talika
does not ask tools to scrape prose.

## What Talika is not

Talika is not a test runner, not a global fixture registry, and not a business
action layer. It is a compile step for table data: take authored table text,
validate it, and return objects your tests already know how to use.
