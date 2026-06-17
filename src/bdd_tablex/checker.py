"""Static validation of Gherkin data tables against bdd-tablex schemas.

The Gherkin dependency is imported lazily so normal runtime parsing remains
dependency-free. Install the ``cli`` extra when using feature-file discovery
or the ``bdd-tablex check`` command.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import BDDTableError, BDDTableErrors
from .schema import BaseTable
from .table import TableCell, TableData


@dataclass(frozen=True)
class FeatureTable:
    """One Gherkin step data table and its surrounding source identity."""

    path: Path
    feature: str
    scenario: str
    step: str
    table: TableData


@dataclass(frozen=True)
class FeatureDiagnostic:
    """One schema diagnostic associated with a feature file and step."""

    path: Path
    feature: str
    scenario: str
    step: str
    error: BDDTableError


def _gherkin_parser() -> Any:
    """Load the optional official Gherkin parser with an actionable message."""
    try:
        from gherkin.parser import Parser  # type: ignore[import-untyped]
    except ImportError as exc:
        raise RuntimeError(
            "Feature checking requires the 'cli' extra: pip install 'bdd-tablex[cli]'"
        ) from exc
    return Parser


def _table_data(data_table: Mapping[str, Any]) -> TableData:
    """Convert Gherkin AST cells while preserving feature-file coordinates."""
    rows = []
    for row in data_table["rows"]:
        cells = []
        for cell in row["cells"]:
            location = cell["location"]
            cells.append(
                TableCell(
                    value=cell["value"],
                    source_row=location["line"],
                    source_column=location["column"],
                    source_value=cell["value"],
                )
            )
        rows.append(cells)
    return TableData.from_cells(rows)


def _scenario_nodes(feature: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]:
    """Yield scenarios and backgrounds, including scenarios nested in rules."""
    for child in feature.get("children", []):
        if "scenario" in child:
            yield child["scenario"]
        elif "background" in child:
            yield child["background"]
        elif "rule" in child:
            yield from _scenario_nodes(child["rule"])


def discover_feature_tables(
    path: str | Path,
    *,
    step: str | None = None,
    scenario: str | None = None,
) -> list[FeatureTable]:
    """Return matching data tables parsed by the official Gherkin parser."""
    source_path = Path(path)
    Parser = _gherkin_parser()
    document = Parser().parse(source_path.read_text(encoding="utf-8"))
    feature = document.get("feature")
    if feature is None:
        return []

    discovered = []
    for scenario_node in _scenario_nodes(feature):
        scenario_name = scenario_node.get("name", "")
        if scenario is not None and scenario_name != scenario:
            continue
        for step_node in scenario_node.get("steps", []):
            data_table = step_node.get("dataTable")
            step_text = step_node.get("text", "")
            if data_table is None or (step is not None and step_text != step):
                continue
            discovered.append(
                FeatureTable(
                    path=source_path,
                    feature=feature.get("name", ""),
                    scenario=scenario_name,
                    step=step_text,
                    table=_table_data(data_table),
                )
            )
    return discovered


def check_feature(
    path: str | Path,
    *,
    schema: type[BaseTable],
    step: str | None = None,
    scenario: str | None = None,
    context: Mapping[str, Any] | None = None,
) -> list[FeatureDiagnostic]:
    """Validate matching feature tables without executing pytest scenarios.

    Custom parsers and validators still run. Projects whose schemas require
    services should supply deterministic checking dependencies through
    ``context`` or through the CLI's context-factory option.
    """
    diagnostics: list[FeatureDiagnostic] = []
    for discovered in discover_feature_tables(path, step=step, scenario=scenario):
        try:
            schema.parse(
                discovered.table,
                context=context,
                error_mode="collect",
            )
        except BDDTableErrors as exc:
            errors = exc.errors
        except BDDTableError as exc:
            errors = (exc,)
        else:
            errors = ()
        diagnostics.extend(
            FeatureDiagnostic(
                path=discovered.path,
                feature=discovered.feature,
                scenario=discovered.scenario,
                step=discovered.step,
                error=error,
            )
            for error in errors
        )
    return diagnostics
