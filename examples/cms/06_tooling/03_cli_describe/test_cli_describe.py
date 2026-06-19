from pytest_bdd import given, scenario, then
from schemas import ContentTable


@scenario("content.feature", "Describe a CLI-importable schema")
def test_cli_describe():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("CLI describe uses a plain schema module")
def cli_describe(rows):
    contract = ContentTable.describe()

    assert contract.schema_name == "ContentTable"
    assert [field.label for field in contract.fields] == ["IDs", "Headline*", "Status"]
    assert ContentTable.parse(rows)[0].status == "draft"
