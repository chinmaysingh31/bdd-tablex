# Detailed Feature Guide

This guide explains `bdd-tablex` slowly and practically. The shorter
[Feature Guide](feature-guide.md) is a map. This file is the long walkthrough:
what each feature does, why it exists, how it behaves, and how to use it with
small examples.

The most important idea:

```text
Feature file table text
    -> source-aware TableData
    -> optional table transformation
    -> schema parsing
    -> typed records
    -> references and validation
    -> optional output models
```

`bdd-tablex` is not trying to execute your business workflow. It is the layer
that makes BDD tables reliable input.

## 1. The Smallest Useful Example

Imagine this Gherkin table:

```gherkin
| name  | role  |
| Alice | admin |
```

Without `bdd-tablex`, a step function receives something like:

```python
[
    ["name", "role"],
    ["Alice", "admin"],
]
```

That is readable for humans, but code still has to:

- find the header indexes,
- check that required columns exist,
- convert values,
- report useful errors.

With `bdd-tablex`, the table contract becomes a class:

```python
from bdd_tablex import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)
```

Parse it:

```python
users = UserTable.parse(
    [
        ["name", "role"],
        ["Alice", "admin"],
    ]
)

assert users[0].name == "Alice"
assert users[0].role == "admin"
```

The result is a schema record. It behaves like a lightweight object whose
attributes match the declared fields.

## 2. RowTable

Use `RowTable` when the first row contains field labels and each later row is a
record.

```gherkin
| name  | role   | active |
| Alice | admin  | true   |
| Bob   | editor | false  |
```

```python
from bdd_tablex import RowTable, boolean, field


class UserTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)
    active = field("active", parser=boolean())
```

```python
users = UserTable.parse(datatable)

assert users[0].name == "Alice"
assert users[0].active is True
assert users[1].active is False
```

### When RowTable Feels Natural

Use row-oriented tables when:

- there are only a few fields,
- every row has the same shape,
- the scenario is listing many similar records,
- the table should be easy to scan horizontally.

Good examples:

```gherkin
| email          | role   |
| a@example.com  | admin  |
| b@example.com  | editor |
```

```gherkin
| sku | price | active |
| A1  | 12.50 | yes    |
| B2  | 8.00  | no     |
```

### RowTable Shape Rules

The first row is the header row.

Every later row must have the same number of cells as the header:

```gherkin
| name  | role  |
| Alice | admin |
| Bob   |
```

That second data row is ragged and produces a structured error with code
`ragged_row`.

## 3. ColumnTable

Use `ColumnTable` when the first column contains field labels and each later
column is one record.

```gherkin
| IDs       | 1       | 2       |
| Type*     | Article | Poll    |
| Headline* | Hello   | QA Poll |
| Category  | Markets |         |
```

```python
from bdd_tablex import ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)
    category = field("Category")
```

```python
items = ContentTable.parse(datatable)

assert items[0].id == "1"
assert items[0].headline == "Hello"
assert items[1].content_type == "Poll"
```

### When ColumnTable Feels Natural

Use column-oriented tables when:

- each item has many fields,
- each item needs a stable ID,
- the table would be too wide as a row table,
- you want compact grouped-column syntax later.

### ColumnTable Shape Rules

A `ColumnTable` must have exactly one `id_field()`.

The first row must be that ID field:

```gherkin
| IDs       | 1       | 2    |
| Headline* | News    | Poll |
```

This is valid for:

```python
id = id_field("IDs")
```

This is invalid:

```gherkin
| Headline* | News |
| IDs       | 1    |
```

Duplicate item IDs are rejected:

```gherkin
| IDs       | 1    | 1    |
| Headline* | News | Poll |
```

## 4. Labels Are Literal

Labels are just text. `bdd-tablex` does not decide that a star means required.

```python
class ContentTable(RowTable):
    headline = field("Headline*")
```

This table is valid and returns an empty string:

```gherkin
| Headline* |
|           |
```

To make it required, say so:

```python
headline = field("Headline*", required=True)
```

That design is intentional. Your project owns table vocabulary. The library
does not invent meaning from punctuation.

## 5. Missing Field Versus Empty Cell

This is one of the most important rules in the whole project.

### Missing Field

The field label is absent:

```gherkin
| name  |
| Alice |
```

Schema:

```python
class UserTable(RowTable):
    name = field("name", required=True)
    active = field("active", default=True)
```

Result:

```python
users = UserTable.parse(datatable)
assert users[0].active is True
```

The field `active` was missing, so the default applies.

### Empty Cell

The field exists, but the value is blank:

```gherkin
| name  | active |
| Alice |        |
```

Result:

```python
users = UserTable.parse(datatable)
assert users[0].active == ""
```

The author explicitly provided the `active` column and left the cell empty.
`bdd-tablex` preserves that choice.

### Why This Matters

Missing often means "use project default".

Empty often means "I intentionally want no value".

Conflating those two creates subtle test bugs, especially when feature files
are written by several people.

## 6. Required Fields

`required=True` checks two things:

1. the field label exists in the table,
2. each selected record has a non-empty value.

```python
class UserTable(RowTable):
    name = field("name", required=True)
```

Missing label:

```gherkin
| role  |
| admin |
```

Error code:

```text
missing_required
```

Empty value:

```gherkin
| name |
|      |
```

Error code:

```text
empty_required
```

## 7. Defaults

Use `default=` for simple static values:

```python
class UserTable(RowTable):
    name = field("name", required=True)
    active = field("active", default=True)
```

Input:

```gherkin
| name  |
| Alice |
```

Output:

```python
assert users[0].active is True
```

Do not use mutable objects as static defaults unless you truly want to share
that object. For lists or dictionaries, prefer `default_factory`.

## 8. Default Factories

Use `default_factory=` when the default should be generated per record or needs
parse context.

```python
class UserTable(RowTable):
    name = field("name", required=True)
    tags = field("tags", default_factory=lambda context: [])
```

The factory receives `DefaultContext`:

```python
def default_role(context):
    return context.user_data["default_role"]


class UserTable(RowTable):
    name = field("name", required=True)
    role = field("role", default_factory=default_role)
```

