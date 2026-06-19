from dataclasses import dataclass

from pytest_bdd import given, scenario, then
from bdd_tablex import RowTable, field


@dataclass(frozen=True)
class User:
    username: str
    age: int


class UserTable(RowTable):
    output_model = User
    username = field("username")
    age: int = field("age")


@scenario("users.feature", "Demonstrate Dataclass Output")
def test_dataclass_output():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the dataclass output behavior is correct")
def behavior(rows):
    assert UserTable.parse(rows) == [User("alice", 34)]

