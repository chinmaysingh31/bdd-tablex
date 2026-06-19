from pytest_bdd import given, scenario, then

from bdd_tablex import CellDSL, ColumnTable, field, id_field


class ExampleGenerator:
    """A deterministic stand-in for a project's Faker or data factory."""

    def random_for(self, field_name):
        values = {
            "headline": "Generated headline",
            "category": "Technology",
        }
        return values[field_name]

    def words(self, count):
        return " ".join(f"word-{number}" for number in range(1, count + 1))


content_cells = CellDSL()


@content_cells.token("random")
def random_value(context):
    generator = context.user_data["generator"]
    return generator.random_for(context.field_name)


@content_cells.pattern(r"(?P<count>\d+) words")
def generated_words(match, context):
    generator = context.user_data["generator"]
    return generator.words(int(match["count"]))


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True, parser=content_cells)
    category = field("Category", parser=content_cells)


@scenario(
    "content.feature",
    "Parse tokens, patterns, literal values, and empty cells",
)
def test_custom_content_cell_dsl():
    pass


@given("the following generated content exists:", target_fixture="content_items")
def generated_content_exists(datatable, bdd_table):
    return bdd_table.parse(
        datatable,
        schema=ContentTable,
        context={"generator": ExampleGenerator()},
    )


@then("the content table contains the expected normalized values")
def expected_content_values(content_items):
    assert content_items[0].as_dict() == {
        "id": "1",
        "content_type": "Article",
        "headline": "Generated headline",
        "category": "Technology",
    }
    assert content_items[1].headline == "word-1 word-2 word-3"
    assert content_items[1].category == "Markets"
    assert content_items[2].headline == "A literal headline"
    assert content_items[2].category == ""
