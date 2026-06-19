"""Executable example for fail-fast and collect-all parsing modes."""

from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableErrors, RowTable, field


class UserTable(RowTable):
    """A small schema with two independent ways for each row to fail."""

    name = field("name", required=True)
    age: int = field("age")


@scenario("users.feature", "Report every independent invalid user cell")
def test_collected_table_errors():
    pass


@given("the following invalid users are checked:", target_fixture="table_errors")
def invalid_users_are_checked(datatable, bdd_table):
    """Catch the aggregate as application code or a custom reporter might."""

    try:
        bdd_table.parse(datatable, schema=UserTable, error_mode="collect")
    except BDDTableErrors as errors:
        return errors
    raise AssertionError("The example table should be invalid")


@then("four source-aware errors are reported together")
def four_errors_are_reported(table_errors):
    assert len(table_errors) == 4
    assert [error.code for error in table_errors] == [
        "empty_required",
        "parser_failed",
        "empty_required",
        "parser_failed",
    ]
    assert [(error.row, error.column) for error in table_errors] == [
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
    ]
