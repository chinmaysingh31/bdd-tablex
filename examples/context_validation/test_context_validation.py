import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableError, RowTable, field

ACCESS_POLICY = {
    "admin": {"global"},
    "editor": {"eu", "us"},
}


class UserAccessTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)
    region = field("region", required=True)

    def validate_record(self, context):
        policy = context.user_data["access_policy"]
        allowed_regions = policy.get(self.role)

        if allowed_regions is None:
            raise ValueError(f"Unknown role: {self.role}")
        if self.region not in allowed_regions:
            raise ValueError(
                f"Role {self.role!r} is not allowed in region {self.region!r}"
            )


@scenario(
    "access.feature",
    "Validate users against a project access policy",
)
def test_context_aware_access_validation():
    pass


@given(
    "the following policy-compliant users exist:",
    target_fixture="validated_users",
)
def policy_compliant_users(datatable, bdd_table):
    return bdd_table.parse(
        datatable,
        schema=UserAccessTable,
        context={"access_policy": ACCESS_POLICY},
    )


@then("the users are accepted by the supplied policy")
def users_are_accepted(validated_users):
    assert [user.name for user in validated_users] == ["Alice", "Bob"]


def test_invalid_user_reports_the_source_row():
    invalid_table = [
        ["name", "role", "region"],
        ["Alice", "editor", "global"],
    ]

    with pytest.raises(BDDTableError, match="not allowed") as error:
        UserAccessTable.parse(
            invalid_table,
            context={"access_policy": ACCESS_POLICY},
        )

    assert "row=2" in str(error.value)
