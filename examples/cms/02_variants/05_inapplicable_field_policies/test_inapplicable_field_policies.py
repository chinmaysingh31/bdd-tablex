from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, TableFields, discriminator, field, id_field


class ArticleFields(TableFields):
    body = field("Body*")


class PollFields(TableFields):
    options: list[str] = field("Options*", required=True)


class ContentTable(ColumnTable):
    inapplicable_fields = "preserve"

    id = id_field("IDs")
    content_type = discriminator(
        "Type*",
        variants={"Article": ArticleFields, "Poll": PollFields},
    )
    headline = field("Headline*", required=True)


@scenario("content.feature", "Preserve a value written for another variant")
def test_inapplicable_field_policies():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("inapplicable values are preserved as extras")
def inapplicable_values_are_preserved(rows):
    poll = ContentTable.parse_records(rows)[0]

    assert isinstance(poll, PollFields)
    assert poll.options == ["Yes", "No"]
    assert poll.table_extras == {"Body*": "copied note"}
