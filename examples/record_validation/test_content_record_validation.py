"""Executable pytest-bdd example for content record validation."""

import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableError, ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)
    category = field("Category")

    def validate_record(self, context):
        if self.content_type == "Poll" and not self.headline.endswith("?"):
            raise ValueError("Poll headlines must end with a question mark")

        if self.content_type == "Article" and not self.category:
            raise ValueError("Articles must have a category")


@scenario(
    "content.feature",
    "Validate relationships between parsed content fields",
)
def test_valid_content_records():
    pass


@given("the following validated content exists:", target_fixture="content_items")
def validated_content_exists(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=ContentTable)


@then("both content records pass their schema rules")
def both_records_are_valid(content_items):
    assert [item.id for item in content_items] == ["1", "2"]


def test_invalid_poll_reports_its_table_column_and_item_id():
    invalid_table = [
        ["IDs", "1", "2"],
        ["Type*", "Article", "Poll"],
        ["Headline*", "Market update", "Choose one"],
        ["Category", "Markets", ""],
    ]

    with pytest.raises(BDDTableError, match="Poll headlines") as error:
        ContentTable.parse(invalid_table)

    assert "column=3" in str(error.value)
    assert "item_id='2'" in str(error.value)