Parse with project data:

```python
users = UserTable.parse(
    [["name"], ["Alice"]],
    context={"default_role": "viewer"},
)

assert users[0].role == "viewer"
```

For `ColumnTable`, default factories can see the item ID:

```python
def generated_headline(context):
    return f"Generated for {context.item_id}"


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline", default_factory=generated_headline)
```

Input:

```gherkin
| IDs | 7 |
```

Output:

```python
assert items[0].headline == "Generated for 7"
```

## 9. Aliases

Aliases allow old or alternate table labels while keeping one canonical schema
attribute.

```python
class UserTable(RowTable):
    name = field("name", aliases=("full name", "display name"), required=True)
```

All of these can work:

```gherkin
| name  |
| Alice |
```

```gherkin
| full name |
| Alice     |
```

```gherkin
| display name |
| Alice        |
```

But this is rejected:

```gherkin
| name  | full name |
| Alice | Alice     |
```

Reason: one schema field would receive two values.

## 10. Unknown Field Policies

By default, unknown labels are errors.

```python
class UserTable(RowTable):
    name = field("name")
```

Input:

```gherkin
| name  | team |
| Alice | QA   |
```

Error code:

```text
unknown_field
```

### Ignore Unknown Fields

```python
class UserTable(RowTable):
    unknown_fields = "ignore"
    name = field("name")
```

Now `team` is accepted and discarded.

### Preserve Unknown Fields

```python
class UserTable(RowTable):
    unknown_fields = "preserve"
    name = field("name")
```

```python
user = UserTable.parse([["name", "team"], ["Alice", "QA"]])[0]

assert user.name == "Alice"
assert user.table_extras == {"team": "QA"}
```

This is useful during migrations. You can accept extra table data without
losing it.

## 11. Parsers

A field parser converts one cell value.

The parser contract is:

```python
def parser(value, context):
    return converted_value
```

Example:

```python
def parse_bool(value, context):
    return value.lower() == "true"


class UserTable(RowTable):
    active = field("active", parser=parse_bool)
```

The parser receives:

- the current value,
- a `CellContext`.

`CellContext` contains:

- `schema`
- `field_name`
- `field_label`
- `row`
- `column`
- `item_id`
- `source_value`
- `user_data`

Example using context:

```python
def prefix_from_context(value, context):
    return context.user_data["prefix"] + value


class UserTable(RowTable):
    name = field("name", parser=prefix_from_context)


users = UserTable.parse(
    [["name"], ["Alice"]],
    context={"prefix": "QA-"},
)

assert users[0].name == "QA-Alice"
```

## 12. Built-In Parser Helpers

`bdd-tablex` includes small parser factories.

### string

```python
name = field("name", parser=string(strip=True))
slug = field("slug", parser=string(lower=True))
code = field("code", parser=string(upper=True))
```

### integer

```python
age = field("age", parser=integer())
hex_value = field("hex", parser=integer(base=16))
```

### floating And decimal

```python
ratio = field("ratio", parser=floating())
price = field("price", parser=decimal())
```

Use `decimal()` for money-like values where exact decimal representation
matters.

### boolean

```python
active = field("active", parser=boolean())
```

Default true values:

```text
true, yes, 1, on
```

Default false values:

```text
false, no, 0, off
```

You can customize:

```python
enabled = field(
    "enabled",
    parser=boolean(true_values=("Y",), false_values=("N",), case_sensitive=True),
)
```

### choice

Validates and returns one allowed string:

```python
state = field("state", parser=choice("Draft", "Published"))
```

Case-insensitive input can still return canonical values:

```python
state = field("state", parser=choice("Draft", "Published", case_sensitive=False))
```

Input `"draft"` returns `"Draft"`.

### split

```python
tags = field("tags", parser=split(","))
```

Input:

```text
news, markets
```

Output:

```python
["news", "markets"]
```

### map_value

```python
priority = field("priority", parser=map_value({"high": 3, "low": 1}))
```

Input `"high"` returns `3`.

### compose

Runs parsers left to right:

```python
number = field("number", parser=compose(string(strip=True), integer()))
```

### each

Applies a parser to every item from a previous parser:

```python
scores = field("scores", parser=compose(split(","), each(integer())))
```

Input:

```text
1, 2, 3
```

Output:

```python
[1, 2, 3]
```

### optional

Maps empty strings and null-like tokens to `None`, then otherwise runs another
parser:

```python
age = field("age", parser=optional(integer()))
```

Inputs:

```text
""
"none"
"NULL"
"30"
```

Outputs:

```python
None
None
None
30
```

`optional(...)` opts into empty-cell parsing. That is why it can see `""`.

## 13. Annotation-Driven Conversion

Instead of writing parser factories explicitly, you can use supported type
annotations.

```python
from decimal import Decimal
from enum import Enum
from typing import Literal


class Status(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class ProductTable(RowTable):
    sku: str = field("sku")
    price: Decimal = field("price")
    active: bool = field("active")
    tags: list[str] = field("tags")
    status: Status = field("status")
    state: Literal["draft", "published"] = field("state")
```

Input:

```gherkin
| sku | price | active | tags           | status    | state |
| A1  | 12.30 | yes    | news, featured | published | draft |
```

Output:

```python
assert product.price == Decimal("12.30")
assert product.active is True
assert product.tags == ["news", "featured"]
assert product.status is Status.PUBLISHED
```

Explicit parsers take precedence:

```python
class WeirdTable(RowTable):
    count: int = field("count", parser=string(upper=True))
```

Even though `count` is annotated as `int`, the explicit parser wins.

Unsupported annotations leave values unchanged. That is safer than guessing.

## 14. CellDSL

`CellDSL` is for project-owned cell language.

It can handle exact tokens:

```python
from bdd_tablex import CellDSL

content_cells = CellDSL()


@content_cells.token("random")
def random_value(context):
    return context.user_data["generator"].headline(context.item_id)
```

Use it as a parser:

```python
class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True, parser=content_cells)
```

Input:

```gherkin
| IDs       | 1      |
| Headline* | random |
```

Output might be:

```python
assert items[0].headline == "Generated headline 1"
```

