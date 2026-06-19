from pytest_bdd import given, scenario, then

from bdd_tablex import TableData


@scenario(
    "content.feature", "TableData keeps current values and original source values"
)
def test_tabledata_and_tablecell():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("TableData and TableCell expose source-aware values")
def tabledata_and_tablecell(rows):
    table = TableData.from_rows(rows)
    headline_cell = table.cell(2, 2)
    rewritten = headline_cell.with_value("Generated headline")

    assert table.to_rows()[1][1] == "Market brief"
    assert headline_cell.source_row == 2
    assert headline_cell.source_column == 2
    assert rewritten.value == "Generated headline"
    assert rewritten.source_value == "Market brief"
