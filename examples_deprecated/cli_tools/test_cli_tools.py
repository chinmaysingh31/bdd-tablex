"""Executable examples for the bdd-tablex command-line tools."""

from __future__ import annotations

import json
from pathlib import Path

from bdd_tablex.cli import main

HERE = Path(__file__).parent
FEATURE = HERE / "users.feature"
SCHEMA = f"{HERE / 'schemas.py'}:UserTable"


def test_cli_check_can_emit_json_diagnostics(capsys):
    """Validate a feature table and read structured diagnostics as JSON."""
    exit_code = main(
        [
            "check",
            str(FEATURE),
            "--schema",
            SCHEMA,
            "--step",
            "the following CLI users:",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload["status"] == "failed"
    assert [error["code"] for error in payload["diagnostics"]] == [
        "empty_required",
        "parser_failed",
    ]
    assert payload["diagnostics"][0]["hint"]


def test_cli_describe_prints_a_schema_contract(capsys):
    """Inspect the fields and policies a schema exposes to feature authors."""
    exit_code = main(["describe", SCHEMA])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Schema: UserTable" in output
    assert "Orientation: row" in output
    assert "name: label='name'" in output


def test_cli_describe_can_emit_json(capsys):
    """Use JSON schema contracts for documentation or editor tooling."""
    exit_code = main(["describe", SCHEMA, "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["schema_name"] == "UserTable"
    assert [field["name"] for field in payload["fields"]] == ["name", "age"]