### Regex Patterns

Patterns use full-match regular expressions.

```python
@content_cells.pattern(r"(?P<count>\d+):word")
def generated_words(match, context):
    count = int(match["count"])
    return context.user_data["generator"].words(count)
```

Input:

```text
12:word
```

The whole value must match. These do not match:

```text
prefix-12:word
12:word-suffix
```

### Predicate Rules

Use `when()` when a regex would be awkward:

```python
@content_cells.when(lambda value, context: value.startswith("QA-"))
def qa_value(value, context):
    return value.removeprefix("QA-")
```

### Fallback

By default, unmatched values pass through unchanged. You can replace that:

```python
@content_cells.fallback
def normalize(value, context):
    return value.strip()
```

### Dispatch Order

For one `CellDSL`, dispatch order is:

1. exact tokens,
2. patterns,
3. predicates,
4. fallback,
5. pass-through.

Exact field-scoped tokens beat global tokens with the same value:

```python
cells = CellDSL()


@cells.token("random")
def global_random(context):
    return "global"


@cells.token("random", fields={"headline"})
def headline_random(context):
    return "headline"
```

For `headline`, `"random"` returns `"headline"`.

For another field, `"random"` returns `"global"`.

## 15. Composing Cell DSLs

Use `compose_cell_dsls()` when you want several independent DSLs.

```python
shared_cells = CellDSL()
content_cells = CellDSL()


@shared_cells.token("none")
def none_value(context):
    return None


@content_cells.pattern(r"fake:(.+)")
def fake_value(match, context):
    return f"generated-{match[1]}"


parser = compose_cell_dsls(shared_cells, content_cells)
```

First matching DSL wins:

```python
class ValueTable(RowTable):
    value = field("value", parser=parser)
```

Input:

```gherkin
| value      |
| none       |
| fake:title |
| literal    |
```

Output:

```python
[None, "generated-title", "literal"]
```

## 16. Source Metadata

Every record knows where it came from.

```python
record.table_source.row
record.table_source.column
record.table_source.item_id
record.source_for("headline")
```

For a row table:

```gherkin
| name  | role   |
| Alice | admin  |
| Bob   | editor |
```

Bob's record has:

```python
assert bob.table_source.row == 3
assert bob.table_source.column is None
assert bob.table_source.item_id is None
```

The role cell has:

```python
role_cell = bob.source_for("role")

assert role_cell.source_row == 3
assert role_cell.source_column == 2
assert role_cell.source_value == "editor"
```

For a column table:

```gherkin
| IDs       | 1    | 2    |
| Headline  | News | Poll |
```

The second record has:

```python
assert item.table_source.column == 3
assert item.table_source.item_id == "2"
```

## 17. Record Validation

Use `validate_record()` for rules about one record.

```python
class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)

    def validate_record(self, context):
        if self.content_type == "Poll" and not self.headline.endswith("?"):
            raise ValueError("Poll headline must end with a question mark")
```

Input:

```gherkin
| IDs       | 1       | 2          |
| Type*     | Article | Poll       |
| Headline* | News    | Choose one |
```

The second record fails. The wrapped error has the selected record location:

```text
code=record_validation_failed
column=3
item_id='2'
```

### Validation With Context

```python
class UserTable(RowTable):
    role = field("role")

    def validate_record(self, context):
        if self.role not in context.user_data["allowed_roles"]:
            raise ValueError(f"Role {self.role!r} is not allowed")
```

```python
UserTable.parse(
    [["role"], ["editor"]],
    context={"allowed_roles": {"admin", "editor"}},
)
```

### Raising A Source-Aware Error Yourself

Plain exceptions point to the record. If you want a specific cell, raise
`BDDTableError.from_cell(...)`.

```python
from bdd_tablex import BDDTableError


class UserTable(RowTable):
    email = field("email")

    def validate_record(self, context):
        if "@" not in self.email:
            raise BDDTableError.from_cell(
                "Email must contain @",
                self.source_for("email"),
                schema=type(self),
                field="email",
            )
```

## 18. Whole-Table Validation

Use `validate_records()` for rules across records.

```python
class UserTable(RowTable):
    email = field("email", required=True)

    @classmethod
    def validate_records(cls, records, context):
        seen = {}
        for record in records:
            if record.email in seen:
                raise BDDTableError.from_cell(
                    "Duplicate email",
                    record.source_for("email"),
                    schema=cls,
                )
            seen[record.email] = record
```

Input:

```gherkin
| email         |
| a@example.com |
| a@example.com |
```

The error points to the second duplicate email cell.

Use table validation for:

- uniqueness,
- exactly one primary record,
- parent/child consistency,
- "at least one item" rules,
- cross-record totals.

## 19. Local Record References

Use `reference()` when one record points to another record in the same table.

```python
class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline")
    parent = reference("Parent")
    related = reference("Related", many=True)
```

Input:

```gherkin
| IDs      | 1    | 2     | 3     |
| Headline | Root | Child | Other |
| Parent   |      | 1     | 1     |
| Related  | 2, 3 |       | 2     |
```

Output:

```python
root, child, other = ContentTable.parse(datatable)

assert root.parent is None
assert child.parent is root
assert other.parent is root
assert root.related == [child, other]
assert child.related == []
```

### Reference Options

```python
reference(
    "Manager",
    target="username",
    many=False,
)
```

```python
reference(
    "Related",
    target="id",
    many=True,
    separator=";",
)
```

### Typed IDs

If the target field has a parser, reference keys use that parser too.

```python
class ContentTable(ColumnTable):
    id = id_field("IDs", parser=integer())
    parent = reference("Parent")
```

Input:

```gherkin
| IDs    | 1 | 2 |
| Parent |   | 1 |
```

Output:

```python
assert items[0].id == 1
assert items[1].parent is items[0]
```

The reference string `"1"` is converted to integer `1` for lookup.

### Reference Timing

References resolve after all records are created and before validation. This
means `validate_record()` can inspect linked records directly.

## 20. Output Models

By default, `parse()` returns schema records.

Set `output_model` when callers should receive project objects.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    name: str
    age: int


