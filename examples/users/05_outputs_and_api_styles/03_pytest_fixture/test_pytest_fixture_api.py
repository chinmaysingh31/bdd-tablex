from pytest_bdd import given, scenario, then
from bdd_tablex import RowTable, field


class ExampleTable(RowTable):
    value = field("value")


@scenario("users.feature", "Demonstrate Pytest Fixture API")
def test_pytest_fixture_api():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the pytest fixture behavior is correct")
def behavior(rows, bdd_table):
    assert bdd_table.parse(rows, schema=ExampleTable)[0].value == "example"

