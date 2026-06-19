"""Declarative alphabetic range and suffix-repeat table expansion."""

import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import (
    AlphabeticRange,
    BDDTableError,
    ColumnGroupExpander,
    ColumnTable,
    SuffixRepeat,
    field,
    id_field,
)


class AlphabeticContentTable(ColumnTable):
    """A table schema using reusable alphabetic and suffix-repeat rules."""

    table_transformer = ColumnGroupExpander(
        key_row="Keys",
        range_rule=AlphabeticRange(separator="-"),
        repeat_rule=SuffixRepeat(separator=" x"),
    )

    key = id_field("Keys")
    kind = field("Kind*", required=True)
    headline = field("Headline*", required=True)


@scenario(
    "content.feature",
    "Expand alphabetic keys and x-style repeated values",
)
def test_alphabetic_table_transformation():
    pass


@given(
    "the following compact alphabetic content exists:",
    target_fixture="alphabetic_content",
)
def compact_alphabetic_content(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=AlphabeticContentTable)


@then("four alphabetic content records are produced")
def four_alphabetic_records_are_produced(alphabetic_content):
    assert [item.key for item in alphabetic_content] == ["A", "B", "C", "D"]
    assert [item.kind for item in alphabetic_content] == [
        "Article",
        "Article",
        "Article",
        "Poll",
    ]


def test_invalid_key_range_reports_the_original_cell():
    invalid_table = [
        ["Keys", "C-A"],
        ["Kind*", "Article x3"],
        ["Headline*", "Regional news"],
    ]

    with pytest.raises(BDDTableError, match="must be ascending") as error:
        AlphabeticContentTable.parse(invalid_table)

    assert error.value.row == 1
    assert error.value.column == 2
    assert error.value.value == "C-A"
