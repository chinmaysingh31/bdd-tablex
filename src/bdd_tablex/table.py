"""Source-aware table values used by parsing and table transformations.

The public schema API accepts ordinary ``list[list[str]]`` values because that
is what pytest-bdd supplies to step functions. Internally, every raw string is
wrapped in :class:`TableCell` so later stages can report the location of the
original feature-file cell.

Projects that implement a custom table transformation may use these classes
directly. A transformed cell should normally be created with
``source_cell.with_value(new_value)``. That keeps diagnostics attached to the
cell syntax the user actually wrote.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import cast

RawTable = Sequence[Sequence[str]]


@dataclass(frozen=True)
class TableCell:
    """One current table value and the feature cell from which it originated.

    Attributes:
        value: The value currently consumed by schema parsing. A transformer
            may change this value.
        source_row: One-based row number of the original BDD table cell.
        source_column: One-based column number of the original BDD table cell.
        source_value: The exact value before any table transformation.

    A transformer may produce several cells from one source cell. Each new
    cell can therefore have a different ``value`` while sharing the same
    source location and ``source_value``.

    """

    value: str
    source_row: int
    source_column: int
    source_value: str

    @classmethod
    def from_value(cls, value: str, *, row: int, column: int) -> TableCell:
        """Create an untransformed cell at a one-based source location."""
        return cls(
            value=value,
            source_row=row,
            source_column=column,
            source_value=value,
        )

    def with_value(self, value: str) -> TableCell:
        """Return a changed cell that still points to this cell's source.

        This is the preferred way for a table transformer to replace or
        expand syntax. For example, a source cell containing ``3:Article``
        may produce three cells whose current value is ``Article`` while all
        three still point back to the original ``3:Article`` cell.
        """
        return TableCell(
            value=value,
            source_row=self.source_row,
            source_column=self.source_column,
            source_value=self.source_value,
        )


@dataclass(frozen=True)
class TableData:
    """An immutable, source-aware representation of a BDD data table.

    ``TableData`` intentionally provides only a few explicit operations. It is
    not a second table-processing framework. Its job is to carry current cell
    values and original source locations through the schema lifecycle.
    """

    rows: tuple[tuple[TableCell, ...], ...]

    @classmethod
    def from_rows(cls, rows: RawTable) -> TableData:
        """Wrap ordinary string rows while recording one-based locations."""
        return cls(
            rows=tuple(
                tuple(
                    TableCell.from_value(value, row=row_number, column=column_number)
                    for column_number, value in enumerate(row, start=1)
                )
                for row_number, row in enumerate(rows, start=1)
            )
        )

    @classmethod
    def from_cells(cls, rows: Sequence[Sequence[TableCell]]) -> TableData:
        """Build a table from cells whose source information already exists.

        Custom transformers use this constructor after arranging existing or
        transformed cells into their new logical table shape.
        """
        return cls(rows=tuple(tuple(row) for row in rows))

    @classmethod
    def ensure(cls, table: RawTable | TableData) -> TableData:
        """Return ``table`` unchanged or convert raw string rows into cells."""
        if isinstance(table, cls):
            return table
        return cls.from_rows(cast(RawTable, table))

    def cell(self, row: int, column: int) -> TableCell:
        """Return a cell using one-based row and column indexes.

        One-based indexes match the coordinates shown in BDD table errors and
        make transformer code easier to compare with a feature file.
        """
        if row < 1 or column < 1:
            raise IndexError("TableData cell indexes start at 1")
        try:
            return self.rows[row - 1][column - 1]
        except IndexError as exc:
            message = f"No table cell exists at row {row}, column {column}"
            raise IndexError(message) from exc

    def to_rows(self) -> list[list[str]]:
        """Return the current table values as ordinary mutable string rows."""
        return [[cell.value for cell in row] for row in self.rows]