class UserTable(RowTable):
    output_model = User

    name = field("name")
    age: int = field("age")
```

Input:

```gherkin
| name  | age |
| Alice | 30  |
```

Output:

```python
users = UserTable.parse(datatable)
assert users == [User(name="Alice", age=30)]
```

### parse_records Skips Output Conversion

```python
records = UserTable.parse_records(datatable)

assert isinstance(records[0], UserTable)
assert records[0].source_for("age").source_value == "30"
```

Use `parse_records()` when you want schema metadata or type-checker-friendly
schema attributes.

### Custom build_output

Use `build_output()` when the output object does not accept all schema fields as
keyword arguments.

```python
@dataclass(frozen=True)
class UserCommand:
    display: str


class UserTable(RowTable):
    name = field("name")
    role = field("role")

    @classmethod
    def build_output(cls, record, context):
        prefix = context.user_data.get("prefix", "")
        return UserCommand(display=f"{prefix}{record.name}:{record.role}")
```

```python
commands = UserTable.parse(
    [["name", "role"], ["Alice", "admin"]],
    context={"prefix": "user:"},
)

assert commands == [UserCommand(display="user:Alice:admin")]
```

## 21. Field Components

Use `TableFields` to share field declarations and behavior.

```python
class AuditFields(TableFields):
    created_by = field("created_by")
    trace_id = field("trace_id")


class ArticleTable(RowTable, AuditFields):
    headline = field("headline")
```

Input:

```gherkin
| headline | created_by | trace_id |
| News     | Alice      | trace-1  |
```

Output:

```python
article = ArticleTable.parse(datatable)[0]

assert article.headline == "News"
assert article.created_by == "Alice"
assert article.trace_id == "trace-1"
```

Field components can also provide:

- parsers,
- references,
- `validate_record()`,
- `output_model`,
- custom `build_output()`.

They are very useful for variants.

## 22. Variants

Variants let one table contain several related record shapes.

### Row-Oriented Variant Example

Input:

```gherkin
| type | amount | last_four | account |
| card | 25     | 4242      |         |
| bank | 50     |           | QA-001  |
```

Schema:

```python
class PaymentTable(RowTable):
    payment_type = discriminator_field("type")
    amount: int = field("amount", required=True)


@PaymentTable.variant("card")
class CardPayment(PaymentTable):
    last_four = field("last_four", required=True)


@PaymentTable.variant("bank")
class BankPayment(PaymentTable):
    account = field("account", required=True)
```

Output:

```python
payments = PaymentTable.parse(datatable)

assert isinstance(payments[0], CardPayment)
assert payments[0].last_four == "4242"

assert isinstance(payments[1], BankPayment)
assert payments[1].account == "QA-001"
```

### Column-Oriented Variant Example

Input:

```gherkin
| IDs       | 1            | 2          |
| Type*     | Article      | Poll       |
| Headline* | Market news  | Choose?    |
| Body*     | Article body |            |
| Options*  |              | Yes, No    |
```

Schema:

```python
class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = discriminator_field("Type*")
    headline = field("Headline*", required=True)


@ContentTable.variant("Article")
class ArticleContent(ContentTable):
    body = field("Body*", required=True)


@ContentTable.variant("Poll")
class PollContent(ContentTable):
    options: list[str] = field("Options*", required=True)
```

Output:

```python
article, poll = ContentTable.parse(datatable)

assert isinstance(article, ArticleContent)
assert article.body == "Article body"

assert isinstance(poll, PollContent)
assert poll.options == ["Yes", "No"]
```

### Empty Cells For Other Variants

The Article row has an empty `Options*` cell. That is fine because `Options*`
belongs to Poll.

The Poll row has an empty `Body*` cell. That is fine because `Body*` belongs to
Article.

### Non-Empty Inapplicable Values

This is suspicious:

```gherkin
| type | body       | options |
| Poll | unexpected | Yes,No  |
```

For a Poll, `body` belongs to Article. Because it is non-empty, the default
behavior rejects it with code `inapplicable_field`.

You can change that with:

```python
class ContentTable(RowTable):
    inapplicable_fields = "preserve"
```

Then the extra value appears in `record.table_extras`.

### Discriminator Parsers

The discriminator parser runs before variant lookup.

```python
class ContentTable(RowTable):
    content_type = discriminator_field(
        "type",
        parser=lambda value, context: value.casefold(),
    )


@ContentTable.variant("article")
class ArticleContent(ContentTable):
    body = field("body")
```

Input `"ARTICLE"` selects variant key `"article"`.

### Declarative Variant Style

When the variant fields are reusable components, use `discriminator(...)`.

```python
class ArticleFields(TableFields):
    body = field("Body*", required=True)


class PollFields(TableFields):
    options: list[str] = field("Options*", required=True)


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = discriminator(
        "Type*",
        variants={
            "Article": ArticleFields,
            "Poll": PollFields,
        },
    )
    headline = field("Headline*", required=True)
```

Internally, `bdd-tablex` creates concrete variant schema classes. A parsed
Article is both a `ContentTable` and an `ArticleFields`.

```python
article = ContentTable.parse(datatable)[0]

assert isinstance(article, ContentTable)
assert isinstance(article, ArticleFields)
```

Use this when variants are naturally reusable field groups.

### Per-Variant Output Models

Each variant can construct a different output model.

```python
@dataclass(frozen=True)
class CardPayment:
    payment_type: str
    amount: int
    last_four: str


@dataclass(frozen=True)
class BankPayment:
    payment_type: str
    amount: int
    account: str


@PaymentTable.variant("card")
class CardPaymentRow(PaymentTable):
    output_model = CardPayment
    last_four = field("last_four", required=True)


@PaymentTable.variant("bank")
class BankPaymentRow(PaymentTable):
    output_model = BankPayment
    account = field("account", required=True)
```

`PaymentTable.parse(...)` can return a mixed list:

```python
[
    CardPayment(...),
    BankPayment(...),
]
```

## 23. Error Collection

Default parsing is fail-fast:

```python
UserTable.parse(datatable)
```

Use collect mode when authors benefit from several errors at once:

```python
from bdd_tablex import BDDTableErrors


