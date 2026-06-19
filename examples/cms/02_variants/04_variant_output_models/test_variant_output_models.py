from dataclasses import dataclass

from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, TableFields, discriminator, field, id_field


@dataclass(frozen=True)
class Article:
    id: str
    content_type: str
    headline: str
    body: str


@dataclass(frozen=True)
class Poll:
    id: str
    content_type: str
    headline: str
    options: list[str]


class ArticleFields(TableFields):
    output_model = Article
    body = field("Body*", required=True)


class PollFields(TableFields):
    output_model = Poll
    options: list[str] = field("Options*", required=True)


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = discriminator(
        "Type*",
        variants={"Article": ArticleFields, "Poll": PollFields},
    )
    headline = field("Headline*", required=True)


@scenario("content.feature", "Convert each variant to its own output model")
def test_variant_output_models():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("variant records become variant output models")
def variant_output_models(rows):
    assert ContentTable.parse(rows) == [
        Article("A-1", "Article", "Market brief", "Full text"),
        Poll("P-1", "Poll", "Reader question", ["Yes", "No"]),
    ]
