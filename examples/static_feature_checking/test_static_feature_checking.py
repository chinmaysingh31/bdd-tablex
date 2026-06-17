"""Executable API example for static Gherkin table validation."""

from bdd_tablex import check_feature

from .schemas import CheckedUserTable


def test_invalid_feature_table_is_reported_without_scenario_execution():
    diagnostics = check_feature(
        "examples/static_feature_checking/invalid_users.feature",
        schema=CheckedUserTable,
        step="the following statically checked users:",
    )

    assert [diagnostic.error.code for diagnostic in diagnostics] == [
        "empty_required",
        "parser_failed",
    ]
    assert all(diagnostic.error.row == 6 for diagnostic in diagnostics)
