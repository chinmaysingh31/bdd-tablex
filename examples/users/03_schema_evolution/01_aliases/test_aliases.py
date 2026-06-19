from pytest_bdd import given, scenario, then
from bdd_tablex import RowTable, field


class UserTable(RowTable):
    name = field("name", aliases=("full name",), required=True)


@scenario("users.feature", "Demonstrate Aliases")
def test_aliases():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the aliases behavior is correct")
def behavior(rows):
    assert UserTable.parse(rows)[0].name == "Alice Doe"

