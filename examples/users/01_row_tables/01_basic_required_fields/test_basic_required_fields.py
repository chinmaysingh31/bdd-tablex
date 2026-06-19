from pytest_bdd import given, scenario, then
from bdd_tablex import RowTable, boolean, field


class UserTable(RowTable):
    username = field("username", required=True)
    email = field("email", required=True)
    active = field("active", parser=boolean(), required=True)


@scenario("users.feature", "Demonstrate Basic Required Fields")
def test_basic_required_fields():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the basic required fields behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows)[0]
    assert user.username == "alice"
    assert user.active is True

