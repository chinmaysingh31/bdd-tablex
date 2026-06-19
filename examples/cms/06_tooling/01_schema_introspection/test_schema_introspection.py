from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True)
    status = field("Status")


@scenario("content.feature", "Inspect a CMS schema contract")
def test_schema_introspection():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("schema introspection returns a machine-readable contract")
def schema_introspection(rows):
    contract = ContentTable.describe()

    assert contract.schema_name == "ContentTable"
    assert contract.orientation == "column"
    assert [field.label for field in contract.fields] == ["IDs", "Headline*", "Status"]
    assert contract.fields[0].is_id is True
    assert contract.as_dict()["fields"][1]["required"] is True
