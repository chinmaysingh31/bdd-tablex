"""Custom rule objects plugged into the reusable column group expander."""

import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import (
    BDDTableError,
    ColumnGroupExpander,
    ColumnTable,
    field,
    id_field,
)


class ReferenceRange:
    """Expand project references such as ``R1~R3``.

    This class implements the small ``RangeRule`` contract by exposing an
    ``expand(cell, context)`` method that returns source-aware cells.
    """

    def expand(self, cell, context):
        """Return one literal reference or an inclusive reference sequence."""

        if "~" not in cell.value:
            return [cell]

        start_text, separator, end_text = cell.value.partition("~")
        if (
            not separator
            or not start_text.startswith("R")
            or not end_text.startswith("R")
        ):
            raise ValueError("Invalid reference range")

        try:
            start = int(start_text[1:])
            end = int(end_text[1:])
        except ValueError as exc:
            raise ValueError("Invalid reference range") from exc

        if start > end:
            raise ValueError("Reference range must be ascending")

        return [cell.with_value(f"R{number}") for number in range(start, end + 1)]


class BracketRepeat:
    """Expand count-in-brackets syntax such as ``[3]Article``."""

    def expand(self, cell, expected_count, context):
        """Repeat bracket syntax or copy a normal cell across its group."""

        if not cell.value.startswith("[") or "]" not in cell.value:
            return [cell] * expected_count

        count_text, value = cell.value[1:].split("]", maxsplit=1)
        if not count_text.isdigit() or not value:
            raise ValueError("Invalid bracket repeat")

        declared_count = int(count_text)
        if declared_count != expected_count:
            raise ValueError(
                f"Repeat count {declared_count} does not match "
                f"group size {expected_count}"
            )

        return [cell.with_value(value) for _ in range(declared_count)]


class ReferenceContentTable(ColumnTable):
    """Schema combining reusable mechanics with fully custom syntax rules."""

    table_transformer = ColumnGroupExpander(
        key_row="References",
        range_rule=ReferenceRange(),
        repeat_rule=BracketRepeat(),
    )

    reference = id_field("References")
    kind = field("Kind*", required=True)
    headline = field("Headline*", required=True)


@scenario(
    "content.feature",
    "Use project-defined range and repeat grammar",
)
def test_custom_group_rule_scenario():
    pass


@given(
    "the following bracket-style content exists:",
    target_fixture="reference_content",
)
def bracket_style_content(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=ReferenceContentTable)


@then("four custom-reference records are produced")
def four_reference_records_are_produced(reference_content):
    assert [item.reference for item in reference_content] == [
        "R1",
        "R2",
        "R3",
        "R4",
    ]
    assert [item.kind for item in reference_content] == [
        "Article",
        "Article",
        "Article",
        "Poll",
    ]


def test_custom_rule_error_is_wrapped_with_source_location():
    invalid_table = [
        ["References", "R3~R1"],
        ["Kind*", "[3]Article"],
        ["Headline*", "Regional news"],
    ]

    with pytest.raises(BDDTableError, match="must be ascending") as error:
        ReferenceContentTable.parse(invalid_table)

    assert error.value.row == 1
    assert error.value.column == 2
    assert error.value.value == "R3~R1"
