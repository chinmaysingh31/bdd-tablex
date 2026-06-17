from pytest_bdd import given, scenario

from bdd_tablex import ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)
    category = field("Category")


@scenario("content.feature", "Describe content with a column-oriented table")
def test_content():
    pass


@given("the following content exists:", target_fixture="content")
def content_exists(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=ContentTable)
