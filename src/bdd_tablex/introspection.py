"""Immutable, machine-readable descriptions of table schema contracts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .fields import MISSING, Field


def _callable_name(value: Any) -> str | None:
    """Return a stable best-effort name for a configured callable or object."""
    if value is None or value is MISSING:
        return None
    return getattr(
        value, "__qualname__", getattr(value, "__name__", type(value).__name__)
    )


@dataclass(frozen=True)
class FieldContract:
    """Public description of one declared schema field."""

    name: str
    label: str
    aliases: tuple[str, ...]
    required: bool
    is_id: bool
    is_discriminator: bool
    has_default: bool
    default_repr: str | None
    default_factory: str | None
    parser: str | None
    reference_target: str | None
    reference_many: bool

    @classmethod
    def from_field(cls, name: str, declared: Field) -> FieldContract:
        """Build an immutable contract from one internal field declaration."""
        reference = declared.reference
        return cls(
            name=name,
            label=declared.label,
            aliases=declared.aliases,
            required=declared.required,
            is_id=declared.is_id,
            is_discriminator=declared.is_discriminator,
            has_default=(
                declared.default is not MISSING
                or declared.default_factory is not MISSING
            ),
            default_repr=(
                repr(declared.default) if declared.default is not MISSING else None
            ),
            default_factory=_callable_name(declared.default_factory),
            parser=_callable_name(declared.parser),
            reference_target=reference.target if reference else None,
            reference_many=reference.many if reference else False,
        )


@dataclass(frozen=True)
class VariantContract:
    """Description of one discriminator value and selected schema contract."""

    value: Any
    schema_name: str
    fields: tuple[FieldContract, ...]
    output_model: str | None
    output_builder: str


@dataclass(frozen=True)
class TableContract:
    """Complete public description returned by ``Table.describe()``."""

    schema_name: str
    orientation: str
    fields: tuple[FieldContract, ...]
    variants: tuple[VariantContract, ...]
    unknown_fields: str
    inapplicable_fields: str
    transformer: str | None
    output_model: str | None
    output_builder: str

    def as_dict(self) -> dict[str, Any]:
        """Return a recursively structured dictionary for tooling and JSON."""
        return asdict(self)


def describe_schema(schema: Any) -> TableContract:
    """Inspect one table schema without parsing a feature table."""
    orientation = (
        "column"
        if any(base.__name__ == "ColumnTable" for base in schema.mro())
        else "row"
    )
    fields = tuple(
        FieldContract.from_field(name, declared)
        for name, declared in schema.__fields__.items()
    )
    variants = tuple(
        VariantContract(
            value=value,
            schema_name=variant.__dict__.get(
                "__schema_display_name__", variant.__name__
            ),
            fields=tuple(
                FieldContract.from_field(name, declared)
                for name, declared in variant.__fields__.items()
            ),
            output_model=_callable_name(variant.output_model),
            output_builder=_callable_name(variant.build_output) or "build_output",
        )
        for value, variant in schema.__variants__.items()
    )
    return TableContract(
        schema_name=schema.__dict__.get("__schema_display_name__", schema.__name__),
        orientation=orientation,
        fields=fields,
        variants=variants,
        unknown_fields=schema.unknown_fields,
        inapplicable_fields=schema.inapplicable_fields,
        transformer=_callable_name(schema.table_transformer),
        output_model=_callable_name(schema.output_model),
        output_builder=_callable_name(schema.build_output) or "build_output",
    )
