from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, TableData, compose_transformers, field, id_field


class UppercaseId:
    def transform(self, table, context, *, schema=None):
        rows = [list(row) for row in table.rows]
        rows[0][1] = rows[0][1].with_value(rows[0][1].value.upper())
        return TableData.from_cells(rows)


class TitleHeadline:
    def transform(self, table, context, *, schema=None):
        rows = [list(row) for row in table.rows]
        rows[1][1] = rows[1][1].with_value(rows[1][1].value.title())
        return TableData.from_cells(rows)


class ContentTable(ColumnTable):
    table_transformer = compose_transformers(UppercaseId(), TitleHeadline())

    id = id_field("IDs")
    headline = field("Headline*", required=True)


@scenario("content.feature", "Transformer pipelines run left to right")
def test_transformer_pipeline():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("transformer pipelines can normalize source tables")
def transformer_pipeline(rows):
    record = ContentTable.parse_records(rows)[0]

    assert record.id == "A-1"
    assert record.headline == "Market Brief"
    assert record.source_for("headline").source_value == "market brief"
