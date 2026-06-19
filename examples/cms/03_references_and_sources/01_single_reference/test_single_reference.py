from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, field, id_field, reference


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True)
    parent = reference("Parent")


@scenario("content.feature", "Resolve one parent reference")
def test_single_reference():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the parent reference resolves to another record")
def single_reference(rows):
    root, child = ContentTable.parse(rows)

    assert root.parent is None
    assert child.parent is root
    assert child.parent.headline == "Home"
