import pytest
from pytest_bdd import given, scenario, then
from bdd_tablex import BDDTableError, RowTable, field


class UserTable(RowTable):
    role = field("role")

    def validate_record(self, context):
        if self.role not in {"admin", "editor"}:
            raise ValueError("unsupported role")


@scenario("users.feature", "Demonstrate Record Validation")
def test_record_validation():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the record validation behavior is correct")
def behavior(rows):
    assert UserTable.parse(rows)[0].role == "admin"
    with pytest.raises(BDDTableError):
        UserTable.parse([["role"], ["owner"]])

