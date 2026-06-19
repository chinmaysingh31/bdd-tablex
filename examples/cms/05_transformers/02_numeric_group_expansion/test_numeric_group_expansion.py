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
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)


@scenario("content.feature", "Numeric ranges expand grouped content columns")
def test_numeric_group_expansion():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("numeric group expansion creates one record per ID")
def numeric_group_expansion(rows):
    records = ContentTable.parse(rows)

    assert [record.id for record in records] == ["1", "2", "3"]
    assert [record.content_type for record in records] == ["Article"] * 3
    assert records[1].source_for("content_type").source_value == "3:Article"
