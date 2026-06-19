from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, field, id_field, reference


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True)
    related = reference("Related", many=True)


@scenario("content.feature", "Resolve several related content references")
def test_many_references():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("many references resolve in table order")
def many_references(rows):
    article, poll, video = ContentTable.parse(rows)

    assert article.related == [poll, video]
    assert poll.related == []
    assert video.related == [poll]
