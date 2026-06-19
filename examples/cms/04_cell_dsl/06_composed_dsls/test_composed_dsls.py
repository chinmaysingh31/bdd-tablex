from pytest_bdd import given, scenario, then

from bdd_tablex import CellDSL, ColumnTable, compose_cell_dsls, field, id_field


shared_cells = CellDSL()
project_cells = CellDSL()


@shared_cells.token("none")
def none_value(context):
    return None


@project_cells.pattern(r"fake:(.+)")
def generated_value(match, context):
    return f"Generated {match[1]}"


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field(
        "Headline*",
        parser=compose_cell_dsls(shared_cells, project_cells),
    )


@scenario("content.feature", "Composed DSLs use the first matching grammar")
def test_composed_dsls():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("composed CellDSLs are applied in order")
def composed_dsls(rows):
    records = ContentTable.parse(rows)

    assert [record.headline for record in records] == [
        None,
        "Generated hero",
        "Literal",
    ]
