import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field

pydantic = pytest.importorskip("pydantic")


class UserModel(pydantic.BaseModel):
    username: str
    age: int = pydantic.Field(ge=18)


class UserTable(RowTable):
    output_model = UserModel
    username = field("username")
    age: int = field("age")


@scenario("users.feature", "Demonstrate Pydantic Output")
def test_pydantic_output():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the pydantic output behavior is correct")
def behavior(rows):
    assert UserTable.parse(rows) == [UserModel(username="alice", age=34)]
