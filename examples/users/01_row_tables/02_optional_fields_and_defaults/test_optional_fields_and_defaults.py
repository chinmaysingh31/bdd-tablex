from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field


def default_team(context):
    return context.user_data["team"]


class UserTable(RowTable):
    username = field("username", required=True)
    role = field("role", default="viewer")
    team = field("team", default_factory=default_team)


@scenario("users.feature", "Demonstrate Optional Fields and Defaults")
def test_optional_fields_and_defaults():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the optional fields and defaults behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows, context={"team": "platform"})[0]
    assert user.role == "viewer"
    assert user.team == "platform"