try:
    UserTable.parse(datatable, error_mode="collect")
except BDDTableErrors as errors:
    for error in errors:
        print(error.code, error.row, error.column, error.message)
```

Example invalid table:

```gherkin
| name | age |
|      | old |
|      | ??? |
```

Possible collected codes:

```text
empty_required
parser_failed
empty_required
parser_failed
```

Collect mode is careful. If early structural or cell parsing failures make
later stages unreliable, it stops before references, validators, or output
models. That avoids misleading secondary errors.

## 24. TableData And TableCell

Transformers use `TableData` and `TableCell`.

Raw input:

```python
[
    ["value"],
    ["news"],
]
```

Becomes:

```python
table = TableData.from_rows([["value"], ["news"]])
```

Inspect a cell:

```python
cell = table.cell(2, 1)

assert cell.value == "news"
assert cell.source_row == 2
assert cell.source_column == 1
assert cell.source_value == "news"
```

Indexes are one-based because feature file coordinates are one-based.

### Current Value Versus Source Value

A transformer can change the current value:

```python
source = TableCell.from_value("3:Article", row=2, column=2)
changed = source.with_value("Article")

assert changed.value == "Article"
assert changed.source_value == "3:Article"
assert changed.source_row == 2
assert changed.source_column == 2
```

That is the key to source-aware transformations.

The parser sees `value == "Article"`.

Diagnostics still report `value == "3:Article"` at row 2, column 2.

## 25. What Is A Table Transformation?

A table transformation changes the table before normal schema parsing.

It answers:

"The feature author wrote a compact or project-specific table. What logical
table should the schema actually parse?"

Example source table:

```gherkin
| value |
| news  |
```

After transformation:

```gherkin
| value |
| NEWS  |
```

Then the schema parses the transformed value.

Transformations are useful for:

- expanding compact syntax,
- normalizing labels,
- renaming rows,
- applying project shorthand,
- generating several logical records from one source cell,
- composing reusable preprocessing stages.

## 26. Custom transform_table

Override `transform_table()` for full control.

```python
from bdd_tablex import RowTable, TableData, field


class UpperTable(RowTable):
    value = field("value")

    @classmethod
    def transform_table(cls, table, context):
        rows = [list(row) for row in table.rows]
        rows[1][0] = rows[1][0].with_value(rows[1][0].value.upper())
        return TableData.from_cells(rows)
```

Input:

```gherkin
| value |
| news  |
```

Output:

```python
record = UpperTable.parse(datatable)[0]
assert record.value == "NEWS"
```

### Why Use with_value

This would work logically but lose source metadata:

```python
TableCell.from_value("NEWS", row=2, column=1)
```

Prefer:

```python
old_cell.with_value("NEWS")
```

Now an error still points to the original cell the author wrote.

### transform_table Must Return TableData

This is invalid:

```python
@classmethod
def transform_table(cls, table, context):
    return table.to_rows()
```

The parser expects `TableData`, not raw rows, after transformation.

### transform_table Replaces table_transformer

The default `BaseTable.transform_table()` uses `table_transformer` when one is
configured.

If you override `transform_table()` yourself, your method takes control.

This means:

```python
class MyTable(ColumnTable):
    table_transformer = ColumnGroupExpander(...)

    @classmethod
    def transform_table(cls, table, context):
        return table
```

The `ColumnGroupExpander` will not run, because the override did not call it.

If you want both custom logic and configured transformer behavior, call it
explicitly:

```python
class MyTable(ColumnTable):
    table_transformer = ColumnGroupExpander(...)

    @classmethod
    def transform_table(cls, table, context):
        prepared = cls.table_transformer.transform(table, context, schema=cls)
        rows = [list(row) for row in prepared.rows]
        # more custom changes here
        return TableData.from_cells(rows)
```

Or use a transformer pipeline, which is usually cleaner.

## 27. TableTransformer Objects

A reusable transformer is any object with a `transform()` method:

```python
class UppercaseValues:
    def transform(self, table, context, *, schema=None):
        rows = [list(row) for row in table.rows]
        rows[1][0] = rows[1][0].with_value(rows[1][0].value.upper())
        return TableData.from_cells(rows)
```

The method receives:

- `table`: current `TableData`,
- `context`: parse context,
- `schema`: the schema class or schema name, used mainly for diagnostics.

It must return `TableData`.

Use a transformer object when:

- the logic is reusable across schemas,
- you want to compose stages,
- the behavior is structural table preprocessing rather than one schema's
  special case.

## 28. Transformer Pipelines

A pipeline runs transformers left to right.

```python
from bdd_tablex import compose_transformers


table_transformer = compose_transformers(
    FirstStage(),
    SecondStage(),
    ThirdStage(),
)
```

Think of it like:

```python
current = original_table
current = FirstStage().transform(current, context, schema=Schema)
current = SecondStage().transform(current, context, schema=Schema)
current = ThirdStage().transform(current, context, schema=Schema)
return current
```

Each stage sees the output of the previous stage.

### Simple Pipeline Example

Input:

```gherkin
| value |
| news  |
```

Transformers:

```python
class Uppercase:
    def transform(self, table, context, *, schema=None):
        rows = [list(row) for row in table.rows]
        rows[1][0] = rows[1][0].with_value(rows[1][0].value.upper())
        return TableData.from_cells(rows)


class Prefix:
    def transform(self, table, context, *, schema=None):
        rows = [list(row) for row in table.rows]
        rows[1][0] = rows[1][0].with_value("QA-" + rows[1][0].value)
        return TableData.from_cells(rows)
```

Schema:

```python
class ValueTable(RowTable):
    table_transformer = compose_transformers(Uppercase(), Prefix())
    value = field("value")
