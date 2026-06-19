import pytest
from pytest_bdd import given, scenario, then
from bdd_tablex import RowTable, boolean, field


class UserTable(RowTable):
    default_active = field("default active", parser=boolean())
    lifecycle_active = field(
        "lifecycle active",
        parser=boolean(
            true_values=("enabled", "active", "y"),
            false_values=("disabled", "inactive", "n"),
        ),
    )
    strict_active = field(
        "strict active",
        parser=boolean(
            true_values=("YES",),
            false_values=("NO",),
            case_sensitive=True,
        ),
    )


@scenario("users.feature", "Demonstrate Boolean Custom Vocabulary")
def test_boolean_custom_vocabulary():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the boolean custom vocabulary behavior is correct")
def behavior(rows):
    enabled, disabled = UserTable.parse(rows)
    assert enabled.default_active is True
    assert enabled.lifecycle_active is True
    assert enabled.strict_active is True
    assert disabled.default_active is False
    assert disabled.lifecycle_active is False
    assert disabled.strict_active is False
    with pytest.raises(ValueError, match="overlap"):
        boolean(true_values=("yes",), false_values=("YES",))

