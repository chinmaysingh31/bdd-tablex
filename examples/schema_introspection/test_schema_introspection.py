"""Executable example for schema contract introspection."""

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, TableFields, discriminator, field


class ArticleFields(TableFields):
    body = field("body", required=True)


class PollFields(TableFields):
    options: list[str] = field("options", required=True)


class ContentTable(RowTable):
    content_type = discriminator(
        "type",
        variants={"Article": ArticleFields, "Poll": PollFields},
    )
    headline = field("headline", aliases=("title",))


@scenario("content.feature", "Describe a table contract without parsing records")
def test_schema_contract():
    pass


@given("the content table schema is inspected", target_fixture="content_contract")
def content_schema_is_inspected():
    return ContentTable.describe()


@then("its fields and variants are machine readable")
def contract_is_machine_readable(content_contract):
    assert content_contract.orientation == "row"
    assert [variant.value for variant in content_contract.variants] == [
        "Article",
        "Poll",
    ]
    assert content_contract.variants[0].schema_name == "ContentTable[Article]"
    assert content_contract.as_dict()["fields"][1]["aliases"] == ("title",)
