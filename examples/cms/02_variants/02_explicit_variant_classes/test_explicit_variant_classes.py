from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, discriminator_field, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = discriminator_field("Type*")
    headline = field("Headline*", required=True)


@ContentTable.variant("Article")
class ArticleContent(ContentTable):
    body = field("Body*", required=True)


@ContentTable.variant("Video")
class VideoContent(ContentTable):
    url = field("URL*", required=True)


@scenario("content.feature", "Select variants registered with decorators")
def test_explicit_variant_classes():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("explicit variant classes produce typed records")
def explicit_variants(rows):
    article, video = ContentTable.parse(rows)

    assert isinstance(article, ArticleContent)
    assert article.body == "Full text"
    assert isinstance(video, VideoContent)
    assert video.url == "/launch-video"
