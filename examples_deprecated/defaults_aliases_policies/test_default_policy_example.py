"""Executable example for defaults, aliases, and unknown-field policy."""

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field


class UserTable(RowTable):
    """A schema that accepts historical labels and preserves project extras."""

    unknown_fields = "preserve"

    name = field("name", aliases=("full name",), required=True)
    role = field(
        "role",
        default_factory=lambda context: context.user_data["default_role"],
    )
    tags: list[str] = field(
        "tags",
        default_factory=lambda context: [],
    )


@scenario(
    "users.feature",
    "Evolve a table contract without breaking older wording",
)
def test_defaults_aliases_and_policies():
    pass


@given("the following flexible users:", target_fixture="flexible_users")
def flexible_users(datatable, bdd_table):
    """Parse with project data used only when an optional field is missing."""

    return bdd_table.parse(
        datatable,
        schema=UserTable,
        context={"default_role": "reader"},
    )


@then("missing values are generated and additional values are preserved")
def generated_defaults_and_preserved_extras(flexible_users):
    user = flexible_users[0]

    assert user.name == "Alice"
    assert user.role == "reader"
    assert user.tags == []
    assert user.table_extras == {"team": "Publishing"}
