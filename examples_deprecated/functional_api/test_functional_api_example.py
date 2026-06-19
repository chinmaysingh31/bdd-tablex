"""Three equivalent ways to parse the same BDD table schema."""

from pytest_bdd import given, scenario

from bdd_tablex import RowTable, field, parse_table, parse_table_records


def parse_bool(value, context):
    """Parse the small boolean convention used in this example table."""
    return value.lower() == "true"


class UserTable(RowTable):
    """A normal row-oriented schema used by all three API styles."""

    name = field("name", required=True)
    role = field("role", required=True)
    active = field("active", parser=parse_bool)


DATATABLE = [
    ["name", "role", "active"],
    ["Alice", "admin", "true"],
    ["Bob", "user", "false"],
]


def test_primary_schema_method_style():
    """Use the primary API when the schema is the natural entry point."""
    users = UserTable.parse(DATATABLE)

    assert users[0].name == "Alice"
    assert users[0].active is True
    assert users[1].active is False


def test_functional_parser_style():
    """Use the functional API when explicit parser calls read better."""
    users = parse_table(UserTable, DATATABLE)
    records = parse_table_records(UserTable, DATATABLE)

    assert users == records
    assert isinstance(records[0], UserTable)
    assert records[1].role == "user"


@scenario("users.feature", "Create users with the pytest fixture style")
def test_pytest_fixture_style():
    """Use the pytest fixture style inside pytest-bdd step definitions."""


@given("the following functional API users:", target_fixture="users")
def users_exist(datatable, bdd_table):
    """Parse via the fixture when pytest dependency injection is convenient."""
    return bdd_table.parse(datatable, schema=UserTable)
