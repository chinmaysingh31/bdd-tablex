"""Composable, project-owned cell parsing rules.

``CellDSL`` intentionally implements dispatch rather than domain syntax. A
project chooses its exact tokens, regular expressions, predicates, field
scopes, generated values, and fallback behavior.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any

from .context import CellContext

TokenHandler = Callable[[CellContext], Any]
PatternHandler = Callable[[re.Match[str], CellContext], Any]
Predicate = Callable[[str, CellContext], bool]
PredicateHandler = Callable[[str, CellContext], Any]
FallbackHandler = Callable[[str, CellContext], Any]


def _normalize_fields(fields: Iterable[str] | None) -> frozenset[str] | None:
    """Return an immutable field-name scope for one rule declaration."""
    if fields is None:
        return None
    if isinstance(fields, str):
        fields = (fields,)
    normalized = frozenset(fields)
    if not normalized or any(not field for field in normalized):
        raise ValueError("Cell DSL field scopes must contain field names")
    return normalized


def _applies(fields: frozenset[str] | None, context: CellContext) -> bool:
    """Return whether a rule is global or includes the current schema field."""
    return fields is None or context.field_name in fields


@dataclass(frozen=True)
class _TokenRule:
    value: str
    fields: frozenset[str] | None
    handler: TokenHandler


@dataclass(frozen=True)
class _PatternRule:
    source: str
    pattern: re.Pattern[str]
    fields: frozenset[str] | None
    handler: PatternHandler


@dataclass(frozen=True)
class _PredicateRule:
    predicate: Predicate
    fields: frozenset[str] | None
    handler: PredicateHandler


class CellDSL:
    """Dispatch cell values to project-defined parsing handlers.

    Dispatch order is exact tokens, regular-expression patterns, predicates,
    and finally the optional fallback. For an exact token, field-scoped rules
    take precedence over a global rule with the same value. Pattern and
    predicate rules otherwise retain registration order.
    """

    def __init__(self) -> None:
        self._tokens: list[_TokenRule] = []
        self._token_keys: set[tuple[str, frozenset[str] | None]] = set()
        self._patterns: list[_PatternRule] = []
        self._pattern_keys: set[tuple[str, frozenset[str] | None]] = set()
        self._predicates: list[_PredicateRule] = []
        self._fallback: FallbackHandler | None = None

    def token(
        self,
        value: str,
        *,
        fields: Iterable[str] | None = None,
    ) -> Callable[[TokenHandler], TokenHandler]:
        """Register an exact token, optionally for selected field names only."""
        if not value:
            raise ValueError("Cell DSL token cannot be empty")
        scope = _normalize_fields(fields)

        def register(handler: TokenHandler) -> TokenHandler:
            key = (value, scope)
            if key in self._token_keys:
                raise ValueError(
                    f"Cell DSL token {value!r} is already registered for this scope"
                )
            self._tokens.append(_TokenRule(value, scope, handler))
            self._token_keys.add(key)
            return handler

        return register

    def pattern(
        self,
        expression: str,
        *,
        fields: Iterable[str] | None = None,
    ) -> Callable[[PatternHandler], PatternHandler]:
        """Register a full-match regular expression and optional field scope."""
        compiled = re.compile(expression)
        scope = _normalize_fields(fields)

        def register(handler: PatternHandler) -> PatternHandler:
            key = (expression, scope)
            if key in self._pattern_keys:
                raise ValueError(
                    f"Cell DSL pattern {expression!r} is already registered "
                    "for this scope"
                )
            self._patterns.append(_PatternRule(expression, compiled, scope, handler))
            self._pattern_keys.add(key)
            return handler

        return register

    def when(
        self,
        predicate: Predicate,
        *,
        fields: Iterable[str] | None = None,
    ) -> Callable[[PredicateHandler], PredicateHandler]:
        """Register a project predicate for syntax that is awkward as regex.

        Predicates run after exact tokens and regular expressions. They should
        return a boolean and avoid side effects because only the handler's
        return value becomes the parsed cell value.
        """
        scope = _normalize_fields(fields)

        def register(handler: PredicateHandler) -> PredicateHandler:
            self._predicates.append(_PredicateRule(predicate, scope, handler))
            return handler

        return register

    def fallback(self, handler: FallbackHandler) -> FallbackHandler:
        """Register behavior for values that match no explicit rule."""
        if self._fallback is not None:
            raise ValueError("Cell DSL fallback is already registered")
        self._fallback = handler
        return handler

    def compose(self, *others: CellDSL) -> CellDSLChain:
        """Return a first-match chain beginning with this DSL."""
        return CellDSLChain((self, *others))

    def _dispatch(self, value: str, context: CellContext) -> tuple[bool, Any]:
        """Return ``(matched, result)`` for composition-aware dispatch."""
        token_rules = [rule for rule in self._tokens if rule.value == value]
        token_rules.sort(key=lambda rule: rule.fields is None)
        for token_rule in token_rules:
            if _applies(token_rule.fields, context):
                return True, token_rule.handler(context)

        for pattern_rule in self._patterns:
            if not _applies(pattern_rule.fields, context):
                continue
            match = pattern_rule.pattern.fullmatch(value)
            if match is not None:
                return True, pattern_rule.handler(match, context)

        for predicate_rule in self._predicates:
            if _applies(predicate_rule.fields, context) and predicate_rule.predicate(
                value, context
            ):
                return True, predicate_rule.handler(value, context)

        if self._fallback is not None:
            return True, self._fallback(value, context)
        return False, value

    def __call__(self, value: str, context: CellContext) -> Any:
        """Parse one value or pass it through when no rule matches."""
        _, result = self._dispatch(value, context)
        return result


class CellDSLChain:
    """A parser that asks several ``CellDSL`` objects in first-match order."""

    def __init__(self, dsls: Sequence[CellDSL]) -> None:
        if not dsls:
            raise ValueError("CellDSLChain requires at least one DSL")
        if not all(isinstance(dsl, CellDSL) for dsl in dsls):
            raise TypeError("CellDSLChain accepts only CellDSL instances")
        self.dsls = tuple(dsls)

    def __call__(self, value: str, context: CellContext) -> Any:
        """Return the result from the first composed DSL that matches."""
        for dsl in self.dsls:
            matched, result = dsl._dispatch(value, context)
            if matched:
                return result
        return value


def compose_cell_dsls(*dsls: CellDSL) -> CellDSLChain:
    """Compose reusable and project-specific cell grammars in priority order."""
    return CellDSLChain(dsls)
