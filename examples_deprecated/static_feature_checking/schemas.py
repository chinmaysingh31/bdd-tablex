"""Schemas imported by the static feature-checking example and CLI."""

from bdd_tablex import RowTable, field


class CheckedUserTable(RowTable):
    """Contract used without running a pytest-bdd scenario."""

    name = field("name", required=True)
    age: int = field("age")
