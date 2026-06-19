from pytest_bdd import given, scenario, then

from bdd_tablex import CellDSL, ColumnTable, field, id_field

status_cells = CellDSL()


@status_cells.fallback
def normalize_status(value, context):
    return value.casefold()


class ContentTable(ColumnTable):
    id = id_field("IDs")
    status = field("Status", parser=status_cells)


@scenario("content.feature", "Fallbacks normalize unmatched values")
def test_fallbacks():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("fallback CellDSL rules are applied")
def fallbacks(rows):
    record = ContentTable.parse(rows)[0]

    assert record.status == "drafted"
