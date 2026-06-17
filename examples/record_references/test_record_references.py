"""Executable example for local references between parsed records."""

import pytest
from pytest_bdd import given, scenario, then

from bdd_tablex import BDDTableError, ColumnTable, field, id_field, reference


class LinkedContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline", required=True)
    parent = reference("Parent")
    related = reference("Related", many=True)

    def validate_record(self, context):
        """References are resolved before record validation runs."""

        if self.parent is self:
            raise BDDTableError.from_cell(
                "Content cannot be its own parent",
                self.source_for("parent"),
                schema=type(self),
            )


@scenario("content.feature", "Resolve parent and related content IDs")
def test_record_references():
    pass


@given("the following linked content exists:", target_fixture="linked_content")
def linked_content(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=LinkedContentTable)


@then("local IDs resolve to content records")
def local_ids_resolve(linked_content):
    root, child, other = linked_content
    assert child.parent is root
    assert other.parent is root
    assert root.related == [child, other]
    assert other.related == [child]


def test_missing_target_reports_the_reference_cell():
    invalid_table = [
        ["IDs", "1", "2"],
        ["Headline", "Root", "Child"],
        ["Parent", "", "99"],
        ["Related", "", ""],
    ]

    with pytest.raises(BDDTableError, match="was not found") as error:
        LinkedContentTable.parse(invalid_table)

    assert error.value.row == 3
    assert error.value.column == 3
    assert error.value.item_id == "2"
