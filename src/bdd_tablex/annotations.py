"""Parser inference for supported Python type annotations."""

from __future__ import annotations

import types
from decimal import Decimal
from enum import Enum
from typing import Any, Literal, Union, get_args, get_origin

from .fields import Parser
from .parsers import boolean, compose, decimal, each, floating, integer, optional, split


def parser_for_annotation(annotation: Any) -> Parser | None:
    """Return a parser for one supported annotation or ``None`` for raw text.

    Supported annotations are ``str``, ``int``, ``float``, ``bool``,
    ``Decimal``, enums, ``Literal`` strings, ``list[T]``, and an optional form
    containing exactly one non-``None`` type. Explicit field parsers always
    take precedence over inference.
    """
    if annotation in (Any, str):
        return None
    if annotation is int:
        return integer()
    if annotation is float:
        return floating()
    if annotation is bool:
        return boolean()
    if annotation is Decimal:
        return decimal()
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return _enum_parser(annotation)

    origin = get_origin(annotation)
    arguments = get_args(annotation)
    if origin in (Union, types.UnionType):
        non_none = [argument for argument in arguments if argument is not type(None)]
        if len(non_none) == 1 and len(non_none) != len(arguments):
            parser = parser_for_annotation(non_none[0]) or _identity
            return optional(parser)
        return None
    if origin is list and len(arguments) == 1:
        item_parser = parser_for_annotation(arguments[0]) or _identity
        return compose(split(","), each(item_parser))
    if (
        origin is Literal
        and arguments
        and all(isinstance(argument, str) for argument in arguments)
    ):
        allowed = tuple(arguments)

        def parse_literal(value: Any, context: Any) -> str:
            if value not in allowed:
                raise ValueError(f"Expected one of {list(allowed)!r}")
            return value

        return parse_literal
    return None


def _identity(value: Any, context: Any) -> Any:
    return value


def _enum_parser(enum_type: type[Enum]) -> Parser:
    """Match enum values first, then member names."""

    def parse(value: Any, context: Any) -> Enum:
        raw = str(value)
        for member in enum_type:
            if str(member.value) == raw or member.name == raw:
                return member
        choices = [str(member.value) for member in enum_type]
        raise ValueError(f"Expected one of {choices!r}")

    return parse
