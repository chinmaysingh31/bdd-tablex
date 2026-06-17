import pytest

from bdd_tablex import (
    BDDTableError,
    ColumnTable,
    RowTable,
    SchemaDefinitionError,
    TableFields,
    discriminator,
    field,
    id_field,
)


def test_default_factory_receives_item_and_project_context():
    seen = []

    def generated(context):
        seen.append(context)
        return f"generated-{context.item_id}-{context.user_data['suffix']}"

    class ContentTable(ColumnTable):
        id = id_field("IDs")
        headline = field("Headline", default_factory=generated)

    items = ContentTable.parse([["IDs", "7"]], context={"suffix": "qa"})

    assert items[0].headline == "generated-7-qa"
    assert seen[0].field_name == "headline"
    assert seen[0].field_label == "Headline"


def test_default_factory_failure_has_structured_error_code():
    def broken(context):
        raise RuntimeError("generator unavailable")

    class ContentTable(RowTable):
        headline = field("headline", default_factory=broken)

    with pytest.raises(BDDTableError) as error:
        ContentTable.parse([["other"], ["value"]])

    assert error.value.code == "unknown_field"

    class PermissiveContentTable(RowTable):
        unknown_fields = "ignore"
        headline = field("headline", default_factory=broken)

    with pytest.raises(BDDTableError, match="generator unavailable") as error:
        PermissiveContentTable.parse([["other"], ["value"]])

    assert error.value.code == "default_factory_failed"
    assert isinstance(error.value.__cause__, RuntimeError)


def test_field_aliases_work_in_both_orientations():
    class UserTable(RowTable):
        name = field("name", aliases=("full name",), required=True)

    class ContentTable(ColumnTable):
        id = id_field("IDs", aliases=("Keys",))
        headline = field("Headline", aliases=("Title",))

    assert UserTable.parse([["full name"], ["Alice"]])[0].name == "Alice"
    item = ContentTable.parse([["Keys", "A"], ["Title", "News"]])[0]
    assert item.id == "A"
    assert item.headline == "News"


def test_canonical_label_and_alias_cannot_appear_together():
    class UserTable(RowTable):
        name = field("name", aliases=("full name",))

    with pytest.raises(BDDTableError, match="one of its aliases") as error:
        UserTable.parse([["name", "full name"], ["Alice", "Alice"]])

    assert error.value.code == "duplicate_label"


def test_alias_collisions_are_rejected_when_schema_is_defined():
    with pytest.raises(SchemaDefinitionError, match="already used"):

        class InvalidTable(RowTable):
            name = field("name", aliases=("title",))
            title = field("title")


@pytest.mark.parametrize("policy", ["ignore", "preserve"])
def test_unknown_field_policies_allow_extra_columns(policy):
    class UserTable(RowTable):
        unknown_fields = policy
        name = field("name")

    user = UserTable.parse([["name", "team"], ["Alice", "News"]])[0]

    assert user.name == "Alice"
    assert user.table_extras == ({"team": "News"} if policy == "preserve" else {})


def test_inapplicable_variant_policy_can_preserve_values():
    class ArticleFields(TableFields):
        body = field("body")

    class PollFields(TableFields):
        options = field("options")

    class ContentTable(RowTable):
        inapplicable_fields = "preserve"
        kind = discriminator(
            "type", variants={"Article": ArticleFields, "Poll": PollFields}
        )

    poll = ContentTable.parse(
        [["type", "body", "options"], ["Poll", "legacy", "Yes,No"]]
    )[0]

    assert poll.options == "Yes,No"
    assert poll.table_extras == {"body": "legacy"}


def test_invalid_policy_is_rejected_at_class_creation():
    with pytest.raises(SchemaDefinitionError, match="unknown_fields"):

        class InvalidTable(RowTable):
            unknown_fields = "sometimes"
            value = field("value")


def test_field_rejects_conflicting_default_options():
    with pytest.raises(ValueError, match="both default and default_factory"):
        field("value", default="x", default_factory=lambda context: "y")

    with pytest.raises(ValueError, match="required fields cannot"):
        field("value", required=True, default="x")
