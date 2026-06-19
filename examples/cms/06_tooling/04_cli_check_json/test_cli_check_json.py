from pathlib import Path

from pytest_bdd import given, scenario, then
from schemas import ContentTable

from bdd_tablex import check_feature


@scenario(
    "content.feature", "Check a CLI-importable schema and render JSON diagnostics"
)
def test_cli_check_json():
    pass


@given(
    "the following statically checked content exists:", target_fixture="feature_path"
)
def statically_checked_content(datatable):
    return Path(__file__).with_name("content.feature")


@then("CLI check JSON uses a plain schema module")
def cli_check_json(feature_path):
    diagnostics = check_feature(
        feature_path,
        schema=ContentTable,
        step="the following statically checked content exists:",
    )

    assert len(diagnostics) == 1
    assert diagnostics[0].error.field == "Headline*"
    assert diagnostics[0].error.item_id == "A-2"
