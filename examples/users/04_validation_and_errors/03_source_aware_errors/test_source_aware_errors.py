import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableError, RowTable, field


class UserTable(RowTable):
    email = field("email")

    @classmethod
    def validate_records(cls, records, context):
        raise BDDTableError.from_cell(
            "source aware",
            records[0].source_for("email"),
            schema=cls,
        )


@scenario("users.feature", "Demonstrate Source Aware Errors")
def test_source_aware_errors():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the source aware errors behavior is correct")
def behavior(rows):
    with pytest.raises(BDDTableError) as captured:
        UserTable.parse(rows)
    assert captured.value.row == 2
    assert captured.value.column == 1
