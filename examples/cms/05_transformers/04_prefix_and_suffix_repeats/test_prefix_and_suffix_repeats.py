from pytest_bdd import given, scenario, then

from bdd_tablex import NumericRange, ParseContext, PrefixRepeat, SuffixRepeat, TableCell


@scenario("content.feature", "Prefix and suffix repeat rules create repeated cells")
def test_prefix_and_suffix_repeats():
    pass


@given("the example table:", target_fixture="rows")
def example_table(datatable):
    return datatable


@then("prefix and suffix repeat rules expand values")
def prefix_and_suffix_repeats(rows):
    context = ParseContext()
    key_cells = NumericRange("..").expand(
        TableCell.from_value("1..2", row=1, column=2), context
    )
    prefix_cells = PrefixRepeat(":").expand(
        TableCell.from_value("2:Article", row=2, column=2),
        len(key_cells),
        context,
    )
    suffix_cells = SuffixRepeat(" x").expand(
        TableCell.from_value("Shared x2", row=3, column=2),
        len(key_cells),
        context,
    )

    assert [cell.value for cell in key_cells] == ["1", "2"]
    assert [cell.value for cell in prefix_cells] == ["Article", "Article"]
    assert [cell.value for cell in suffix_cells] == ["Shared", "Shared"]