```

Result:

```python
record = ValueTable.parse([["value"], ["news"]])[0]
assert record.value == "QA-NEWS"
```

Why? The first stage changes `"news"` to `"NEWS"`. The second stage changes
`"NEWS"` to `"QA-NEWS"`.

### Source Metadata Through A Pipeline

Even after both stages:

```python
record.source_for("value").source_value == "news"
```

That is because both transformers used `old_cell.with_value(...)`.

### Pipeline Error Handling

If a stage raises `BDDTableError`, the pipeline lets it pass through. That is
an intentional, already-source-aware diagnostic.

If a stage raises another exception, the pipeline wraps it:

```text
Table transformer stage 2 (NormalizeLabels) failed: ...
```

If a stage returns something other than `TableData`, the error code is
`invalid_transform`.

### When To Use A Pipeline

Use a pipeline when there are separate preprocessing jobs:

1. normalize labels,
2. expand grouped columns,
3. apply another structural cleanup.

Example:

```python
class RenameContentIDs:
    def transform(self, table, context, *, schema=None):
        rows = [list(row) for row in table.rows]
        if rows[0][0].value == "Content IDs":
            rows[0][0] = rows[0][0].with_value("IDs")
        return TableData.from_cells(rows)


class ContentTable(ColumnTable):
    table_transformer = compose_transformers(
        RenameContentIDs(),
        ColumnGroupExpander(
            key_row="IDs",
            range_rule=NumericRange(".."),
            repeat_rule=PrefixRepeat(":"),
        ),
    )

    id = id_field("IDs")
    content_type = field("Type*", required=True)
```

Input:

```gherkin
| Content IDs | 1..2      |
| Type*       | 2:Article |
```

Stage 1 changes the label:

```gherkin
| IDs   | 1..2      |
| Type* | 2:Article |
```

Stage 2 expands the grouped columns:

```gherkin
| IDs   | 1       | 2       |
| Type* | Article | Article |
```

Then normal `ColumnTable` parsing runs.

## 29. ColumnGroupExpander In Plain English

`ColumnGroupExpander` solves this problem:

"One source column in the feature file actually describes several logical
records."

Source table:

```gherkin
| IDs       | 1..3      | 4    |
| Type      | 3:Article | Poll |
| Headline  | Shared    | Vote |
```

Logical table after expansion:

```gherkin
| IDs       | 1       | 2       | 3       | 4    |
| Type      | Article | Article | Article | Poll |
| Headline  | Shared  | Shared  | Shared  | Vote |
```

Schema:

```python
class ContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="IDs",
        range_rule=NumericRange(".."),
        repeat_rule=PrefixRepeat(":"),
    )

    id = id_field("IDs")
    content_type = field("Type")
    headline = field("Headline")
```

Parse:

```python
items = ContentTable.parse(datatable)

assert [item.id for item in items] == ["1", "2", "3", "4"]
assert [item.content_type for item in items] == [
    "Article",
    "Article",
    "Article",
    "Poll",
]
```

### The Three Actors

`ColumnGroupExpander` has three main parts:

```python
ColumnGroupExpander(
    key_row="IDs",
    range_rule=NumericRange(".."),
    repeat_rule=PrefixRepeat(":"),
)
```

`key_row` says which first-row label identifies the key/ID row.

`range_rule` expands source key cells.

`repeat_rule` expands non-key value cells to match the number of keys.

### Range Rule Example

With `NumericRange("..")`:

```text
1..3 -> 1, 2, 3
4    -> 4
```

The range rule only handles the key row.

### Repeat Rule Example

With `PrefixRepeat(":")`:

```text
3:Article -> Article, Article, Article
Shared    -> Shared, Shared, Shared
```

The repeat rule handles all rows below the key row.

### Important Point

The separator is not the meaning.

This:

```python
NumericRange("-")
```

means numeric ranges like:

```text
7-9 -> 7, 8, 9
```

This:

```python
AlphabeticRange("-")
```

means alphabetic ranges like:

```text
A-C -> A, B, C
```

Same separator, different semantics.

The rule object defines meaning.

## 30. Built-In Range Rules

### NumericRange

```python
NumericRange(separator="..")
```

Examples:

```text
1..3 -> 1, 2, 3
7    -> 7
```

Invalid:

```text
3..1        # descending
one..three  # endpoints are not integers
1..2..3     # too many endpoints
```

Ranges are inclusive and must be ascending.

### AlphabeticRange

```python
AlphabeticRange(separator="-")
```

Examples:

```text
A-C -> A, B, C
a-c -> a, b, c
Z   -> Z
```

Invalid:

```text
C-A    # descending
A-c    # mixed case
AA-BB  # endpoints are not single letters
```

It supports ASCII letters.

## 31. Built-In Repeat Rules

### PrefixRepeat

```python
PrefixRepeat(separator=":")
```

Examples with expected count 3:

```text
3:Article    -> Article, Article, Article
Shared       -> Shared, Shared, Shared
News: Europe -> News: Europe, News: Europe, News: Europe
```

Why does `"News: Europe"` copy as a literal? Because the text before `:` is not
an integer. That avoids treating normal prose as repeat syntax.

Invalid with expected count 3:

```text
2:Article  # count mismatch
3:         # empty repeated value
```

### SuffixRepeat

```python
SuffixRepeat(separator=" x")
```

Examples with expected count 3:

```text
Article x3    -> Article, Article, Article
Shared        -> Shared, Shared, Shared
Version xnext -> Version xnext, Version xnext, Version xnext
```

Invalid:

```text
Article x2  # count mismatch
 x3         # empty repeated value
```

## 32. Custom Range And Repeat Rules

You can define your own compact syntax.

Suppose your project writes references like:

```text
R1~R3
```

And repeats like:

```text
[3]Article
```

Custom range rule:

```python
class ReferenceRange:
    def expand(self, cell, context):
        if "~" not in cell.value:
            return [cell]

        left, right = cell.value.split("~", 1)
        if not (left.startswith("R") and right.startswith("R")):
            raise ValueError("Invalid reference range")

        start = int(left.removeprefix("R"))
        end = int(right.removeprefix("R"))
        if start > end:
            raise ValueError("Reference range must be ascending")

        return [cell.with_value(f"R{number}") for number in range(start, end + 1)]
```

Custom repeat rule:

```python
class BracketRepeat:
    def expand(self, cell, expected_count, context):
        if not cell.value.startswith("["):
            return [cell] * expected_count

        count_text, _, value = cell.value[1:].partition("]")
        count = int(count_text)
        if count != expected_count:
            raise ValueError("Repeat count does not match group size")
        if not value:
            raise ValueError("Repeated value cannot be empty")

        return [cell.with_value(value) for _ in range(count)]
