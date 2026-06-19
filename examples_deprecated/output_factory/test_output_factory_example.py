"""Executable example for custom output construction."""

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field


class UserTable(RowTable):
    name = field("name", required=True)

    @classmethod
    def build_output(cls, record, context):
        """Create any project-owned result after parsing and validation."""

        return {
            "display_name": f"{context.user_data['prefix']} {record.name}",
            "feature_row": record.table_source.row,
        }


@scenario("users.feature", "Build a project object with parse context")
def test_custom_output_factory():
    pass


@given("the following output-factory users:", target_fixture="output_users")
def output_factory_users(datatable, bdd_table):
    return bdd_table.parse(
        datatable,
        schema=UserTable,
        context={"prefix": "Editor"},
    )


@then("the custom output builder receives the record and context")
def output_builder_receives_record_and_context(output_users):
    assert output_users == [{"display_name": "Editor Alice", "feature_row": 2}]
