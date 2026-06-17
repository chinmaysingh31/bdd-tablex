"""Functional parsing helpers for projects that prefer explicit APIs.

The schema methods remain the primary interface:

``UserTable.parse(datatable)``

Some teams prefer a parser-function style because it makes the schema an
argument rather than the object receiving the call. The helpers in this module
support that style without creating another parsing implementation.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from .context import ParseContext
from .schema import BaseTable
from .table import RawTable, TableData

TableT = TypeVar("TableT", bound=BaseTable)


def parse_table(
    schema: type[BaseTable],
    datatable: RawTable | TableData,
    *,
    context: Mapping[str, Any] | ParseContext | None = None,
    error_mode: str = "first",
) -> list[Any]:
    """Parse a BDD table using a schema class.

    This is the functional equivalent of ``schema.parse(datatable)``. It is
    useful in codebases that prefer explicit parser functions over classmethod
    calls, and it returns the same public result as the schema method,
    including output-model conversion when configured.
    """
    return schema.parse(datatable, context=context, error_mode=error_mode)


def parse_table_records(
    schema: type[TableT],
    datatable: RawTable | TableData,
    *,
    context: Mapping[str, Any] | ParseContext | None = None,
    error_mode: str = "first",
) -> list[TableT]:
    """Parse a BDD table and return validated schema record instances.

    This is the functional equivalent of ``schema.parse_records(datatable)``.
    It intentionally skips optional output-model conversion, making the return
    type useful for static type checkers and tests that need source metadata or
    intermediate schema records.
    """
    return schema.parse_records(datatable, context=context, error_mode=error_mode)
