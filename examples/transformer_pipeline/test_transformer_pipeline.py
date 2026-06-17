"""Executable example for source-aware table transformer composition."""

from pytest_bdd import given, scenario, then

from bdd_tablex import (
    ColumnGroupExpander,
    ColumnTable,
    NumericRange,
    PrefixRepeat,
    TableData,
    compose_transformers,
    field,
    id_field,
)


class RenameContentIDs:
    """Project transformer that normalizes one historical row label."""

    def transform(self, table, context, *, schema=None):
        rows = [list(row) for row in table.rows]
        rows[0][0] = rows[0][0].with_value("IDs")
        return TableData.from_cells(rows)


class ContentTable(ColumnTable):
    table_transformer = compose_transformers(
        RenameContentIDs(),
        ColumnGroupExpander(
            key_row="IDs",
            range_rule=NumericRange(".."),
            repeat_rule=PrefixRepeat(":"),
        ),
    )

    id = id_field("IDs")
    content_type = field("Type", required=True)


@scenario("content.feature", "Normalize labels before expanding grouped columns")
def test_composed_transformers():
    pass


@given("the following pipelined content:", target_fixture="pipelined_content")
def pipelined_content(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=ContentTable)


@then("both transformer stages have run in order")
def transformer_stages_ran(pipelined_content):
    assert [item.id for item in pipelined_content] == ["1", "2"]
    assert [item.content_type for item in pipelined_content] == [
        "Article",
        "Article",
    ]
    assert pipelined_content[0].source_for("id").source_value == "1..2"
