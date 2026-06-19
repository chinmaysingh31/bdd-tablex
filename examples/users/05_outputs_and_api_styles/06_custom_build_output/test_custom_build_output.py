from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, field


class ExampleTable(RowTable):
    value = field("value")

    @classmethod
    def build_output(cls, record, context):
        return {"display": context.user_data["prefix"] + record.value}


@scenario("users.feature", "Demonstrate Custom Build Output")
def test_custom_build_output():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("the custom build output behavior is correct")
def behavior(rows):
    assert ExampleTable.parse(rows, context={"prefix": "Value: "}) == [
        {"display": "Value: example"}
    ]
