from decimal import Decimal

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, decimal, field, floating, integer, string


class UserTable(RowTable):
    username = field("username", parser=string(strip=True, lower=True))
    age = field("age", parser=integer())
    mask = field("mask", parser=integer(base=16))
    rating = field("rating", parser=floating())
    balance = field("balance", parser=decimal())


@scenario("users.feature", "Demonstrate Scalar Parsers")
def test_scalar_parsers():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the scalar parsers behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows)[0]
    assert user.username == "alice"
    assert user.mask == 255
    assert user.balance == Decimal("12.30")
