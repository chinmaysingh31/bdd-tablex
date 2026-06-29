from pytest_bdd import given, scenario, then

from talika import RowTable, boolean, field, split


class UserTable(RowTable):
    name = field("name", required=True)
    age: int = field("age")
    roles = field("roles", parser=split(","))
    active = field("active", parser=boolean(), default=True)





@scenario("users.feature", "Demonstrate Split Compose Each Optional")
def test_split_compose_each_optional():
    pass


@given("The following users are present", target_fixture="rows")
def example_table(datatable):
    users = UserTable.parse(datatable)
    return datatable


# @then("the split compose each optional behavior is correct")
# def behavior(rows):
#     user = UserTable.parse(rows)[0]
#     assert user.tags == ["qa", "docs"]
#     assert user.scores == [1, 2, 3]
#     assert user.reviewer is None
