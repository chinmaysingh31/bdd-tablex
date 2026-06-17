from decimal import Decimal
from enum import Enum
from typing import Literal

import pytest

from bdd_tablex import BDDTableError, RowTable, field, string


class Status(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


def test_annotations_infer_supported_scalar_parsers():
    class TypedTable(RowTable):
        count: int = field("count")
        ratio: float = field("ratio")
        price: Decimal = field("price")
        active: bool = field("active")
        status: Status = field("status")

    record = TypedTable.parse(
        [
            ["count", "ratio", "price", "active", "status"],
            ["3", "1.5", "12.30", "yes", "published"],
        ]
    )[0]

    assert record.count == 3
    assert record.ratio == 1.5
    assert record.price == Decimal("12.30")
    assert record.active is True
    assert record.status is Status.PUBLISHED


def test_annotations_infer_optional_list_and_literal_parsers():
    class TypedTable(RowTable):
        age: int | None = field("age")
        tags: list[str] = field("tags")
        state: Literal["draft", "published"] = field("state")

    records = TypedTable.parse(
        [
            ["age", "tags", "state"],
            ["", "news, featured", "draft"],
            ["30", "archive", "published"],
        ]
    )

    assert records[0].age is None
    assert records[0].tags == ["news", "featured"]
    assert records[1].age == 30


def test_explicit_parser_takes_precedence_over_annotation():
    class TypedTable(RowTable):
        count: int = field("count", parser=string(upper=True))

    assert TypedTable.parse([["count"], ["many"]])[0].count == "MANY"


def test_unsupported_annotations_leave_values_unchanged():
    class CustomType:
        pass

    class TypedTable(RowTable):
        value: CustomType = field("value")

    assert TypedTable.parse([["value"], ["raw"]])[0].value == "raw"


def test_inferred_parser_errors_keep_cell_location():
    class TypedTable(RowTable):
        count: int = field("count")

    with pytest.raises(BDDTableError, match="invalid literal") as error:
        TypedTable.parse([["count"], ["many"]])

    assert error.value.row == 2
    assert error.value.column == 1
