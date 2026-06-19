from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, TableFields, discriminator, field, id_field


class ArticleFields(TableFields):
    body = field("Body*", required=True)


class PollFields(TableFields):
    options: list[str] = field("Options*", required=True)


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = discriminator(
        "Type*",
        variants={"Article": ArticleFields, "Poll": PollFields},
    )
    headline = field("Headline*", required=True)


@scenario("content.feature", "Select variants declared with TableFields")
def test_declarative_tablefields_variants():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("declarative variants produce typed records")
def declarative_variants(rows):
    article, poll = ContentTable.parse(rows)

    assert isinstance(article, ArticleFields)
    assert isinstance(article, ContentTable)
    assert article.body == "Full text"
    assert isinstance(poll, PollFields)
    assert poll.options == ["Yes", "No"]
    assert ContentTable.variant_for("Article") is type(article)
