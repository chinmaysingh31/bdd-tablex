import pytest

from bdd_tablex import BDDTableError, RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)
    role = field("role", required=True)
    active = field("active", default=True)


def test_parses_rows_into_schema_records():
    users = UserTable.parse(
        [
            ["name", "role", "active"],
            ["Alice", "admin", "yes"],
            ["Bob", "editor", ""],
        ]
    )

    assert users[0].name == "Alice"
    assert users[0].as_dict() == {
        "name": "Alice",
        "role": "admin",
        "active": "yes",
    }
    assert users[1].active == ""
    assert repr(users[0]).startswith("UserTable(name='Alice'")


def test_missing_optional_header_uses_default():
    users = UserTable.parse([["name", "role"], ["Alice", "admin"]])

    assert users[0].active is True


def test_missing_required_header_is_rejected():
    with pytest.raises(BDDTableError, match="Required field is missing") as error:
        UserTable.parse([["name"], ["Alice"]])

    assert "field='role'" in str(error.value)


def test_missing_required_header_is_rejected_without_data_rows():
    with pytest.raises(BDDTableError, match="Required field is missing"):
        UserTable.parse([["name"]])


def test_empty_required_cell_is_rejected():
    with pytest.raises(BDDTableError, match="empty value") as error:
        UserTable.parse([["name", "role"], ["Alice", ""]])

    message = str(error.value)
    assert "row=2" in message
    assert "column=2" in message
    assert "value=''" in message
