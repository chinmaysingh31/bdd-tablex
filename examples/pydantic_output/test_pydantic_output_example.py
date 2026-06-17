"""Executable project example for the optional Pydantic integration."""

from pydantic import BaseModel, Field
from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field


class UserModel(BaseModel):
    name: str
    age: int = Field(ge=18)


class UserTable(RowTable):
    output_model = UserModel

    name: str = field("name", required=True)
    age: int = field("age", required=True)


@scenario("users.feature", "Validate and return Pydantic users")
def test_pydantic_output_model():
    pass


@given("the following Pydantic users exist:", target_fixture="pydantic_users")
def pydantic_users(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=UserTable)


@then("the user is a validated Pydantic model")
def user_is_validated(pydantic_users):
    user = pydantic_users[0]
    assert isinstance(user, UserModel)
    assert user.name == "Alice"
    assert user.age == 30
