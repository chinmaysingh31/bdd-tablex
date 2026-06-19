from pytest_bdd import given, scenario, then

from bdd_tablex import CellDSL, ColumnTable, field, id_field

content_cells = CellDSL()


@content_cells.when(lambda value, context: value.startswith("CMS:"))
def cms_token(value, context):
    return value.removeprefix("CMS:").title()


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True, parser=content_cells)


@scenario("content.feature", "Predicate rules handle project-specific syntax")
def test_predicate_rules():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("predicate CellDSL rules are applied")
def predicate_rules(rows):
    record = ContentTable.parse(rows)[0]

    assert record.headline == "Launch"
