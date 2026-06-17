"""Executable pytest-bdd example for the source-aware table model."""

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, TableData, field


class UserTable(RowTable):
    """A normal schema that can parse either raw rows or TableData."""

    name = field("name", required=True)
    status = field("status", required=True)


@scenario(
    "source_locations.feature",
    "Inspect original BDD table cell locations",
)
def test_source_aware_table_data():
    pass


@given(
    "the following source-aware users exist:",
    target_fixture="source_aware_users",
)
def source_aware_users(datatable):
    """Wrap pytest-bdd rows explicitly so this example can inspect cells."""

    table = TableData.from_rows(datatable)
    users = UserTable.parse(table)
    return table, users


@then("the table retains its original values and locations")
def original_locations_are_available(source_aware_users):
    table, users = source_aware_users
    disabled = table.cell(row=3, column=2)

    assert disabled.value == "disabled"
    assert disabled.source_value == "disabled"
    assert disabled.source_row == 3
    assert disabled.source_column == 2
    assert [user.name for user in users] == ["Alice", "Bob"]
