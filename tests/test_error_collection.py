import pytest

from bdd_tablex import (
    BDDTableError,
    BDDTableErrors,
    ColumnTable,
    RowTable,
    field,
    id_field,
)


def test_collect_mode_reports_multiple_cells_in_discovery_order():
    class UserTable(RowTable):
        name = field("name", required=True)
        age: int = field("age")

    with pytest.raises(BDDTableErrors) as captured:
        UserTable.parse(
            [
                ["name", "age"],
                ["", "old"],
                ["", "older"],
            ],
            error_mode="collect",
        )

    errors = captured.value.errors
    assert len(errors) == 4
    assert [error.code for error in errors] == [
        "empty_required",
        "parser_failed",
        "empty_required",
        "parser_failed",
    ]
    assert [(error.row, error.column) for error in errors] == [
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
    ]


def test_first_mode_remains_the_default():
    class UserTable(RowTable):
        name = field("name", required=True)
        age: int = field("age")

    with pytest.raises(BDDTableError) as captured:
        UserTable.parse([["name", "age"], ["", "old"]])

    assert not isinstance(captured.value, BDDTableErrors)
    assert captured.value.code == "empty_required"


def test_collect_mode_combines_valid_record_validation_failures():
    class ScoreTable(ColumnTable):
        id = id_field("IDs")
        score: int = field("Score")

        def validate_record(self, context):
            if self.score < 0:
                raise ValueError("score cannot be negative")

    with pytest.raises(BDDTableErrors) as captured:
        ScoreTable.parse(
            [["IDs", "1", "2"], ["Score", "-1", "-2"]],
            error_mode="collect",
        )

    assert len(captured.value) == 2
    assert all(error.code == "record_validation_failed" for error in captured.value)


def test_invalid_error_mode_is_rejected():
    class ValueTable(RowTable):
        value = field("value")

    with pytest.raises(ValueError, match="error_mode"):
        ValueTable.parse([["value"], ["one"]], error_mode="everything")
