from pytest_bdd import given, scenario, then

from bdd_tablex import ColumnGroupExpander, ParseContext, TableData


class PairRange:
    def expand(self, cell, context):
        prefix = context.user_data["prefix"]
        return [cell.with_value(f"{prefix}-left"), cell.with_value(f"{prefix}-right")]


class PairRepeat:
    def expand(self, cell, expected_count, context):
        return [cell.with_value(f"{cell.value}-{index}") for index in range(expected_count)]


@scenario("content.feature", "Custom range and repeat rules receive parse context")
def test_custom_range_repeat_rules():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("custom range and repeat rules define project syntax")
def custom_range_repeat_rules(rows):
    expander = ColumnGroupExpander(
        key_row="Keys",
        range_rule=PairRange(),
        repeat_rule=PairRepeat(),
    )
    expanded = expander.transform(
        TableData.from_rows(rows),
        ParseContext.from_value({"prefix": "slot"}),
    )

    assert expanded.to_rows() == [
        ["Keys", "slot-left", "slot-right"],
        ["Value", "card-0", "card-1"],
    ]
