---
icon: lucide/ban
---

# Inapplicable Fields

Variant tables often include the union of all possible fields.

```gherkin
| type    | body         | options |
| Article | Article body |         |
| Poll    |              | Yes, No |
```

An empty cell for another variant is ignored. A non-empty cell for another
variant is rejected by default.

## Forbid

The default policy is:

```python
inapplicable_fields = "forbid"
```

This catches a value written into a field that does not belong to the selected
variant.

## Preserve

Use `"preserve"` when legacy tables may contain old values you still want to
inspect.

```python
class ContentTable(RowTable):
    inapplicable_fields = "preserve"
```

Preserved values are available as `record.table_extras`.

```python
assert poll.table_extras == {"body": "legacy"}
```

`"ignore"` is not supported today.
