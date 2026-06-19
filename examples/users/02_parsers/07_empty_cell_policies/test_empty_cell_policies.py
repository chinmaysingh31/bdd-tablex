import pytest
from pytest_bdd import given, scenario, then
from bdd_tablex import BDDTableError, RowTable, field, integer


def parse_blank(value, context):
    return "<blank>" if value == "" else value


class UserTable(RowTable):
    raw_value = field("raw value", parser=integer(), empty="raw")
    parsed_value = field("parsed value", parser=parse_blank, empty="parse")
    none_value = field("none value", empty="none")
    strict_value = field("strict value", empty="error")


@scenario("users.feature", "Demonstrate Empty Cell Policies")
def test_empty_cell_policies():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the empty cell policies behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows)[0]
    assert user.raw_value == ""
    assert user.parsed_value == "<blank>"
    assert user.none_value is None
    with pytest.raises(BDDTableError) as captured:
        UserTable.parse([["strict value"], [""]])
    assert captured.value.code == "empty_optional"

