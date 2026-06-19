from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, choice, field, map_value


class UserTable(RowTable):
    role = field("role", parser=choice("admin", "editor", case_sensitive=False))
    priority = field("priority", parser=map_value({"low": 1, "high": 5}))


@scenario("users.feature", "Demonstrate Choice and Mapping Parsers")
def test_choice_and_mapping_parsers():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the choice and mapping behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows)[0]
    assert user.role == "admin"
    assert user.priority == 5
