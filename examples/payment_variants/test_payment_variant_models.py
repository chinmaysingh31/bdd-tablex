"""Executable row-oriented example with per-variant dataclass outputs."""

from dataclasses import dataclass
from decimal import Decimal

from pytest_bdd import given, scenario, then

from bdd_tablex import RowTable, discriminator_field, field


@dataclass(frozen=True)
class CardPayment:
    """Project domain object produced for card rows."""

    payment_type: str
    amount: Decimal
    last_four: str


@dataclass(frozen=True)
class BankPayment:
    """Project domain object produced for bank-transfer rows."""

    payment_type: str
    amount: Decimal
    account: str


class PaymentTable(RowTable):
    """Fields shared by every payment variant."""

    payment_type = discriminator_field("type")
    amount: Decimal = field("amount", required=True)


@PaymentTable.variant("card")
class CardPaymentRow(PaymentTable):
    """Card-only input and output configuration."""

    output_model = CardPayment
    last_four = field("last_four", required=True)


@PaymentTable.variant("bank")
class BankPaymentRow(PaymentTable):
    """Bank-only input and output configuration."""

    output_model = BankPayment
    account = field("account", required=True)


@scenario("payment_variants.feature", "Build different domain models from row variants")
def test_payment_variant_models():
    pass


@given("the following payments were received:", target_fixture="payments")
def payments_received(datatable, bdd_table):
    return bdd_table.parse(datatable, schema=PaymentTable)


@then("payment variants become their own domain models")
def variants_become_domain_models(payments):
    assert payments == [
        CardPayment(payment_type="card", amount=Decimal("25"), last_four="4242"),
        BankPayment(payment_type="bank", amount=Decimal("50"), account="QA-001"),
    ]
