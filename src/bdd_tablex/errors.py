"""Errors with BDD-table location details."""

from __future__ import annotations

from collections.abc import Iterator
from enum import Enum
from typing import Any

from .table import TableCell

_UNSET = object()


class BDDTableErrorCode(str, Enum):
    """Stable machine-readable categories for table failures.

    Human-readable messages may improve over time. Integrations should use
    these codes when grouping diagnostics or deciding how to present them.
    """

    TABLE_ERROR = "table_error"
    SCHEMA_DEFINITION = "schema_definition"
    INVALID_CONTEXT = "invalid_context"
    TABLE_EMPTY = "table_empty"
    HEADER_EMPTY = "header_empty"
    RAGGED_ROW = "ragged_row"
    DUPLICATE_LABEL = "duplicate_label"
    UNKNOWN_FIELD = "unknown_field"
    MISSING_REQUIRED = "missing_required"
    EMPTY_REQUIRED = "empty_required"
    DEFAULT_FACTORY_FAILED = "default_factory_failed"
    PARSER_FAILED = "parser_failed"
    TRANSFORM_FAILED = "transform_failed"
    INVALID_TRANSFORM = "invalid_transform"
    UNKNOWN_VARIANT = "unknown_variant"
    INAPPLICABLE_FIELD = "inapplicable_field"
    DUPLICATE_ID = "duplicate_id"
    REFERENCE_FAILED = "reference_failed"
    RECORD_VALIDATION_FAILED = "record_validation_failed"
    TABLE_VALIDATION_FAILED = "table_validation_failed"
    OUTPUT_FAILED = "output_failed"


class BDDTableError(ValueError):
    """Raised when a table cannot be transformed or parsed by its schema.

    The structured attributes are intentionally public. Test runners and
    editor integrations can inspect them without parsing the human-readable
    error message.
    """

    def __init__(
        self,
        message: str,
        *,
        schema: type | str | None = None,
        field: str | None = None,
        row: int | None = None,
        column: int | None = None,
        item_id: Any | None = None,
        value: Any = _UNSET,
        code: BDDTableErrorCode | str = BDDTableErrorCode.TABLE_ERROR,
        hint: str | None = None,
    ) -> None:
        self.message = message
        if isinstance(schema, type):
            self.schema = schema.__dict__.get(
                "__schema_display_name__", schema.__name__
            )
        else:
            self.schema = schema
        self.field = field
        self.row = row
        self.column = column
        self.item_id = item_id
        self.value = value
        self.code = code.value if isinstance(code, BDDTableErrorCode) else str(code)
        self.hint = hint
        super().__init__(self.__str__())

    @classmethod
    def from_cell(
        cls,
        message: str,
        cell: TableCell,
        *,
        schema: type | str | None = None,
        field: str | None = None,
        item_id: Any | None = None,
        code: BDDTableErrorCode | str = BDDTableErrorCode.TABLE_ERROR,
        hint: str | None = None,
    ) -> BDDTableError:
        """Create an error located at a cell's original feature-file source.

        This helper is useful inside custom table transformations. It reports
        the source syntax, not merely the current transformed value.
        """
        return cls(
            message,
            schema=schema,
            field=field,
            row=cell.source_row,
            column=cell.source_column,
            item_id=item_id,
            value=cell.source_value,
            code=code,
            hint=hint,
        )

    def __str__(self) -> str:
        details = []
        details.append(f"code={self.code}")
        if self.schema is not None:
            details.append(f"schema={self.schema}")
        if self.field is not None:
            details.append(f"field={self.field!r}")
        if self.row is not None:
            details.append(f"row={self.row}")
        if self.column is not None:
            details.append(f"column={self.column}")
        if self.item_id is not None:
            details.append(f"item_id={self.item_id!r}")
        if self.value is not _UNSET:
            details.append(f"value={self.value!r}")
        location = f" ({', '.join(details)})" if details else ""
        hint = f". Hint: {self.hint}" if self.hint else ""
        return f"{self.message}{location}{hint}"

    @property
    def has_value(self) -> bool:
        """Return whether the diagnostic points to a concrete offending value."""
        return self.value is not _UNSET


class BDDTableErrors(ValueError):
    """Raised when collect mode finds several independent table failures.

    The contained errors retain their normal structured attributes and source
    locations. The aggregate itself is intentionally small so test runners,
    editor extensions, and command-line tools can render diagnostics in the
    format most useful to their users.
    """

    def __init__(self, errors: list[BDDTableError] | tuple[BDDTableError, ...]):
        if not errors:
            raise ValueError("BDDTableErrors requires at least one error")
        self.errors = tuple(errors)
        super().__init__(self.__str__())

    def __iter__(self) -> Iterator[BDDTableError]:
        """Iterate over individual diagnostics in discovery order."""
        return iter(self.errors)

    def __len__(self) -> int:
        """Return the number of collected diagnostics."""
        return len(self.errors)

    def __str__(self) -> str:
        lines = [f"BDD table contains {len(self.errors)} errors:"]
        lines.extend(
            f"  {index}. {error}" for index, error in enumerate(self.errors, 1)
        )
        return "\n".join(lines)


class SchemaDefinitionError(ValueError):
    """Raised immediately when a schema declaration is internally ambiguous."""

    def __init__(self, message: str, *, schema: str | None = None) -> None:
        self.message = message
        self.schema = schema
        detail = f" (schema={schema})" if schema else ""
        super().__init__(f"{message}{detail}")
