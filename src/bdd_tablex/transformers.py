"""Composition utilities for source-aware table transformations."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from .context import ParseContext
from .errors import BDDTableError, BDDTableErrorCode
from .table import TableData


class TableTransformer(Protocol):
    """Structural contract implemented by reusable table transformers."""

    def transform(
        self,
        table: TableData,
        context: ParseContext,
        *,
        schema: type | str | None = None,
    ) -> TableData:
        """Return a source-aware table for the next transformation stage."""


class TransformerPipeline:
    """Run table transformers from left to right.

    Each stage receives the previous stage's ``TableData`` and the same parse
    context. Unexpected failures identify the stage, while intentional
    ``BDDTableError`` diagnostics pass through unchanged.
    """

    def __init__(self, transformers: Sequence[TableTransformer]) -> None:
        if not transformers:
            raise ValueError("TransformerPipeline requires at least one transformer")
        for transformer in transformers:
            if not callable(getattr(transformer, "transform", None)):
                raise TypeError("Table transformers must provide transform()")
        self.transformers = tuple(transformers)

    def transform(
        self,
        table: TableData,
        context: ParseContext,
        *,
        schema: type | str | None = None,
    ) -> TableData:
        """Apply every configured transformer and validate each result."""
        current = table
        for index, transformer in enumerate(self.transformers, start=1):
            stage_name = type(transformer).__name__
            try:
                current = transformer.transform(current, context, schema=schema)
            except BDDTableError:
                raise
            except Exception as exc:
                raise BDDTableError(
                    f"Table transformer stage {index} ({stage_name}) failed: {exc}",
                    schema=schema,
                    code=BDDTableErrorCode.TRANSFORM_FAILED,
                ) from exc
            if not isinstance(current, TableData):
                raise BDDTableError(
                    f"Table transformer stage {index} ({stage_name}) must return "
                    "TableData",
                    schema=schema,
                    code=BDDTableErrorCode.INVALID_TRANSFORM,
                )
        return current


def compose_transformers(*transformers: TableTransformer) -> TransformerPipeline:
    """Create a reusable left-to-right table transformation pipeline."""
    return TransformerPipeline(transformers)
