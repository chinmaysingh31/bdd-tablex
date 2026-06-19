"""Executable pytest-bdd example for column-oriented content variants."""

from pytest_bdd import given, scenario, then

from bdd_tablex import (
    ColumnTable,
    discriminator_field,
    field,
    id_field,
)


class ContentTable(ColumnTable):
    """Fields shared by every kind of content in this project."""

    id = id_field("IDs")
    content_type = discriminator_field("Type*")
    headline = field("Headline*", required=True)


@ContentTable.variant("Article")
class ArticleContent(ContentTable):
    """Additional table contract for Article records only."""

    body = field("Body*", required=True)

    def validate_record(self, context):
        """Keep Article-specific policy beside the Article fields."""

        if len(self.body) < context.user_data["minimum_body_length"]:
            raise ValueError("Article body is too short")


@ContentTable.variant("Poll")
class PollContent(ContentTable):
    """Additional table contract for Poll records only."""

    options: list[str] = field("Options*", required=True)

    def validate_record(self, context):
        """A Poll requires enough choices to be meaningful."""

        if len(self.options) < 2:
            raise ValueError("Poll requires at least two options")


@scenario("content_variants.feature", "Parse different content shapes from one table")
def test_content_variants():
    pass


@given("the following mixed content exists:", target_fixture="content_items")
def mixed_content_exists(datatable, bdd_table):
    """Parse through the package fixture exactly as a real step would."""

    return bdd_table.parse(
        datatable,
        schema=ContentTable,
        context={"minimum_body_length": 10},
    )


@then("each content type has its own parsed fields")
def content_types_have_own_fields(content_items):
    article, poll = content_items

    assert isinstance(article, ArticleContent)
    assert article.body == "A detailed news body"
    assert not hasattr(article, "options")

    assert isinstance(poll, PollContent)
    assert poll.options == ["Equities", "Bonds"]
    assert not hasattr(poll, "body")
