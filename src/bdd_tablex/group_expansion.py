"""Declarative expansion helpers for grouped column-oriented BDD tables.

The helpers in this module cover a common table shape: the first row contains
one key or ID cell per source group, and every other row contains one value for
that same group. A key cell may expand into several logical item columns. The
corresponding value cells are then repeated or copied across those columns.

The package supplies reusable mechanics and a few explicit rule objects. It
does not require these conventions. Projects can provide their own range and
repeat rules, or bypass this layer by overriding ``transform_table()``.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from .context import ParseContext
from .errors import BDDTableError
from .table import TableCell, TableData


class RangeRule(Protocol):
    """Contract for turning one key cell into one or more logical keys."""

    def expand(self, cell: TableCell, context: ParseContext) -> Sequence[TableCell]:
        """Return logical key cells derived from ``cell``.

        A value that does not use the rule's special syntax should normally
        return ``[cell]``. Invalid recognized syntax may raise ``ValueError``;
        ``ColumnGroupExpander`` converts it into a source-aware
        ``BDDTableError``.
        """


class RepeatRule(Protocol):
    """Contract for spreading one value cell across a logical key group."""

    def expand(
        self,
        cell: TableCell,
        expected_count: int,
        context: ParseContext,
    ) -> Sequence[TableCell]:
        """Return exactly ``expected_count`` logical value cells.

        A value without repeat syntax should normally be copied across the
        group. Invalid recognized syntax may raise ``ValueError``.
        """


def _validate_separator(separator: str, rule_name: str) -> None:
    """Reject empty separators, which would make syntax recognition ambiguous."""
    if not separator:
        raise ValueError(f"{rule_name} separator cannot be empty")


@dataclass(frozen=True)
class NumericRange:
    """Expand inclusive ascending integer ranges such as ``1..4``.

    Values without the configured separator are treated as one literal key.
    Once the separator is present, both endpoints must be integers and the
    first endpoint must not exceed the second.
    """

    separator: str = ".."

    def __post_init__(self) -> None:
        _validate_separator(self.separator, type(self).__name__)

    def expand(self, cell: TableCell, context: ParseContext) -> list[TableCell]:
        """Return one literal key or an inclusive sequence of integer keys."""
        if self.separator not in cell.value:
            return [cell]

        parts = cell.value.split(self.separator)
        if len(parts) != 2:
            raise ValueError(f"Invalid numeric range {cell.value!r}")

        try:
            start, end = (int(part) for part in parts)
        except ValueError as exc:
            raise ValueError(f"Invalid numeric range {cell.value!r}") from exc

        if start > end:
            raise ValueError("Numeric range must be ascending")

        return [cell.with_value(str(value)) for value in range(start, end + 1)]


@dataclass(frozen=True)
class AlphabeticRange:
    """Expand inclusive ASCII letter ranges such as ``A-D`` or ``a-d``.

    Endpoints must each be one ASCII letter and use the same case. Values
    without the configured separator remain literal keys.
    """

    separator: str = "-"

    def __post_init__(self) -> None:
        _validate_separator(self.separator, type(self).__name__)

    def expand(self, cell: TableCell, context: ParseContext) -> list[TableCell]:
        """Return one literal key or an inclusive sequence of letter keys."""
        if self.separator not in cell.value:
            return [cell]

        parts = cell.value.split(self.separator)
        valid_endpoints = all(
            len(part) == 1 and part.isascii() and part.isalpha() for part in parts
        )
        valid = (
            len(parts) == 2
            and valid_endpoints
            and parts[0].isupper() == parts[1].isupper()
        )
        if not valid:
            raise ValueError(f"Invalid alphabetic range {cell.value!r}")

        start, end = (ord(part) for part in parts)
        if start > end:
            raise ValueError("Alphabetic range must be ascending")

        return [cell.with_value(chr(value)) for value in range(start, end + 1)]


@dataclass(frozen=True)
class PrefixRepeat:
    """Expand count-before-value syntax such as ``3:Article``.

    If the text before the separator is not an integer, the entire value is
    treated as a literal and copied across the key group. This allows normal
    text containing the separator, such as ``News: Europe``, to remain valid.
    """

    separator: str = ":"

    def __post_init__(self) -> None:
        _validate_separator(self.separator, type(self).__name__)

    def expand(
        self,
        cell: TableCell,
        expected_count: int,
        context: ParseContext,
    ) -> list[TableCell]:
        """Repeat recognized syntax or copy a literal value across the group."""
        count_text, separator, value = cell.value.partition(self.separator)
        if not separator or not count_text.isdigit():
            return [cell] * expected_count
        if not value:
            raise ValueError("Repeated value cannot be empty")

        declared_count = int(count_text)
        if declared_count != expected_count:
            raise ValueError(
                f"Repeat count {declared_count} does not match "
                f"group size {expected_count}"
            )

        return [cell.with_value(value) for _ in range(declared_count)]


@dataclass(frozen=True)
class SuffixRepeat:
    """Expand value-before-count syntax such as ``Article x3``.

    If the text after the final separator is not an integer, the entire value
    is treated as a literal and copied across the key group.
    """

    separator: str = " x"

    def __post_init__(self) -> None:
        _validate_separator(self.separator, type(self).__name__)

    def expand(
        self,
        cell: TableCell,
        expected_count: int,
        context: ParseContext,
    ) -> list[TableCell]:
        """Repeat recognized syntax or copy a literal value across the group."""
        value, separator, count_text = cell.value.rpartition(self.separator)
        if not separator or not count_text.isdigit():
            return [cell] * expected_count
        if not value:
            raise ValueError("Repeated value cannot be empty")

        declared_count = int(count_text)
        if declared_count != expected_count:
            raise ValueError(
                f"Repeat count {declared_count} does not match "
                f"group size {expected_count}"
            )

        return [cell.with_value(value) for _ in range(declared_count)]


@dataclass(frozen=True)
class ColumnGroupExpander:
    """Expand grouped columns using replaceable range and repeat rules.

    Args:
        key_row: Literal label expected in the first cell of the first row.
        range_rule: Object implementing :class:`RangeRule`.
        repeat_rule: Object implementing :class:`RepeatRule`.

    The expander owns the repetitive table mechanics: rectangular-shape
    checks, group iteration, source preservation, count validation, and
    ``TableData`` construction. Rule objects own syntax recognition and value
    expansion.

    """

    key_row: str
    range_rule: RangeRule
    repeat_rule: RepeatRule

    def transform(
        self,
        table: TableData,
        context: ParseContext,
        *,
        schema: type | str | None = None,
    ) -> TableData:
        """Return an expanded logical table ready for normal schema parsing."""
        if not table.rows or not table.rows[0]:
            raise BDDTableError("Grouped table is empty", schema=schema)

        source_width = len(table.rows[0])
        for row_number, row in enumerate(table.rows, start=1):
            if len(row) == source_width:
                continue
            if row:
                raise BDDTableError.from_cell(
                    "Column group expansion requires a rectangular table",
                    row[0],
                    schema=schema,
                )
            raise BDDTableError(
                "Column group expansion requires a rectangular table",
                schema=schema,
                row=row_number,
            )

        key_label = table.rows[0][0]
        if key_label.value != self.key_row:
            raise BDDTableError.from_cell(
                f"Expected key row {self.key_row!r}",
                key_label,
                schema=schema,
            )

        expanded_rows: list[list[TableCell]] = [[row[0]] for row in table.rows]
        for source_column in range(1, source_width):
            key_cell = table.rows[0][source_column]
            key_cells = self._expand_range(key_cell, context, schema)
            if not key_cells:
                raise BDDTableError.from_cell(
                    "Range rule produced no keys",
                    key_cell,
                    schema=schema,
                )
            expanded_rows[0].extend(key_cells)

            for row_index in range(1, len(table.rows)):
                value_cell = table.rows[row_index][source_column]
                value_cells = self._expand_repeat(
                    value_cell,
                    len(key_cells),
                    context,
                    schema,
                )
                if len(value_cells) != len(key_cells):
                    raise BDDTableError.from_cell(
                        f"Repeat rule produced {len(value_cells)} values for "
                        f"a group of {len(key_cells)} keys",
                        value_cell,
                        schema=schema,
                    )
                expanded_rows[row_index].extend(value_cells)

        return TableData.from_cells(expanded_rows)

    def _expand_range(
        self,
        cell: TableCell,
        context: ParseContext,
        schema: type | str | None,
    ) -> list[TableCell]:
        """Run a range rule and normalize its errors and return value."""
        try:
            cells = list(self.range_rule.expand(cell, context))
        except BDDTableError:
            raise
        except Exception as exc:
            raise BDDTableError.from_cell(
                f"Range expansion failed: {exc}",
                cell,
                schema=schema,
            ) from exc
        self._require_cells(cells, cell, "Range", schema)
        return cells

    def _expand_repeat(
        self,
        cell: TableCell,
        expected_count: int,
        context: ParseContext,
        schema: type | str | None,
    ) -> list[TableCell]:
        """Run a repeat rule and normalize its errors and return value."""
        try:
            cells = list(self.repeat_rule.expand(cell, expected_count, context))
        except BDDTableError:
            raise
        except Exception as exc:
            raise BDDTableError.from_cell(
                f"Repeat expansion failed: {exc}",
                cell,
                schema=schema,
            ) from exc
        self._require_cells(cells, cell, "Repeat", schema)
        return cells

    @staticmethod
    def _require_cells(
        cells: Sequence[object],
        source: TableCell,
        rule_name: str,
        schema: type | str | None,
    ) -> None:
        """Ensure custom rules return TableCell instances."""
        if all(isinstance(cell, TableCell) for cell in cells):
            return
        raise BDDTableError.from_cell(
            f"{rule_name} rule must return TableCell values",
            source,
            schema=schema,
        )
