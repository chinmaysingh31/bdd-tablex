from pytest_bdd import given, scenario, then

from bdd_tablex import CellDSL, ColumnTable, field, id_field

content_cells = CellDSL()


@content_cells.pattern(r"(?P<count>\d+):word")
def generated_words(match, context):
    return " ".join(
        f"{context.item_id}-{number}" for number in range(1, int(match["count"]) + 1)
    )


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True, parser=content_cells)


@scenario("content.feature", "Regex patterns use captured values")
def test_regex_patterns():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("regex CellDSL patterns are applied")
def regex_patterns(rows):
    record = ContentTable.parse(rows)[0]

    assert record.headline == "A-1-1 A-1-2 A-1-3"
