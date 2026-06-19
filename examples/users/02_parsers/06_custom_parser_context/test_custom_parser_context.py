from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field, id_field

seen = {}


def parse_username(value, context):
    seen.update(
        field_name=context.field_name,
        field_label=context.field_label,
        item_id=context.item_id,
        source_value=context.source_value,
    )
    return f"{context.user_data['prefix']}-{context.item_id}-{value}"


class UserTable(RowTable):
    user_id = id_field("user id")
    username = field("username", parser=parse_username)


@scenario("users.feature", "Demonstrate Custom Parser Context")
def test_custom_parser_context():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the custom parser context behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows, context={"prefix": "import"})[0]
    assert user.username == "import-U-1-alice"
    assert seen == {
        "field_name": "username",
        "field_label": "username",
        "item_id": "U-1",
        "source_value": "alice",
    }
