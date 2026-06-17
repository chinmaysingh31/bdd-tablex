# Schema introspection

`Table.describe()` returns immutable dataclasses describing the public table
contract without parsing any feature data:

```python
contract = ContentTable.describe()

assert contract.orientation == "row"
assert contract.fields[0].required is True
assert contract.variants[0].value == "Article"
```

The contract includes canonical labels, aliases, defaults, parser names,
references, policies, variant fields, transformer identity, and output
configuration. `contract.as_dict()` supports documentation generators, editor
integrations, and other project tooling without reading private attributes.

