"""Schema field declarations."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from .context import CellContext, DefaultContext

MISSING = object()
Parser = Callable[[Any, CellContext], Any]
DefaultFactory = Callable[[DefaultContext], Any]


@dataclass(frozen=True)
class ReferenceSpec:
    """Configuration for resolving local IDs to records in the same table."""

    target: str
    many: bool
    separator: str


@dataclass
class Field:
    """One declared schema field and its conversion behavior."""

    label: str
    aliases: tuple[str, ...] = ()
    required: bool = False
    default: Any = MISSING
    default_factory: DefaultFactory | object = MISSING
    parser: Parser | None = None
    parse_empty: bool = False
    is_id: bool = False
    is_discriminator: bool = False
    variants: Mapping[Any, type] | None = None
    reference: ReferenceSpec | None = None
    name: str = ""

    def clone(self) -> Field:
        """Return an independent declaration for schema inheritance."""
        return Field(
            label=self.label,
            aliases=self.aliases,
            required=self.required,
            default=self.default,
            default_factory=self.default_factory,
            parser=self.parser,
            parse_empty=self.parse_empty,
            is_id=self.is_id,
            is_discriminator=self.is_discriminator,
            variants=self.variants,
            reference=self.reference,
            name=self.name,
        )

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object | None, owner: type | None = None) -> Any:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: Any) -> None:
        instance.__dict__[self.name] = value

    @property
    def labels(self) -> tuple[str, ...]:
        """Return the canonical label followed by accepted aliases."""
        return (self.label, *self.aliases)


def _validate_field_options(
    label: str,
    aliases: Sequence[str],
    *,
    required: bool,
    default: Any,
    default_factory: DefaultFactory | object,
) -> tuple[str, ...]:
    """Validate declaration options shared by all field constructors."""
    if not label:
        raise ValueError("field label cannot be empty")
    normalized = tuple(aliases)
    if any(not alias for alias in normalized):
        raise ValueError("field aliases cannot be empty")
    if label in normalized or len(set(normalized)) != len(normalized):
        raise ValueError("field aliases must be unique and differ from the label")
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("field cannot declare both default and default_factory")
    if required and (default is not MISSING or default_factory is not MISSING):
        raise ValueError("required fields cannot declare defaults")
    if default_factory is not MISSING and not callable(default_factory):
        raise TypeError("default_factory must be callable")
    return normalized


def field(
    label: str,
    *,
    required: bool = False,
    default: Any = MISSING,
    default_factory: DefaultFactory | object = MISSING,
    parser: Parser | None = None,
    aliases: Sequence[str] = (),
) -> Any:
    """Declare a row or column in a table schema.

    Parsers normally do not receive explicit empty cells, preserving the
    package distinction between an empty cell and a missing field. Parser
    objects may opt into empty-cell handling by exposing ``parse_empty=True``.
    """
    normalized_aliases = _validate_field_options(
        label,
        aliases,
        required=required,
        default=default,
        default_factory=default_factory,
    )
    return Field(
        label=label,
        aliases=normalized_aliases,
        required=required,
        default=default,
        default_factory=default_factory,
        parser=parser,
        parse_empty=bool(getattr(parser, "parse_empty", False)),
    )


def id_field(
    label: str,
    *,
    parser: Parser | None = None,
    aliases: Sequence[str] = (),
) -> Any:
    """Declare the item identifier row for a column-oriented table."""
    normalized_aliases = _validate_field_options(
        label,
        aliases,
        required=True,
        default=MISSING,
        default_factory=MISSING,
    )
    return Field(
        label=label,
        aliases=normalized_aliases,
        required=True,
        parser=parser,
        is_id=True,
    )


def discriminator_field(
    label: str,
    *,
    parser: Parser | None = None,
    aliases: Sequence[str] = (),
) -> Any:
    """Declare the field used to select a registered record variant.

    A discriminator is always required because the parser cannot choose a
    variant without it. The optional parser runs before variant lookup, so a
    project may register enum members or other typed values as variant keys.

    Declaring this field does not enable variants by itself. Register variant
    schema subclasses with ``@BaseSchema.variant(value)``.
    """
    normalized_aliases = _validate_field_options(
        label,
        aliases,
        required=True,
        default=MISSING,
        default_factory=MISSING,
    )
    return Field(
        label=label,
        aliases=normalized_aliases,
        required=True,
        parser=parser,
        is_discriminator=True,
    )


def discriminator(
    label: str,
    *,
    variants: Mapping[Any, type],
    parser: Parser | None = None,
    aliases: Sequence[str] = (),
) -> Any:
    """Declare a discriminator and its variant field components together.

    ``variants`` maps parsed discriminator values to ``TableFields``
    subclasses. When the containing table schema is created, bdd-tablex
    composes each component with that schema and registers the resulting
    record variant automatically.

    This is the concise alternative to ``discriminator_field()`` plus
    ``@Table.variant(value)`` classes. The explicit decorator form remains
    useful when a project prefers named variant schema classes.
    """
    if not isinstance(variants, Mapping):
        raise TypeError("discriminator variants must be a mapping")
    if not variants:
        raise ValueError("discriminator variants cannot be empty")
    normalized_aliases = _validate_field_options(
        label,
        aliases,
        required=True,
        default=MISSING,
        default_factory=MISSING,
    )
    return Field(
        label=label,
        aliases=normalized_aliases,
        required=True,
        parser=parser,
        is_discriminator=True,
        variants=MappingProxyType(dict(variants)),
    )


def reference(
    label: str,
    *,
    target: str = "id",
    many: bool = False,
    separator: str = ",",
    required: bool = False,
    default: Any = MISSING,
    aliases: Sequence[str] = (),
) -> Any:
    """Declare a local reference to another parsed record in the same table.

    The raw cell contains one target value, or a separator-delimited list when
    ``many=True``. Resolution occurs after all records are constructed and
    before validation hooks run.
    """
    if many and not separator:
        raise ValueError("reference separator cannot be empty")
    normalized_aliases = _validate_field_options(
        label,
        aliases,
        required=required,
        default=default,
        default_factory=MISSING,
    )
    return Field(
        label=label,
        aliases=normalized_aliases,
        required=required,
        default=default,
        reference=ReferenceSpec(target=target, many=many, separator=separator),
    )
