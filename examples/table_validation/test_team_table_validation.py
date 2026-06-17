"""Executable team example for validation across all records."""

import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableError, RowTable, boolean, field


class TeamUserTable(RowTable):
    email = field("email", required=True)
    primary = field("primary", required=True, parser=boolean())

    @classmethod
    def validate_records(cls, records, context):
        """Require unique emails and exactly one primary user."""

        by_email = {}
        for record in records:
            if record.email in by_email:
                raise BDDTableError.from_cell(
                    "Email must be unique",
                    record.source_for("email"),
                    schema=cls,
                )
            by_email[record.email] = record

        primary_users = [record for record in records if record.primary]
        if len(primary_users) != 1:
            raise ValueError("Exactly one primary user is required")


@scenario("users.feature", "Validate relationships across several users")
def test_whole_table_validation():
    pass


@given("the following team users exist:", target_fixture="team_users")
def team_users(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=TeamUserTable)


@then("the complete user table is valid")
def complete_table_is_valid(team_users):
    assert len(team_users) == 2
    assert sum(user.primary for user in team_users) == 1


def test_duplicate_email_points_to_the_second_email_cell():
    with pytest.raises(BDDTableError, match="Email must be unique") as error:
        TeamUserTable.parse(
            [
                ["email", "primary"],
                ["same@example.com", "yes"],
                ["same@example.com", "no"],
            ]
        )

    assert error.value.row == 3
    assert error.value.column == 1
