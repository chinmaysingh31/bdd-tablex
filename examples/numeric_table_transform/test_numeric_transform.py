"""Declarative numeric range and prefix-repeat table expansion."""

import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import (
    BDDTableError,
    ColumnGroupExpander,
    ColumnTable,
    NumericRange,
    PrefixRepeat,
    field,
    id_field,
)


class NumericContentTable(ColumnTable):
    """Content schema using reusable numeric and prefix-repeat rules."""

    table_transformer = ColumnGroupExpander(
        key_row="IDs",
        range_rule=NumericRange(separator=".."),
        repeat_rule=PrefixRepeat(separator=":"),
    )

    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)


@scenario(
    "content.feature",
    "Expand numeric ID ranges and repeated values",
)
def test_numeric_table_transformation():
    pass


@given(
    "the following compact numeric content exists:",
    target_fixture="numeric_content",
)
def compact_numeric_content(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=NumericContentTable)


@then("four numeric content records are produced")
def four_numeric_records_are_produced(numeric_content):
    assert [item.id for item in numeric_content] == ["1", "2", "3", "4"]
    assert [item.content_type for item in numeric_content] == [
        "Article",
        "Article",
        "Article",
        "Poll",
    ]
    assert numeric_content[0].headline == "Shared headline"
    assert numeric_content[2].headline == "Shared headline"


def test_repeat_mismatch_points_to_the_original_repeat_cell():
    invalid_table = [
        ["IDs", "1..3"],
        ["Type*", "2:Article"],
        ["Headline*", "Shared headline"],
    ]

    with pytest.raises(BDDTableError, match="does not match") as error:
        NumericContentTable.parse(invalid_table)

    assert error.value.row == 2
    assert error.value.column == 2
    assert error.value.value == "2:Article"
