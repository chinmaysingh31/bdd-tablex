from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, compose, each, field, integer, optional, split


class UserTable(RowTable):
    tags = field("tags", parser=split(","))
    scores = field("scores", parser=compose(split(";"), each(integer())))
    reviewer = field("reviewer", parser=optional(integer(), none_values=("none",)))


@scenario("users.feature", "Demonstrate Split Compose Each Optional")
def test_split_compose_each_optional():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the split compose each optional behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows)[0]
    assert user.tags == ["qa", "docs"]
    assert user.scores == [1, 2, 3]
    assert user.reviewer is None
