from pytest_bdd import given, scenario, then

from bdd_tablex import AlphabeticRange, ColumnGroupExpander, ColumnTable, PrefixRepeat, field, id_field


class ContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="IDs",
        range_rule=AlphabeticRange("-"),
        repeat_rule=PrefixRepeat(":"),
    )

    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)


@scenario("content.feature", "Alphabetic ranges expand grouped content columns")
def test_alphabetic_group_expansion():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("alphabetic group expansion creates one record per ID")
def alphabetic_group_expansion(rows):
    records = ContentTable.parse(rows)

    assert [record.id for record in records] == ["A", "B", "C"]
    assert records[2].headline == "Shared"
