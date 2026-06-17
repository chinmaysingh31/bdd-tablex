import pytest

from bdd_tablex import BDDTableError, ColumnTable, RowTable, field, id_field


class SimpleRows(RowTable):
    value = field("value")


class SimpleColumns(ColumnTable):
    id = id_field("IDs")
    value = field("Value")


@pytest.mark.parametrize(
    ("datatable", "message"),
    [
        ([], "Table is empty"),
        ([[]], "Table header is empty"),
        ([["value"], ["one", "extra"]], "Ragged row"),
        ([["value", "value"], ["one", "two"]], "duplicate field label"),
        ([["unknown"], ["one"]], "Unknown field label"),
    ],
)
def test_row_table_shape_errors(datatable, message):
    with pytest.raises(BDDTableError, match=message):
        SimpleRows.parse(datatable)


@pytest.mark.parametrize(
    ("datatable", "message"),
    [
        ([["IDs", "1"], ["Value"]], "Ragged row"),
        ([["IDs", "1"], ["Value", "one"], ["Value", "two"]], "duplicate field"),
        ([["IDs", "1"], ["Unknown", "one"]], "Unknown field label"),
    ],
)
def test_column_table_shape_errors(datatable, message):
    with pytest.raises(BDDTableError, match=message):
        SimpleColumns.parse(datatable)
