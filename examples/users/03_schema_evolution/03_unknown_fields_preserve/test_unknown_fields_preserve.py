from pytest_bdd import given, scenario, then
from bdd_tablex import RowTable, field


class UserTable(RowTable):
    unknown_fields = "preserve"
    username = field("username")


@scenario("users.feature", "Demonstrate Unknown Fields Preserve")
def test_unknown_fields_preserve():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the unknown fields preserve behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows)[0]
    assert user.username == "alice"
    assert user.table_extras == {"team": "Platform"}

