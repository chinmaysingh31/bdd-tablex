from pytest_bdd import given, scenario, then
from bdd_tablex import RowTable, field


class UserTable(RowTable):
    unknown_fields = "ignore"
    username = field("username")


@scenario("users.feature", "Demonstrate Unknown Fields Ignore")
def test_unknown_fields_ignore():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the unknown fields ignore behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows)[0]
    assert user.username == "alice"
    assert user.table_extras == {}

