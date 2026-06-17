"""Lightweight typed records produced from table schemas."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Any, ClassVar

from .fields import Field
from .sources import RecordSource


class TableRecord:
    """Lightweight schema record created before optional model conversion."""

    __fields__: ClassVar[dict[str, Field]] = {}
    _table_source: RecordSource
    _table_extras: Mapping[str, Any]

    @classmethod
    def _from_values(
        cls,
        values: dict[str, Any],
        *,
        source: RecordSource | None = None,
        extras: Mapping[str, Any] | None = None,
    ) -> TableRecord:
        """Construct a schema record without invoking a user initializer."""
        record = cls.__new__(cls)
        for name in cls.__fields__:
            setattr(record, name, values[name])
        record._table_source = source or RecordSource.create()
        record._table_extras = MappingProxyType(dict(extras or {}))
        return record

    @property
    def table_source(self) -> RecordSource:
        """Return immutable source metadata for this parsed record."""
        return self._table_source

    def source_for(self, field_name: str) -> Any:
        """Return the original ``TableCell`` for one schema attribute."""
        return self.table_source.source_for(field_name)

    @property
    def table_extras(self) -> Mapping[str, Any]:
        """Return unknown or inapplicable values preserved by schema policy."""
        return self._table_extras

    def as_dict(self) -> dict[str, Any]:
        """Return declared schema fields as a new ordinary dictionary."""
        return {name: getattr(self, name) for name in self.__fields__}

    def __repr__(self) -> str:
        values = ", ".join(
            f"{name}={getattr(self, name)!r}" for name in self.__fields__
        )
        return f"{type(self).__name__}({values})"

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self.as_dict() == other.as_dict()
