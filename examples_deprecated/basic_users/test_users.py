from pytest_bdd import given, scenario

from bdd_tablex import RowTable, field


def parse_bool(value, context):
    return value.lower() == "true"


class UserTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)
    active = field("active", parser=parse_bool)


@scenario("users.feature", "Create users from a row-oriented table")
def test_users():
    pass


@given("the following users exist:", target_fixture="users")
def users_exist(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=UserTable)
