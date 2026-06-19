"""Executable example for reusable field parsers and composition."""

from decimal import Decimal

from pytest_bdd import given, scenario, then

from bdd_tablex import (
    RowTable,
    boolean,
    compose,
    decimal,
    each,
    field,
    map_value,
    split,
    string,
)


class ProductTable(RowTable):
    """A row schema whose cells become typed Python values."""

    sku = field("sku", required=True, parser=string(strip=True, upper=True))
    price = field("price", required=True, parser=decimal())
    active = field("active", required=True, parser=boolean())
    tags = field(
        "tags",
        parser=compose(split(","), each(string(strip=True, lower=True))),
    )
    priority = field("priority", parser=map_value({"low": 1, "high": 10}))


@scenario("products.feature", "Convert product cells into useful Python values")
def test_reusable_field_parsers():
    pass


@given("the following typed products exist:", target_fixture="products")
def typed_products(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=ProductTable)


@then("product values are converted and composed")
def product_values_are_converted(products):
    assert products[0].sku == "A-1"
    assert products[0].price == Decimal("12.50")
    assert products[0].active is True
    assert products[0].tags == ["news", "featured"]
    assert products[0].priority == 10
    assert products[1].active is False
