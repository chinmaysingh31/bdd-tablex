from bdd_tablex import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)


def test_bdd_table_fixture_parses_with_schema(bdd_table):
    users = bdd_table.parse([["name"], ["Alice"]], schema=UserTable)

    assert users[0].name == "Alice"


def test_bdd_table_fixture_can_return_schema_records(bdd_table):
    users = bdd_table.parse_records([["name"], ["Alice"]], schema=UserTable)

    assert isinstance(users[0], UserTable)
    assert users[0].name == "Alice"
