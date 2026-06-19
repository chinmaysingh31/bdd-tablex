"""Executable dataclass example for converting schema records."""

from dataclasses import dataclass

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field, integer


@dataclass(frozen=True)
class User:
    name: str
    age: int


class UserTable(RowTable):
    output_model = User

    name = field("name", required=True)
    age = field("age", required=True, parser=integer())


@scenario("users.feature", "Return project domain objects from a BDD table")
def test_dataclass_output_models():
    pass


@given("the following modeled users exist:", target_fixture="modeled_users")
def modeled_users(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=UserTable)


@then("the parsed users are dataclass instances")
def users_are_dataclasses(modeled_users):
    assert modeled_users == [
        User(name="Alice", age=30),
        User(name="Bob", age=24),
    ]
