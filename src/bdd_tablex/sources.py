"""Read-only source metadata attached to parsed schema records."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from .table import TableCell


@dataclass(frozen=True)
class RecordSource:
    """Original table locations associated with one parsed schema record.

    Attributes:
        item_id: Parsed local ID for column-oriented records when available.
        row: Source row for a row-oriented record.
        column: Source key/ID column for a column-oriented record.
        cells: Mapping from schema attribute names to their source cells.

    """

    item_id: Any | None
    row: int | None
    column: int | None
    cells: Mapping[str, TableCell]

    @classmethod
    def create(
        cls,
        *,
        item_id: Any | None = None,
        row: int | None = None,
        column: int | None = None,
        cells: Mapping[str, TableCell] | None = None,
    ) -> RecordSource:
        """Create immutable metadata from parser-owned source values."""
        return cls(
            item_id=item_id,
            row=row,
            column=column,
            cells=MappingProxyType(dict(cells or {})),
        )

    def source_for(self, field_name: str) -> TableCell:
        """Return the source cell for one schema attribute name."""
        try:
            return self.cells[field_name]
        except KeyError as exc:
            message = f"No source cell is available for field {field_name!r}"
            raise KeyError(message) from exc
