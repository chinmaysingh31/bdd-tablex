from pytest_bdd import given, scenario, then

from bdd_tablex import CellDSL, ColumnTable, field, id_field

content_cells = CellDSL()


@content_cells.token("random")
def random_headline(context):
    return f"Generated headline for {context.item_id}"


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True, parser=content_cells)


@scenario("content.feature", "Exact tokens produce generated values")
def test_exact_tokens():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("exact CellDSL tokens are applied")
def exact_tokens(rows):
    record = ContentTable.parse(rows)[0]

    assert record.headline == "Generated headline for A-1"
