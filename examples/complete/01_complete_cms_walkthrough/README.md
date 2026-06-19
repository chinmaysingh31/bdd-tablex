# Complete Cms Walkthrough

## Purpose

This example teaches **Complete Cms Walkthrough** in isolation so the learner can see one bdd-tablex behavior without unrelated machinery competing for attention.

Use this pattern when your feature table has the same pressure as this folder: the BDD wording needs to stay readable, while the Python schema owns parsing, validation, source metadata, or output conversion.

The example is executable first and tutorial material second. That means every claim in this page is backed by the adjacent pytest-bdd scenario.

Path: `.\examples\complete\01_complete_cms_walkthrough`

## Feature Table

```gherkin
Feature: Complete CMS walkthrough

  Scenario: Parse a compact mixed-content table
    Given the following complete content table:
      | IDs                | 1..2          | 3                    |
      | Type*              | 2:Article     | Poll                 |
      | Headline*          | 2:random      | Which desk leads?    |
      | Category           | Markets       | Politics             |
      | Published*         | yes           | no                   |
      | Body*              | 2:12:word     |                      |
      | Related            | 3             |                      |
      | Options*           |               | Equities, Bonds      |
      | Closes after hours |               | 24                   |
    Then the complete content records are typed and linked

  Scenario: Convert each content variant to its own output model
    Given the following publish commands:
      | IDs       | A             | P              |
      | Type*     | Article       | Poll           |
      | Headline* | Morning brief | Choose a desk? |
      | Body*     | Full text     |                |
      | Options*  |               | News, Markets  |
    Then each publish command uses its variant output model
```

The table is deliberately small unless the folder is the final walkthrough. Small tables make the contract visible: labels live in the feature file, values stay human-readable, and the schema decides how each cell becomes a Python value.

Column-oriented CMS examples use `IDs` as the first row because `ColumnTable` requires exactly one `id_field`. Row-oriented user examples use the first row as headers because `RowTable` creates one record per later row.

Blank cells are meaningful. Depending on the schema they may mean omitted optional value, explicit empty value, rejected required value, or a value that belongs to another variant.

## Schema Walkthrough

```python
from dataclasses import dataclass

from pytest_bdd import given, scenario, then

from bdd_tablex import (
    CellDSL,
    ColumnGroupExpander,
    ColumnTable,
    NumericRange,
    PrefixRepeat,
    TableFields,
    boolean,
    discriminator,
    field,
    id_field,
    reference,
)


class DemoContentGenerator:
    def headline(self, item_id):
        return f"Generated headline {item_id}"

    def words(self, count, item_id):
        return " ".join(f"item{item_id}-word{number}" for number in range(1, count + 1))


content_cells = CellDSL()


@content_cells.token("random")
def random_content_value(context):
    return context.user_data["generator"].headline(context.item_id)


@content_cells.pattern(r"(?P<count>\d+):word")
def generated_words(match, context):
    return context.user_data["generator"].words(int(match["count"]), context.item_id)


class ArticleFields(TableFields):
    body = field("Body*", required=True, parser=content_cells)
    related = reference("Related", many=True)

    def validate_record(self, context):
        minimum = context.user_data["minimum_article_words"]
        if len(self.body.split()) < minimum:
            raise ValueError(f"Article body must contain at least {minimum} words")
        if any(item.content_type != "Poll" for item in self.related):
            raise ValueError("Articles may relate only to Poll records")


class PollFields(TableFields):
    options: list[str] = field("Options*", required=True)
    closes_after_hours: int = field("Closes after hours", default=24)

    def validate_record(self, context):
        if len(self.options) < context.user_data["minimum_poll_options"]:
            raise ValueError("Poll does not have enough options")


class ContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="IDs",
        range_rule=NumericRange(separator=".."),
        repeat_rule=PrefixRepeat(separator=":"),
    )

    id = id_field("IDs")
    content_type = discriminator(
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

## Walkthrough Notes

This final example is intentionally broad. Unlike the focused folders, it shows several moving parts cooperating in the same table:

- grouped IDs become separate content records before schema parsing begins.
- repeat syntax expands shared values while preserving original source cells.
- the discriminator selects Article or Poll fields per item.
- CellDSL tokens and regex patterns generate deterministic content from context.
- boolean parsing turns yes and 
o into Python booleans.
- references resolve after all records exist, so articles can point at polls.
- variant validators run after references, which lets policies inspect linked records.
- defaults fill omitted optional values such as Closes after hours.
- source metadata remains available even after grouped-column expansion.
- variant output models let a second schema return different dataclasses from one table.

When adapting this example for a real project, resist starting here. Build the narrow examples first, then combine only the pieces your domain actually needs. The broad walkthrough is useful as a confidence check and as future docs material, but the smaller folders are better starting templates for production tests.

A good extension exercise is to add a Video variant with a required URL and then decide whether article references may point to videos. That forces you to touch the discriminator mapping, a variant field group, validation, and assertions without changing the package internals.
## Adaptation Checklist

Before adapting the complete walkthrough into project docs, decide which parts should remain in the broad example and which parts deserve their own focused page.

Keep these pieces in the walkthrough:

- one compact grouped column table.
- one mixed variant schema.
- one deterministic DSL token or pattern.
- one reference relationship.
- one validation rule that depends on parsed values.
- one source metadata assertion.
- one output model scenario.

Move these pieces out if they grow:

- multiple generators or fixture services.
- several unrelated validation policies.
- more than one custom transformer convention.
- external databases, HTTP calls, or time-sensitive values.
- long business vocabulary that hides the tablex behavior.

The best docs version should feel like a capstone. A learner who has read the focused examples should recognize every ingredient and mainly learn how the lifecycle composes them.

Final docs note: keep this page as the capstone, not the first tutorial. It should reward readers who already understand the focused folders.
Use the focused examples as source links for each ingredient.
Keep broad business commentary out of this page unless it explains parser lifecycle.

## Previous / Next

Previous: [../../cms/06_tooling/04_cli_check_json](../../cms/06_tooling/04_cli_check_json)

Next: [../../README.md](../../README.md)