```

Use them:

```python
class ReferenceContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="References",
        range_rule=ReferenceRange(),
        repeat_rule=BracketRepeat(),
    )

    reference = id_field("References")
    kind = field("Kind")
```

Input:

```gherkin
| References | R1~R3      |
| Kind       | [3]Article |
```

Logical table:

```gherkin
| References | R1      | R2      | R3      |
| Kind       | Article | Article | Article |
```

### Custom Rule Requirements

Range rules must return `TableCell` values.

Repeat rules must return `TableCell` values.

Repeat rules must return exactly `expected_count` cells.

Use `cell.with_value(...)` to preserve source information.

## 33. Transformer Or Parser?

This question comes up a lot.

Use a field parser when you are changing one cell value into one Python value:

```text
"yes" -> True
"1, 2, 3" -> [1, 2, 3]
"12.50" -> Decimal("12.50")
```

Use a transformer when you are changing the table structure or labels before
schema parsing:

```text
"1..3" -> three item columns
"Content IDs" row label -> "IDs"
one compact source column -> several logical columns
```

Use `CellDSL` when it is still one cell in, one value out, but your project
wants reusable symbolic syntax:

```text
"random" -> generated headline
"12:word" -> generated text
```

## 34. Full Transformer Walkthrough

Start with this table:

```gherkin
| Content IDs | 1..2      | 3     |
| Type*       | 2:Article | Poll  |
| Headline*   | 2:random  | Vote? |
```

The schema expects:

```python
id = id_field("IDs")
```

But the feature uses `"Content IDs"`. Also, it uses grouped IDs.

We need two stages:

1. rename `"Content IDs"` to `"IDs"`,
2. expand grouped columns.

Stage 1:

```python
class RenameContentIDs:
    def transform(self, table, context, *, schema=None):
        rows = [list(row) for row in table.rows]
        first_cell = rows[0][0]
        if first_cell.value == "Content IDs":
            rows[0][0] = first_cell.with_value("IDs")
        return TableData.from_cells(rows)
```

Stage 2:

```python
ColumnGroupExpander(
    key_row="IDs",
    range_rule=NumericRange(".."),
    repeat_rule=PrefixRepeat(":"),
)
```

Schema:

```python
class ContentTable(ColumnTable):
    table_transformer = compose_transformers(
        RenameContentIDs(),
        ColumnGroupExpander(
            key_row="IDs",
            range_rule=NumericRange(".."),
            repeat_rule=PrefixRepeat(":"),
        ),
    )

    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True, parser=content_cells)
```

After stage 1:

```gherkin
| IDs       | 1..2      | 3     |
| Type*     | 2:Article | Poll  |
| Headline* | 2:random  | Vote? |
```

After stage 2:

```gherkin
| IDs       | 1       | 2       | 3     |
| Type*     | Article | Article | Poll  |
| Headline* | random  | random  | Vote? |
```

Then field parsing runs.

If `content_cells` maps `"random"` to generated headlines, the final records
may be:

```python
[
    ContentTable(id="1", content_type="Article", headline="Generated 1"),
    ContentTable(id="2", content_type="Article", headline="Generated 2"),
    ContentTable(id="3", content_type="Poll", headline="Vote?"),
]
```

The source metadata still remembers the compact source:

```python
assert records[0].source_for("headline").source_value == "2:random"
assert records[1].source_for("headline").source_value == "2:random"
```

That is the magic of `TableCell.with_value(...)`.

## 35. Static Feature Checking

Static checking validates `.feature` file tables without running scenarios.

Programmatic:

```python
from bdd_tablex import check_feature


diagnostics = check_feature(
    "users.feature",
    schema=UserTable,
    step="the following users:",
)
```

CLI:

```powershell
bdd-tablex check users.feature `
  --schema tests/support/schemas.py:UserTable `
  --step "the following users:" `
  --format json
```

JSON diagnostics include:

- status,
- matched table count,
- error count,
- error code,
- message,
- hint,
- schema,
- field,
- row,
- column,
- item ID,
- offending value when available.

Use static checking for:

- CI,
- pre-commit,
- editor integration,
- fast feedback before running scenarios.

Nuance: scenario-outline substitutions are not expanded.

## 36. Schema Introspection

Use `describe()` to inspect a schema without parsing a table.

```python
contract = ContentTable.describe()

assert contract.orientation == "column"
assert contract.unknown_fields == "forbid"
```

Convert to a dictionary:

```python
payload = contract.as_dict()
```

The contract includes:

- schema name,
- orientation,
- fields,
- aliases,
- required flags,
- defaults,
- parser names,
- references,
- variants,
- policies,
- transformer name,
- output model,
- output builder.

CLI:

```powershell
bdd-tablex describe tests/support/schemas.py:ContentTable
bdd-tablex describe tests/support/schemas.py:ContentTable --format json
```

Use introspection for:

- docs,
- editor hints,
- review tooling,
- schema discovery,
- explaining table contracts to feature authors.

## 37. Pytest Fixture

The package registers a `bdd_table` fixture.

```python
@given("the following users exist:", target_fixture="users")
def users_exist(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=UserTable)
```

It also supports records:

```python
@given("the following users exist:", target_fixture="users")
def users_exist(datatable, bdd_table):
    return bdd_table.parse_records(datatable, schema=UserTable)
```

The fixture is just a convenience facade. The schema still owns the lifecycle.

## 38. Functional API

Some teams prefer parser functions:

```python
from bdd_tablex import parse_table, parse_table_records


users = parse_table(UserTable, datatable)
records = parse_table_records(UserTable, datatable)
```

These delegate to:

```python
UserTable.parse(datatable)
UserTable.parse_records(datatable)
```

They do not create a separate parsing implementation.

## 39. Common Patterns

### Simple Required Typed Records

```python
class UserTable(RowTable):
    name = field("name", required=True)
    age: int = field("age", required=True)
    active: bool = field("active", default=True)
```

### Evolving Table Vocabulary

