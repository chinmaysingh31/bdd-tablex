from pathlib import Path

from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnTable, check_feature, discover_feature_tables, field, id_field
from bdd_tablex.checker import check_feature_tables


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True)


@scenario("content.feature", "Python API finds table diagnostics")
def test_static_checker_python_api():
    pass


@given("the following statically checked content exists:", target_fixture="feature_path")
def statically_checked_content(datatable):
    return Path(__file__).with_name("content.feature")


@then("the Python checker reports structured diagnostics")
def static_checker_python_api(feature_path):
    tables = discover_feature_tables(
        feature_path,
        step="the following statically checked content exists:",
    )
    diagnostics = check_feature_tables(tables, schema=ContentTable)
    direct = check_feature(
        feature_path,
        schema=ContentTable,
        step="the following statically checked content exists:",
    )

    assert len(tables) == 1
    assert len(diagnostics) == 1
    assert len(direct) == 1
    assert diagnostics[0].error.field == "Headline*"
    assert diagnostics[0].error.item_id == "A-2"
