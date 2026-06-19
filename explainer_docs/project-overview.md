# Project Overview

`bdd-tablex` is a Python package for teams that write BDD scenarios with data
tables, especially with `pytest-bdd`. It lets those teams declare small,
dataclass-style table schemas that parse raw table rows, validate the table
shape, convert cell values, preserve source locations, and return typed records
or project domain objects.

## Problem It Solves

BDD data tables are great for readable examples, but most BDD tools hand a step
definition a raw `list[list[str]]`. That creates several common problems:

- Step definitions collect repetitive parsing code.
- Required columns or rows are checked late or inconsistently.
- Strings like `"true"`, `"30"`, `"A, B"`, or `"random"` stay untyped unless
  every step remembers to convert them.
- Error messages often point to the step function, not the feature-file cell.
- Compact project-specific table syntax is hard to reuse safely.
- As tables grow, the table contract lives in human convention instead of code.
- CI cannot easily validate feature tables before running scenarios.

`bdd-tablex` moves those concerns into reusable schemas and helpers. Step
definitions can remain focused on the scenario action.

## Core Idea

A table schema is a Python class. Field declarations describe the BDD labels,
whether values are required, how values are parsed, and what should happen when
data is missing or extra.

```python
from bdd_tablex import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)
    active: bool = field("active", default=True)
```

That schema becomes the contract for a row-oriented table:

```gherkin
| name  | role  | active |
| Alice | admin | true   |
```

Parsing returns records whose attributes match the schema:

```python
users = UserTable.parse(datatable)
assert users[0].name == "Alice"
assert users[0].active is True
```

Column-oriented tables use the same idea, but the first column holds labels and
each later column is one record. This is useful when each item has many fields:

```gherkin
| IDs       | 1       | 2       |
| Type*     | Article | Poll    |
| Headline* | Hello   | QA Poll |
```

## What Makes It Valuable

`bdd-tablex` gives a project three things at once:

- Readable BDD tables for humans.
- Typed and validated records for code.
- Precise diagnostics for authors and tooling.

The important part is that these do not fight each other. A feature file can
stay expressive, while the parser preserves exact row, column, item ID, and
original cell text through conversions and transformations.

## What It Does Not Try To Be

The project is careful about scope:

- It does not impose one universal BDD table grammar.
- It does not perform business actions.
- It does not require pytest-bdd for direct schema parsing.
- It does not require Pydantic or any runtime dependency for normal parsing.
- It does not hide project semantics inside the package.

The package owns the table mechanics. The project using it owns domain meaning.
For example, the library can dispatch the token `"random"` through `CellDSL`,
but the consuming test project decides whether `"random"` means a generated
headline, generated SKU, generated user, or something else.

## Design Philosophy

The source and contributing notes show a consistent design philosophy:

- Keep schema declarations small and ordinary Python.
- Preserve feature-file source locations through every stage.
- Keep the direct parsing API independent from pytest.
- Make extension contracts explicit and easy to test.
- Distinguish a missing field from an explicitly empty cell.
- Provide focused examples for every public capability.
- Prefer project-owned syntax over a general built-in grammar.

This makes the package useful both for simple test suites and for teams that
need more advanced authoring conventions.

## Smallest Feature To Biggest Feature

At the smallest level, `bdd-tablex` can parse one table column into one record
attribute:

```python
name = field("name")
```

A little bigger, it can require fields, infer parsers from annotations, and
return typed values:

```python
age: int = field("age", required=True)
active: bool = field("active", default=True)
```

Then it can validate a record:

```python
def validate_record(self, context):
    if self.role not in context.user_data["allowed_roles"]:
        raise ValueError("Unsupported role")
```

Then it can validate relationships across a whole table:

```python
@classmethod
def validate_records(cls, records, context):
    ...
```

At the largest level, it supports mixed record variants, compact column-group
expansion, custom cell DSL rules, references between records, output model
construction, schema introspection, and static feature-file checking.

## The Main Product Story

The project is best explained as a reliability layer for BDD table authorship.
It gives teams a way to keep feature files readable while making table parsing
explicit, reusable, typed, and tool-friendly.

Before:

```python
@given("the following users exist:")
def users_exist(datatable):
    # Parse headers by hand, check required columns by hand,
    # convert booleans by hand, raise approximate errors by hand.
```

After:

```python
@given("the following users exist:")
def users_exist(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=UserTable)
```

That shift is the core selling point. It removes fragile glue code without
making feature authors give up readable tables.

