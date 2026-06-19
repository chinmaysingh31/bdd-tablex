from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)
    status = field("Status")


@scenario("content.feature", "Parse a basic CMS column table")
def test_basic_column_table():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the column table records are parsed by item column")
def parsed_by_item_column(rows):
    article, poll = ContentTable.parse(rows)

    assert article.id == "A-1"
    assert article.content_type == "Article"
    assert article.headline == "Market brief"
    assert poll.id == "P-1"
    assert poll.status == "published"
