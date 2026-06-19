import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableError, ColumnTable, TableFields, discriminator, field, id_field


class ArticleFields(TableFields):
    body = field("Body*", required=True)

    def validate_record(self, context):
        if len(self.body.split()) < context.user_data["minimum_words"]:
            raise ValueError("article body is too short")


class PollFields(TableFields):
    options: list[str] = field("Options*", required=True)


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = discriminator(
        "Type*",
        variants={"Article": ArticleFields, "Poll": PollFields},
    )
    headline = field("Headline*", required=True)


@scenario("content.feature", "Article validation runs only for article records")
def test_variant_specific_validation():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("variant validation reports article policy errors")
def variant_validation(rows):
    with pytest.raises(BDDTableError) as error:
        ContentTable.parse(rows, context={"minimum_words": 3})

    assert "article body is too short" in str(error.value)
    assert error.value.schema == "ContentTable[Article]"
    assert error.value.item_id == "A-1"
