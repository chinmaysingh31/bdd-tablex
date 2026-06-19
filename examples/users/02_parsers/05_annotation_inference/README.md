# Annotation Inference

## Purpose

This example teaches **Annotation Inference** in isolation so the learner can see one bdd-tablex behavior without unrelated machinery competing for attention.

Use this pattern when your feature table has the same pressure as this folder: the BDD wording needs to stay readable, while the Python schema owns parsing, validation, source metadata, or output conversion.

The example is executable first and tutorial material second. That means every claim in this page is backed by the adjacent pytest-bdd scenario.

Path: `.\examples\users\02_parsers\05_annotation_inference`

## Feature Table

```gherkin
Feature: User focused example

  Scenario: Demonstrate Annotation Inference
    Given the example table:
      | age | ratio | balance | active | status    | tier  | tags     | reviewer | override |
      | 34  | 1.5   | 12.30   | yes    | published | staff | qa, docs |          | many     |
    Then the annotation inference behavior is correct
```

The table is deliberately small unless the folder is the final walkthrough. Small tables make the contract visible: labels live in the feature file, values stay human-readable, and the schema decides how each cell becomes a Python value.

Column-oriented CMS examples use `IDs` as the first row because `ColumnTable` requires exactly one `id_field`. Row-oriented user examples use the first row as headers because `RowTable` creates one record per later row.

Blank cells are meaningful. Depending on the schema they may mean omitted optional value, explicit empty value, rejected required value, or a value that belongs to another variant.

## Schema Walkthrough

```python
from decimal import Decimal
from enum import Enum
from typing import Literal

from pytest_bdd import given, scenario, then
from bdd_tablex import RowTable, field, string


class Status(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class UserTable(RowTable):
    age: int = field("age")
    ratio: float = field("ratio")
    balance: Decimal = field("balance")
    active: bool = field("active")
    status: Status = field("status")
    tier: Literal["basic", "staff"] = field("tier")
    tags: list[str] = field("tags")
    reviewer: int | None = field("reviewer")
    override: int = field("override", parser=string(upper=True))


@scenario("users.feature", "Demonstrate Annotation Inference")
def test_annotation_inference():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the annotation inference behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows)[0]
    assert user.age == 34
    assert user.ratio == 1.5
    assert user.balance == Decimal("12.30")
    assert user.active is True
    assert user.status is Status.PUBLISHED
    assert user.tier == "staff"
    assert user.tags == ["qa", "docs"]
    assert user.reviewer is None
    assert user.override == "MANY"
```

The schema keeps feature-language labels and Python attribute names separate. Labels such as `Headline*` or `default active` are for scenario authors; attributes such as `headline` or `default_active` are for test and application code.

Prefer top-level `bdd_tablex` imports in examples and docs. They show the intended public API and avoid teaching readers private module paths.

If this folder includes a `schemas.py` file, that file is intentionally plain. CLI commands can import it without entering pytest-bdd scenario registration paths.

## Parser / Validation / Output Flow

1. Raw pytest-bdd rows are wrapped as source-aware `TableData` and `TableCell` objects.
2. Any configured table transformer rewrites the logical table while preserving source coordinates.
3. The schema validates labels, aliases, duplicate labels, IDs, and required field presence.
4. Field parsers convert cell text into Python values, using `CellContext` for item ID, field name, source value, and user data.
5. Variants, when present, are selected from the parsed discriminator value.
6. References, when present, resolve after all records are built.
7. `validate_record` and `validate_records` run after parsing and reference resolution.
8. `parse()` may build output objects; `parse_records()` keeps schema record objects for metadata inspection.

## Nuances

- A focused folder should teach one primary concept. Neighboring examples cover nearby ideas.
- Required field failures, parser failures, unknown variants, duplicate IDs, and validation failures all carry structured diagnostics.
- `item_id` is especially useful in column tables and row tables with `id_field`; it makes errors point to the domain record, not only a coordinate.
- `source_for(...)` expects the Python field name, not the feature label.
- Table labels are matched through field labels and aliases; output objects use Python attributes.
- `error_mode="collect"` is useful when a learner or CI job needs all recoverable table problems at once.
- `unknown_fields="ignore"` and `unknown_fields="preserve"` are schema-evolution tools, not substitutes for misspelled required labels.
- Variant-specific fields may appear in a shared table, but non-empty values for the wrong variant depend on inapplicable_fields.
- Custom parsers and DSL handlers should be deterministic in examples so docs remain stable.
- Transformations should use `cell.with_value(...)` to keep diagnostics attached to the source table text.

## What The Assertions Prove

- The adjacent test parses the same table shown in the feature file.
- Assertions check public behavior rather than private helper functions.
- When the example is about diagnostics, the test checks structured fields such as `field`, `item_id`, `row`, `column`, or `code`.
- When the example is about output conversion, the test verifies the actual Python object returned by `parse()`.
- When the example is about source metadata, the test checks preserved source rows, columns, or original values.
- When the example is about CLI or static checking, the test uses the same schema shape the command line should import.

## Try Changing This

- Change one table value and rerun only this example to see the smallest possible feedback loop.
- Rename a feature label, then either update the schema label or add an alias.
- Add one blank cell and decide whether it should be omitted, parsed, converted to `None`, or rejected.
- For diagnostics examples, inspect the full `BDDTableError` object instead of only the message.
- For CMS examples, add a second content item and watch whether the behavior is per-table, per-record, or per-field.

## Previous / Next

Previous: [../04_split_compose_each_optional](../04_split_compose_each_optional)

Next: [../06_custom_parser_context](../06_custom_parser_context)

