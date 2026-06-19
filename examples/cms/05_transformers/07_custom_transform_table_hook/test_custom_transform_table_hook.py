from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, TableData, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True)

    @classmethod
    def transform_table(cls, table, context):
        rows = [list(row) for row in table.rows]
        rows[1][1] = rows[1][1].with_value("Reviewed draft")
        return TableData.from_cells(rows)


@scenario("content.feature", "A schema can override transform_table directly")
def test_custom_transform_table_hook():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("custom transform_table hooks can rewrite logical cells")
def custom_transform_table_hook(rows):
    record = ContentTable.parse_records(rows)[0]

    assert record.headline == "Reviewed draft"
    assert record.source_for("headline").source_value == "draft"
