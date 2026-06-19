"""Executable example for scoped, predicate, and composed CellDSL rules."""

from pytest_bdd import given, scenario, then

from bdd_tablex import CellDSL, RowTable, compose_cell_dsls, field

shared_cells = CellDSL()
content_cells = CellDSL()


@shared_cells.token("none")
def none_value(context):
    """A reusable token shared by several project domains."""

    return None


@content_cells.token("random", fields={"headline"})
def random_headline(context):
    """Limit this token to the headline schema attribute."""

    return context.user_data["headline_factory"]()


@content_cells.when(lambda value, context: value.startswith("fake:"))
def fake_content_value(value, context):
    """Use a predicate for syntax that does not need regex captures."""

    return f"Generated {value.removeprefix('fake:')}"


content_parser = compose_cell_dsls(shared_cells, content_cells)


class ContentTable(RowTable):
    headline = field("headline", parser=content_parser)
    category = field("category", parser=content_parser)


@scenario("content.feature", "Combine shared and field-specific cell rules")
def test_composable_cell_dsl():
    pass


@given("the following composable content:", target_fixture="composable_content")
def composable_content(datatable, bdd_table):
    return bdd_table.parse(
        datatable,
        schema=ContentTable,
        context={"headline_factory": lambda: "Generated headline"},
    )


@then("the first matching scoped or composed rule is used")
def first_matching_rule_is_used(composable_content):
    assert composable_content[0].headline == "Generated headline"
    assert composable_content[0].category == "random"
    assert composable_content[1].headline == "Generated poll"
    assert composable_content[1].category is None
