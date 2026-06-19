from dataclasses import dataclass

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field


@dataclass(frozen=True)
class Value:
    value: str


class ExampleTable(RowTable):
    output_model = Value
    value = field("value")


@scenario("users.feature", "Demonstrate Parse vs Parse Records")
def test_parse_vs_parse_records():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the parse vs parse records behavior is correct")
def behavior(rows):
    assert ExampleTable.parse(rows) == [Value("example")]
    assert isinstance(ExampleTable.parse_records(rows)[0], ExampleTable)
