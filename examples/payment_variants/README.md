# Row variants with output models

Variants work for `RowTable` as well as `ColumnTable`. This example also shows
that each selected variant may construct a different project model.

```python
class PaymentTable(RowTable):
    payment_type = discriminator_field("type")
    amount: Decimal = field("amount", required=True)


@PaymentTable.variant("card")
class CardPaymentRow(PaymentTable):
    output_model = CardPayment
    last_four = field("last_four", required=True)


@PaymentTable.variant("bank")
class BankPaymentRow(PaymentTable):
    output_model = BankPayment
    account = field("account", required=True)
```

Parsing still follows the normal lifecycle:

1. Parse shared and selected variant fields.
2. Resolve local references.
3. Run the selected variant's `validate_record()`.
4. Run the base table's `validate_records()` across the mixed schema records.
5. Construct each selected variant's `output_model`, when configured.

The result can therefore be heterogeneous without adding business-domain
knowledge to `bdd-tablex`:

```python
payments = PaymentTable.parse(datatable)

assert isinstance(payments[0], CardPayment)
assert isinstance(payments[1], BankPayment)
```

Run this example alone:

```powershell
uv run pytest -p no:cacheprovider examples/payment_variants -q
```

