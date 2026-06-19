# Empty Cell Policies

## Purpose

This example teaches **Empty Cell Policies** in isolation so the learner can see one bdd-tablex behavior without unrelated machinery competing for attention.

Use this pattern when your feature table has the same pressure as this folder: the BDD wording needs to stay readable, while the Python schema owns parsing, validation, source metadata, or output conversion.

The example is executable first and tutorial material second. That means every claim in this page is backed by the adjacent pytest-bdd scenario.

Path: `.\examples\users\02_parsers\07_empty_cell_policies`

## Feature Table

```gherkin
Feature: User focused example

  Scenario: Demonstrate Empty Cell Policies
    Given the example table:
      | raw value | parsed value | none value | strict value |
      |           |              |            | filled       |
    Then the empty cell policies behavior is correct
```

The table is deliberately small unless the folder is the final walkthrough. Small tables make the contract visible: labels live in the feature file, values stay human-readable, and the schema decides how each cell becomes a Python value.

Column-oriented CMS examples use `IDs` as the first row because `ColumnTable` requires exactly one `id_field`. Row-oriented user examples use the first row as headers because `RowTable` creates one record per later row.

Blank cells are meaningful. Depending on the schema they may mean omitted optional value, explicit empty value, rejected required value, or a value that belongs to another variant.

## Schema Walkthrough

```python
import pytest
from pytest_bdd import given, scenario, then
from bdd_tablex import BDDTableError, RowTable, field, integer


def parse_blank(value, context):
    return "<blank>" if value == "" else value


class UserTable(RowTable):
    raw_value = field("raw value", parser=integer(), empty="raw")
    parsed_value = field("parsed value", parser=parse_blank, empty="parse")
    none_value = field("none value", empty="none")
    strict_value = field("strict value", empty="error")


@scenario("users.feature", "Demonstrate Empty Cell Policies")
def test_empty_cell_policies():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the empty cell policies behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows)[0]
    assert user.raw_value == ""
    assert user.parsed_value == "<blank>"
    assert user.none_value is None
    with pytest.raises(BDDTableError) as captured:
        UserTable.parse([["strict value"], [""]])
    assert captured.value.code == "empty_optional"
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
- `empty="raw"` preserves the historical default for optional blank cells.
- `empty="parse"` sends the blank string to the parser.
- `empty="none"` converts an explicit blank cell to `None`.
- `empty="error"` rejects explicit blanks even for optional fields.

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

## How To Read And Run This

Read the feature file first, then the schema class, then the assertions. That order mirrors how a feature author experiences the package: they write a table, the schema gives the table meaning, and the assertions prove the resulting behavior.

Run this example on its own while experimenting:

```powershell
pytest examples/users/02_parsers/07_empty_cell_policies/test_empty_cell_policies.py -q
```

Keep changes local to this folder while learning. These examples are intentionally independent, so editing one folder should not force changes in a neighboring folder.

When a change fails, prefer inspecting the structured error object in the test over changing the table until the assertion passes by accident.

The README lives at `examples/users/02_parsers/07_empty_cell_policies/README.md`; the executable behavior lives next to it in the feature and test files.

## Previous / Next

Previous: [../06_custom_parser_context](../06_custom_parser_context)

Next: [../../03_schema_evolution/01_aliases](../../03_schema_evolution/01_aliases)

