from decimal import Decimal
from enum import Enum
from typing import Literal

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field, string


class Status(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class UserTable(RowTable):
    age: int = field("age")
    ratio: float = field("ratio")
    balance: Decimal = field("balance")
    active: bool = field("active")
    status: Status = field("status")
    tier: Literal["basic", "staff"] = field("tier")
    tags: list[str] = field("tags")
    reviewer: int | None = field("reviewer")
    override: int = field("override", parser=string(upper=True))


@scenario("users.feature", "Demonstrate Annotation Inference")
def test_annotation_inference():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the annotation inference behavior is correct")
def behavior(rows):
    user = UserTable.parse(rows)[0]
    assert user.age == 34
    assert user.ratio == 1.5
    assert user.balance == Decimal("12.30")
    assert user.active is True
    assert user.status is Status.PUBLISHED
    assert user.tier == "staff"
    assert user.tags == ["qa", "docs"]
    assert user.reviewer is None
    assert user.override == "MANY"
