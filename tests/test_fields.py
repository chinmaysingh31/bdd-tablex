import pytest

from bdd_tablex import (
    BDDTableError,
    ColumnTable,
    RowTable,
    SchemaDefinitionError,
    field,
    id_field,
)


def test_asterisk_in_label_has_no_implicit_meaning():
    class LiteralLabelTable(RowTable):
        value = field("Value*")

    record = LiteralLabelTable.parse([["Value*"], [""]])[0]

    assert record.value == ""


def test_column_table_requires_exactly_one_id_field():
    class MissingIdTable(ColumnTable):
        value = field("Value")

    with pytest.raises(BDDTableError, match="exactly one id_field"):
        MissingIdTable.parse([["Value", "one"]])


def test_duplicate_schema_labels_are_rejected():
    with pytest.raises(SchemaDefinitionError, match="already used"):

        class DuplicateSchema(RowTable):
            first = field("value")
            second = field("value")


def test_id_field_can_use_a_custom_parser():
    class NumberedTable(ColumnTable):
        id = id_field("IDs", parser=lambda value, context: int(value))
        value = field("Value")

    assert NumberedTable.parse([["IDs", "7"], ["Value", "seven"]])[0].id == 7
