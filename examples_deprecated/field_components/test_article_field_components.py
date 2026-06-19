"""Executable article example for reusable groups of field declarations."""

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, TableFields, field


class AuditFields(TableFields):
    """Field declarations shared by several project schemas."""

    created_by = field("created_by", required=True)
    trace_id = field("trace_id", required=True)


class ArticleTable(RowTable, AuditFields):
    headline = field("headline", required=True)


@scenario("articles.feature", "Reuse audit fields in an article table")
def test_reusable_field_components():
    pass


@given("the following audited articles exist:", target_fixture="articles")
def audited_articles(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=ArticleTable)


@then("the article contains its reusable audit fields")
def article_contains_audit_fields(articles):
    article = articles[0]
    assert article.headline == "News"
    assert article.created_by == "Alice"
    assert article.trace_id == "trace-1"
