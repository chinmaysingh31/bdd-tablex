"""Executable example for annotation-driven field conversion."""

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field


class AnnotatedUserTable(RowTable):
    name: str = field("name", required=True)
    age: int | None = field("age")
    active: bool = field("active", required=True)
    tags: list[str] = field("tags")


@scenario("users.feature", "Infer common parsers from field annotations")
def test_annotated_schema():
    pass


@given("the following annotated users exist:", target_fixture="annotated_users")
def annotated_users(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=AnnotatedUserTable)


@then("annotations produce typed values")
def annotations_produce_typed_values(annotated_users):
    assert annotated_users[0].age == 30
    assert annotated_users[0].active is True
    assert annotated_users[0].tags == ["admin", "editorial"]
    assert annotated_users[1].age is None
    assert annotated_users[1].active is False
