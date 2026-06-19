import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableError, BDDTableErrorCode, ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    content_type = field("Type*", required=True)
    headline = field("Headline*", required=True)


@scenario("content.feature", "Duplicate item IDs report the offending item")
def test_duplicate_ids_and_item_diagnostics():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("duplicate IDs are reported with item diagnostics")
def duplicate_ids_are_reported(rows):
    with pytest.raises(BDDTableError) as error:
        ContentTable.parse(rows)

    assert error.value.code == BDDTableErrorCode.DUPLICATE_ID
    assert error.value.field == "IDs"
    assert error.value.item_id == "A-1"
    assert error.value.row == 2
    assert error.value.column == 3
