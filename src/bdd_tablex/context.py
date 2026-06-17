"""Context objects passed through table and cell parsing."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, cast


@dataclass(frozen=True)
class ParseContext:
    """Project-owned dependencies and settings for one parse operation.

    The library copies the supplied mapping and exposes it as read-only
    ``user_data``. Cell parsers, table transformers, and record validators all
    receive data originating from this same context object.
    """

    user_data: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    @classmethod
    def from_value(cls, value: Mapping[str, Any] | ParseContext | None) -> ParseContext:
        """Normalize a mapping, existing context, or ``None``."""
        if value is None:
            return cls()
        if isinstance(value, cls):
            return value
        return cls(user_data=MappingProxyType(dict(cast(Mapping[str, Any], value))))


@dataclass(frozen=True)
class CellContext:
    """Source location and project data supplied to a field parser.

    ``value`` is passed separately to a field parser and represents the
    current, possibly transformed value. ``source_value`` records what was
    written in the original BDD table before table transformation.
    """

    schema: type
    field_name: str
    field_label: str
    row: int | None
    column: int | None
    item_id: Any | None
    source_value: str
    user_data: Mapping[str, Any]


@dataclass(frozen=True)
class DefaultContext:
    """Context supplied when a missing optional field uses a factory.

    Default factories do not have a source cell because the field was omitted
    from the BDD table. They still receive the selected schema, field identity,
    item ID when available, and the same read-only project data supplied to the
    parse operation.
    """

    schema: type
    field_name: str
    field_label: str
    item_id: Any | None
    user_data: Mapping[str, Any]
