"""Reusable field parsers and small parser-composition helpers.

Every parser follows the same callable contract used by ``field(parser=...)``:
it accepts the current value and a :class:`~bdd_tablex.CellContext`. Parser
factories return plain callable objects, so projects can use them directly,
compose them, or mix them with custom functions.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from .context import CellContext
from .fields import Parser


def string(*, strip: bool = False, lower: bool = False, upper: bool = False) -> Parser:
    """Return a parser that normalizes text without inventing other semantics."""
    if lower and upper:
        raise ValueError("string parser cannot enable both lower and upper")

    def parse(value: Any, context: CellContext) -> str:
        result = str(value)
        if strip:
            result = result.strip()
        if lower:
            result = result.lower()
        if upper:
            result = result.upper()
        return result

    return parse


def integer(*, base: int = 10) -> Parser:
    """Return a parser that converts text to ``int`` using the selected base."""

    def parse(value: Any, context: CellContext) -> int:
        return int(value, base) if isinstance(value, str) else int(value)

    return parse


def floating() -> Parser:
    """Return a parser that converts a value to ``float``."""

    def parse(value: Any, context: CellContext) -> float:
        return float(value)

    return parse


def decimal() -> Parser:
    """Return a parser that converts through text to an exact ``Decimal``."""

    def parse(value: Any, context: CellContext) -> Decimal:
        return Decimal(str(value))

    return parse


def boolean(
    *,
    true_values: Iterable[str] = ("true", "yes", "1", "on"),
    false_values: Iterable[str] = ("false", "no", "0", "off"),
    case_sensitive: bool = False,
) -> Parser:
    """Return a strict boolean parser with configurable accepted tokens."""
    normalize = (lambda value: value) if case_sensitive else str.lower
    accepted_true = {normalize(str(value)) for value in true_values}
    accepted_false = {normalize(str(value)) for value in false_values}
    overlap = accepted_true & accepted_false
    if overlap:
        raise ValueError(f"Boolean true and false values overlap: {sorted(overlap)!r}")

    def parse(value: Any, context: CellContext) -> bool:
        normalized = normalize(str(value))
        if normalized in accepted_true:
            return True
        if normalized in accepted_false:
            return False
        accepted = sorted(accepted_true | accepted_false)
        raise ValueError(f"Expected one of {accepted!r}")

    return parse


def choice(*values: str, case_sensitive: bool = True) -> Parser:
    """Return a parser that validates and returns one allowed string value."""
    if not values:
        raise ValueError("choice parser requires at least one allowed value")
    if case_sensitive:
        accepted = {value: value for value in values}
    else:
        accepted = {value.lower(): value for value in values}

    def parse(value: Any, context: CellContext) -> str:
        raw = str(value)
        key = raw if case_sensitive else raw.lower()
        if key not in accepted:
            raise ValueError(f"Expected one of {list(values)!r}")
        return accepted[key]

    return parse


def split(
    separator: str = ",",
    *,
    strip_items: bool = True,
    keep_empty: bool = False,
) -> Parser:
    """Return a parser that splits one cell into a list of strings."""
    if not separator:
        raise ValueError("split separator cannot be empty")

    def parse(value: Any, context: CellContext) -> list[str]:
        items = str(value).split(separator)
        if strip_items:
            items = [item.strip() for item in items]
        if not keep_empty:
            items = [item for item in items if item != ""]
        return items

    return parse


def map_value(values: Mapping[str, Any], *, case_sensitive: bool = True) -> Parser:
    """Return a parser that maps known cell strings to arbitrary Python values."""
    mapping = dict(values)
    if not case_sensitive:
        mapping = {str(key).lower(): value for key, value in mapping.items()}

    def parse(value: Any, context: CellContext) -> Any:
        raw = str(value)
        key = raw if case_sensitive else raw.lower()
        if key not in mapping:
            raise ValueError(f"No mapped value for {raw!r}")
        return mapping[key]

    return parse


def compose(*parsers: Parser) -> Parser:
    """Run parsers left-to-right, passing each result to the next parser."""
    if not parsers:
        raise ValueError("compose requires at least one parser")

    def parse(value: Any, context: CellContext) -> Any:
        result = value
        for parser in parsers:
            result = parser(result, context)
        return result

    return parse


def each(parser: Parser) -> Parser:
    """Apply one parser to every value produced by an earlier parser."""

    def parse(values: Any, context: CellContext) -> list[Any]:
        if isinstance(values, (str, bytes)) or not isinstance(values, Iterable):
            raise ValueError("each parser expects a non-string iterable")
        return [parser(value, context) for value in values]

    return parse


@dataclass(frozen=True)
class _OptionalParser:
    parser: Parser
    none_values: frozenset[str]
    case_sensitive: bool
    parse_empty: bool = True

    def __call__(self, value: Any, context: CellContext) -> Any:
        raw = str(value)
        normalized = raw if self.case_sensitive else raw.lower()
        if raw == "" or normalized in self.none_values:
            return None
        return self.parser(value, context)


def optional(
    parser: Parser,
    *,
    none_values: Iterable[str] = ("none", "null"),
    case_sensitive: bool = False,
) -> Parser:
    """Return a parser that maps empty/null tokens to ``None`` first."""
    normalize = (lambda value: value) if case_sensitive else str.lower
    normalized = frozenset(normalize(str(value)) for value in none_values)
    return _OptionalParser(parser, normalized, case_sensitive)
