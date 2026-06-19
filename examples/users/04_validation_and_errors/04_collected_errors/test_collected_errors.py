import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableErrors, RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    age: int = field("age")


@scenario("users.feature", "Demonstrate Collected Errors")
def test_collected_errors():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the collected errors behavior is correct")
def behavior(rows):
    with pytest.raises(BDDTableErrors) as captured:
        UserTable.parse(rows, error_mode="collect")
    assert [error.code for error in captured.value.errors] == [
        "empty_required",
        "parser_failed",
    ]
