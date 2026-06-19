from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True)
    status = field("Status")


@scenario("content.feature", "Inspect source metadata for parsed records")
def test_record_sources():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("record sources expose item and field cells")
def record_sources(rows):
    record = ContentTable.parse_records(rows)[0]
    headline_cell = record.source_for("headline")

    assert record.table_source.item_id == "A-1"
    assert record.table_source.column == 2
    assert headline_cell.value == "Market brief"
    assert headline_cell.source_row == 3
    assert headline_cell.source_column == 2