```python
class UserTable(RowTable):
    name = field("name", aliases=("full name", "display name"), required=True)
    role = field("role", default="viewer")
```

### Project Token Syntax

```python
cells = CellDSL()


@cells.token("random")
def random_value(context):
    return context.user_data["generator"].value()


class DataTable(RowTable):
    value = field("value", parser=cells)
```

### Compact Content Matrix

```python
class ContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="IDs",
        range_rule=NumericRange(".."),
        repeat_rule=PrefixRepeat(":"),
    )

    id = id_field("IDs")
    kind = field("Type*", required=True)
    headline = field("Headline*", required=True)
```

### Mixed Shapes

```python
class EventTable(RowTable):
    event_type = discriminator_field("type")
    timestamp = field("timestamp", required=True)


@EventTable.variant("click")
class ClickEvent(EventTable):
    selector = field("selector", required=True)


@EventTable.variant("purchase")
class PurchaseEvent(EventTable):
    amount: Decimal = field("amount", required=True)
```

## 40. Common Mistakes

### Expecting `*` To Mean Required

Wrong assumption:

```python
headline = field("Headline*")
```

Correct:

```python
headline = field("Headline*", required=True)
```

### Expecting Defaults To Replace Empty Cells

Input:

```gherkin
| active |
|        |
```

This is not missing. It is explicitly empty.

### Returning Raw Rows From transform_table

Wrong:

```python
return table.to_rows()
```

Correct:

```python
return TableData.from_cells(rows)
```

### Creating Fresh Cells And Losing Source

Usually wrong:

```python
TableCell.from_value("Article", row=1, column=1)
```

Usually correct:

```python
source_cell.with_value("Article")
```

### Forgetting That Override transform_table Takes Control

If you override `transform_table()`, configured `table_transformer` does not run
unless your override calls it.

### Registering Raw Variant Values After Parser Normalization

If the discriminator parser returns lowercase values:

```python
parser=lambda value, context: value.casefold()
```

Register lowercase variant keys:

```python
@ContentTable.variant("article")
```

Not:

```python
@ContentTable.variant("Article")
```

### Using A Transformer For One-Cell Conversion

If one cell becomes one Python value, use a field parser.

If the table shape or labels change, use a transformer.

## 41. How To Decide Which Feature To Use

Use this quick guide:

```text
Need to parse simple rows?                 RowTable
Need many fields per item?                 ColumnTable
Need one cell converted?                   field(parser=...)
Need standard conversion?                  parser helpers or annotations
Need generated symbolic values?            CellDSL
Need several DSLs in priority order?       compose_cell_dsls
Need missing value default?                default or default_factory
Need old labels?                           aliases
Need extra labels tolerated?               unknown_fields
Need mixed record shapes?                  variants
Need record-to-record links?               reference
Need one-record domain rule?               validate_record
Need whole-table domain rule?              validate_records
Need output domain objects?                output_model or build_output
Need compact table structure expanded?     transformer or ColumnGroupExpander
Need several transform stages?             compose_transformers
Need feature file checks before runtime?   check_feature or bdd-tablex check
Need machine-readable schema docs?         describe
```

## 42. The Full Power Example

This combines many features in one realistic content table.

Feature:

```gherkin
| IDs                | 1..2          | 3                    |
| Type*              | 2:Article     | Poll                 |
| Headline*          | 2:random      | Which desk leads?    |
| Category           | Markets       | Politics             |
| Published*         | yes           | no                   |
| Body*              | 2:12:word     |                      |
| Related            | 3             |                      |
| Options*           |               | Equities, Bonds      |
| Closes after hours |               | 24                   |
```

Pieces:

```python
content_cells = CellDSL()


@content_cells.token("random")
def random_content_value(context):
    return context.user_data["generator"].headline(context.item_id)


@content_cells.pattern(r"(?P<count>\d+):word")
def generated_words(match, context):
    return context.user_data["generator"].words(
        int(match["count"]),
        context.item_id,
    )
```

Variant components:

```python
class ArticleFields(TableFields):
    body = field("Body*", required=True, parser=content_cells)
    related = reference("Related", many=True)

    def validate_record(self, context):
        minimum = context.user_data["minimum_article_words"]
        if len(self.body.split()) < minimum:
            raise ValueError("Article body is too short")
        if any(item.content_type != "Poll" for item in self.related):
            raise ValueError("Articles may relate only to Poll records")


class PollFields(TableFields):
    options: list[str] = field("Options*", required=True)
    closes_after_hours: int = field("Closes after hours", default=24)

    def validate_record(self, context):
        if len(self.options) < context.user_data["minimum_poll_options"]:
            raise ValueError("Poll does not have enough options")
```

Schema:

```python
class ContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="IDs",
        range_rule=NumericRange(".."),
        repeat_rule=PrefixRepeat(":"),
    )

    id = id_field("IDs")
    content_type = discriminator(
        "Type*",
        variants={
            "Article": ArticleFields,
            "Poll": PollFields,
        },
    )
    headline = field("Headline*", required=True, parser=content_cells)
    category = field("Category", default="General")
    published: bool = field("Published*", required=True)
```

Parse:

```python
records = ContentTable.parse(
    datatable,
    context={
        "generator": DemoContentGenerator(),
        "minimum_article_words": 10,
        "minimum_poll_options": 2,
    },
)
```

What happens:

1. `1..2` becomes IDs `1` and `2`.
2. `2:Article` becomes two Article type cells.
3. `2:random` becomes two logical `"random"` headline cells.
4. `CellDSL` turns `"random"` into generated headlines.
5. `2:12:word` becomes two logical `"12:word"` cells.
6. `CellDSL` turns `"12:word"` into generated article bodies.
7. The discriminator selects `ArticleFields` or `PollFields`.
8. `published: bool` converts yes/no to booleans.
9. `options: list[str]` converts `"Equities, Bonds"` to a list.
10. `reference("Related", many=True)` resolves Article related IDs to Poll
    records.
11. Variant-specific validators run.
12. Records retain source metadata pointing back to compact cells.

This is the reason the package exists: readable compact BDD tables, but typed
validated Python objects and precise diagnostics.

