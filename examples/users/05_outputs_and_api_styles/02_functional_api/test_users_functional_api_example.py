from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field, parse_table, parse_table_records


class ExampleTable(RowTable):
    value = field("value")


@scenario("users.feature", "Demonstrate Functional API")
def test_functional_api():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the functional api behavior is correct")
def behavior(rows):
    assert parse_table(ExampleTable, rows)[0].value == "example"
    assert isinstance(parse_table_records(ExampleTable, rows)[0], ExampleTable)
