# Cli Check Json

## Purpose

This example teaches **Cli Check Json** in isolation so the learner can see one bdd-tablex behavior without unrelated machinery competing for attention.

Use this pattern when your feature table has the same pressure as this folder: the BDD wording needs to stay readable, while the Python schema owns parsing, validation, source metadata, or output conversion.

The example is executable first and tutorial material second. That means every claim in this page is backed by the adjacent pytest-bdd scenario.

Path: `.\examples\cms\06_tooling\04_cli_check_json`

## Feature Table

```gherkin
Feature: CMS CLI check JSON

  Scenario: Check a CLI-importable schema and render JSON diagnostics
    Given the following statically checked content exists:
      | IDs       | A-1          | A-2 |
      | Headline* | Market brief |     |
      | Status    | draft        |     |
    Then CLI check JSON uses a plain schema module
```

The table is deliberately small unless the folder is the final walkthrough. Small tables make the contract visible: labels live in the feature file, values stay human-readable, and the schema decides how each cell becomes a Python value.

Column-oriented CMS examples use `IDs` as the first row because `ColumnTable` requires exactly one `id_field`. Row-oriented user examples use the first row as headers because `RowTable` creates one record per later row.

Blank cells are meaningful. Depending on the schema they may mean omitted optional value, explicit empty value, rejected required value, or a value that belongs to another variant.

## Schema Walkthrough

```python
from pathlib import Path

from pytest_bdd import given, scenario, then

from bdd_tablex import check_feature
from schemas import ContentTable


@scenario("content.feature", "Check a CLI-importable schema and render JSON diagnostics")
def test_cli_check_json():
    pass


@given("the following statically checked content exists:", target_fixture="feature_path")
def statically_checked_content(datatable):
    return Path(__file__).with_name("content.feature")


@then("CLI check JSON uses a plain schema module")
def cli_check_json(feature_path):
    diagnostics = check_feature(
        feature_path,
        schema=ContentTable,
        step="the following statically checked content exists:",
    )

    assert len(diagnostics) == 1
    assert diagnostics[0].error.field == "Headline*"
    assert diagnostics[0].error.item_id == "A-2"
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
- CLI examples import `schemas.py`, not the pytest test module. This avoids `pytest_bdd` decorator configuration errors outside pytest.

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
pytest examples/cms/06_tooling/04_cli_check_json/test_cli_check_json.py -q
```

Keep changes local to this folder while learning. These examples are intentionally independent, so editing one folder should not force changes in a neighboring folder.

When a change fails, prefer inspecting the structured error object in the test over changing the table until the assertion passes by accident.

The README lives at `examples/cms/06_tooling/04_cli_check_json/README.md`; the executable behavior lives next to it in the feature and test files.

## Previous / Next

Previous: [../03_cli_describe](../03_cli_describe)

Next: [../../../complete/01_complete_cms_walkthrough](../../../complete/01_complete_cms_walkthrough)

