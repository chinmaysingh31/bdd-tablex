"""Executable example for read-only source metadata on schema records."""

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)


@scenario("users.feature", "Inspect source cells from a parsed record")
def test_record_source_metadata():
    pass


@given("the following traceable users exist:", target_fixture="traceable_users")
def traceable_users(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=UserTable)


@then("each user can identify its original table cells")
def users_identify_source_cells(traceable_users):
    bob = traceable_users[1]
    role_cell = bob.source_for("role")

    assert bob.table_source.row == 3
    assert role_cell.source_row == 3
    assert role_cell.source_column == 2
    assert role_cell.source_value == "editor"
