from dataclasses import dataclass

from pytest_bdd import given, scenario, then

from bdd_tablex import (
    CellDSL,
    ColumnGroupExpander,
    ColumnTable,
    NumericRange,
    PrefixRepeat,
    TableFields,
    boolean,
    discriminator,
    field,
    id_field,
    reference,
)


class DemoContentGenerator:
    def headline(self, item_id):
        return f"Generated headline {item_id}"

    def words(self, count, item_id):
        return " ".join(f"item{item_id}-word{number}" for number in range(1, count + 1))


content_cells = CellDSL()


@content_cells.token("random")
def random_content_value(context):
    return context.user_data["generator"].headline(context.item_id)


@content_cells.pattern(r"(?P<count>\d+):word")
def generated_words(match, context):
    return context.user_data["generator"].words(int(match["count"]), context.item_id)


class ArticleFields(TableFields):
    body = field("Body*", required=True, parser=content_cells)
    related = reference("Related", many=True)

    def validate_record(self, context):
        minimum = context.user_data["minimum_article_words"]
        if len(self.body.split()) < minimum:
            raise ValueError(f"Article body must contain at least {minimum} words")
        if any(item.content_type != "Poll" for item in self.related):
            raise ValueError("Articles may relate only to Poll records")


class PollFields(TableFields):
    options: list[str] = field("Options*", required=True)
    closes_after_hours: int = field("Closes after hours", default=24)

    def validate_record(self, context):
        if len(self.options) < context.user_data["minimum_poll_options"]:
            raise ValueError("Poll does not have enough options")


class ContentTable(ColumnTable):
    table_transformer = ColumnGroupExpander(
        key_row="IDs",
        range_rule=NumericRange(separator=".."),
        repeat_rule=PrefixRepeat(separator=":"),
    )

    id = id_field("IDs")
    content_type = discriminator(
        "Type*",
        variants={"Article": ArticleFields, "Poll": PollFields},
    )
    headline = field("Headline*", required=True, parser=content_cells)
    category = field("Category", default="General")
    published = field("Published*", required=True, parser=boolean())


@dataclass(frozen=True)
class ArticleCommand:
    id: str
    content_type: str
    headline: str
    body: str


@dataclass(frozen=True)
class PollCommand:
    id: str
    content_type: str
    headline: str
    options: list[str]


class ArticleCommandFields(TableFields):
    output_model = ArticleCommand
    body = field("Body*", required=True)


class PollCommandFields(TableFields):
    output_model = PollCommand
    options: list[str] = field("Options*", required=True)


class PublishCommandTable(ColumnTable):
    id = id_field("IDs")
    content_type = discriminator(
        "Type*",
        variants={"Article": ArticleCommandFields, "Poll": PollCommandFields},
    )
    headline = field("Headline*", required=True)


@scenario("content.feature", "Parse a compact mixed-content table")
def test_complete_content_records():
    pass


@scenario("content.feature", "Convert each content variant to its own output model")
def test_complete_content_output_models():
    pass


@given("the following complete content table:", target_fixture="complete_content")
def complete_content_table(datatable, bdd_table):
    return bdd_table.parse(
        datatable,
        schema=ContentTable,
        context={
            "generator": DemoContentGenerator(),
            "minimum_article_words": 10,
            "minimum_poll_options": 2,
        },
    )


@then("the complete content records are typed and linked")
def complete_records_are_typed_and_linked(complete_content):
    first_article, second_article, poll = complete_content

    assert isinstance(first_article, ArticleFields)
    assert first_article.id == "1"
    assert first_article.headline == "Generated headline 1"
    assert len(first_article.body.split()) == 12
    assert first_article.published is True
    assert first_article.related == [poll]
    assert isinstance(second_article, ArticleFields)
    assert second_article.related == [poll]
    assert isinstance(poll, PollFields)
    assert poll.options == ["Equities", "Bonds"]
    assert poll.closes_after_hours == 24
    assert poll.published is False
    assert ContentTable.variant_for("Article") is type(first_article)
    assert first_article.source_for("headline").source_value == "2:random"


@given("the following publish commands:", target_fixture="publish_commands")
def publish_commands(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=PublishCommandTable)


@then("each publish command uses its variant output model")
def commands_use_variant_models(publish_commands):
    assert publish_commands == [
        ArticleCommand("A", "Article", "Morning brief", "Full text"),
        PollCommand("P", "Poll", "Choose a desk?", ["News", "Markets"]),
    ]
