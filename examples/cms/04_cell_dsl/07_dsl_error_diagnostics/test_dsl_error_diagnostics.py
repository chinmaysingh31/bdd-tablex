import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableError, CellDSL, ColumnTable, field, id_field

content_cells = CellDSL()


@content_cells.token("broken")
def broken_value(context):
    raise RuntimeError("generator unavailable")


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True, parser=content_cells)


@scenario("content.feature", "DSL handler errors keep source diagnostics")
def test_dsl_error_diagnostics():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("DSL errors report the original cell")
def dsl_error_diagnostics(rows):
    with pytest.raises(BDDTableError) as error:
        ContentTable.parse(rows)

    assert "generator unavailable" in str(error.value)
    assert error.value.field == "Headline*"
    assert error.value.item_id == "A-1"
    assert error.value.row == 2
    assert error.value.column == 2
