"""Small pytest integration for bdd-tablex."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

import pytest

from .context import ParseContext
from .schema import BaseTable
from .table import RawTable, TableData

TableT = TypeVar("TableT", bound=BaseTable)


class BDDTableParser:
    """Convenience facade exposed through the ``bdd_table`` fixture.

    This facade intentionally delegates to the schema class. It does not own
    a second parser, registry, or pytest-specific table lifecycle.
    """

    def parse(
        self,
        datatable: RawTable | TableData,
        *,
        schema: type[BaseTable],
        context: Mapping[str, Any] | ParseContext | None = None,
        error_mode: str = "first",
    ) -> list[Any]:
        """Parse a raw or source-aware table with the requested schema."""
        return schema.parse(datatable, context=context, error_mode=error_mode)

    def parse_records(
        self,
        datatable: RawTable | TableData,
        *,
        schema: type[TableT],
        context: Mapping[str, Any] | ParseContext | None = None,
        error_mode: str = "first",
    ) -> list[TableT]:
        """Parse a table and return validated schema records.

        This mirrors ``schema.parse_records(...)`` for pytest and pytest-bdd
        steps that want type-checker-friendly schema instances instead of
        optional output-model conversion.
        """
        return schema.parse_records(datatable, context=context, error_mode=error_mode)


@pytest.fixture
def bdd_table() -> BDDTableParser:
    """Provide the small schema parsing facade to pytest and pytest-bdd tests."""
    return BDDTableParser()
