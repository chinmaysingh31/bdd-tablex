"""Schemas used by the command-line tooling example."""

from bdd_tablex import RowTable, field


class UserTable(RowTable):
    """A small schema with one required field and one inferred integer field."""

    name = field("name", required=True)
    age: int = field("age")
