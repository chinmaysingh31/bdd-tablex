from pytest_bdd import given, scenario, then

from bdd_tablex import CellDSL, ColumnTable, field, id_field


content_cells = CellDSL()


@content_cells.token("random", fields={"headline"})
def random_headline(context):
    return "Generated headline"


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True, parser=content_cells)
    status = field("Status", parser=content_cells)


@scenario("content.feature", "Field scopes keep tokens local to one field")
def test_field_scoped_rules():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("field-scoped CellDSL rules affect only selected fields")
def field_scoped_rules(rows):
    record = ContentTable.parse(rows)[0]

    assert record.headline == "Generated headline"
    assert record.status == "random"
