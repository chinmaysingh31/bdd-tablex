from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)
    status = field("Status")


@scenario("content.feature", "Parse content when an optional row is absent")
def test_missing_optional_rows():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("missing optional rows become None")
def missing_optional_rows(rows):
    records = ContentTable.parse(rows)

    assert [record.status for record in records] == [None, None]
    assert [record.headline for record in records] == [
        "Market brief",
        "Reader question",
    ]
