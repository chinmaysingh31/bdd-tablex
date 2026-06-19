from pytest_bdd import given, scenario, then

from bdd_tablex import (
    ColumnGroupExpander,
    ColumnTable,
    NumericRange,
    PrefixRepeat,
    field,
    id_field,
)


class ContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="IDs",
        range_rule=NumericRange(".."),
        repeat_rule=PrefixRepeat(":"),
    )

    id = id_field("IDs")
    headline = field("Headline*", required=True)


@scenario("content.feature", "Expanded grouped columns preserve original source cells")
def test_transformed_source_metadata():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("transformed records still point at compact source cells")
def transformed_source_metadata(rows):
    first, second = ContentTable.parse_records(rows)

    assert [first.id, second.id] == ["1", "2"]
    assert first.headline == "Shared"
    assert second.source_for("headline").source_value == "2:Shared"
    assert second.source_for("headline").source_column == 2
