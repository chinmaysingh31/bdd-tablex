from pytest_bdd import given, scenario, then
from bdd_tablex import RowTable, field, id_field


seen = []


def parse_display(value, context):
    seen.append(context.item_id)
    return value.lower()


def default_audit(context):
    return f"audit-{context.item_id}"


class UserTable(RowTable):
    display_name = field("display name", parser=parse_display)
    user_id = id_field("user id")
    audit_name = field("audit name", default_factory=default_audit)


@scenario("users.feature", "Demonstrate Row ID Field Context")
def test_row_id_field_context():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the row id field context behavior is correct")
def behavior(rows):
    seen.clear()
    user = UserTable.parse_records(rows)[0]
    assert seen == ["U-100"]
    assert user.audit_name == "audit-U-100"
    assert user.table_source.item_id == "U-100"

