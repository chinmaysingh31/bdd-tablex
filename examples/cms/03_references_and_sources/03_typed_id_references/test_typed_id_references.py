from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, field, id_field, integer, reference


class ContentTable(ColumnTable):
    id = id_field("IDs", parser=integer())
    headline = field("Headline*", required=True)
    parent = reference("Parent")


@scenario("content.feature", "Reference keys use the target ID parser")
def test_typed_id_references():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("typed ID references resolve using parsed IDs")
def typed_id_references(rows):
    parent, child = ContentTable.parse(rows)

    assert parent.id == 101
    assert child.id == 102
    assert child.parent is parent
