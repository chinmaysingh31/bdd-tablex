import pytest
from pytest_bdd import given, scenario, then
from bdd_tablex import BDDTableError, RowTable, field, id_field


def parse_status(value, context):
    raise ValueError("unsupported status")


class UserTable(RowTable):
    status = field("status", parser=parse_status)
    user_id = id_field("user id")


@scenario("users.feature", "Demonstrate Row ID Diagnostics")
def test_row_id_diagnostics():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the row id diagnostics behavior is correct")
def behavior(rows):
    with pytest.raises(BDDTableError) as captured:
        UserTable.parse(rows)
    assert captured.value.item_id == "U-500"
    assert captured.value.value == "blocked"

