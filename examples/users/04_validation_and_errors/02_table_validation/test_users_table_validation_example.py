import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableError, RowTable, field


class UserTable(RowTable):
    email = field("email")

    @classmethod
    def validate_records(cls, records, context):
        if len({record.email for record in records}) != len(records):
            raise ValueError("duplicate email")


@scenario("users.feature", "Demonstrate Table Validation")
def test_table_validation():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the table validation behavior is correct")
def behavior(rows):
    assert len(UserTable.parse(rows)) == 2
    with pytest.raises(BDDTableError):
        UserTable.parse([["email"], ["a@example.com"], ["a@example.com"]])
