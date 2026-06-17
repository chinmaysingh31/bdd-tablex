# Composable cell DSLs

Large projects often have shared tokens plus domain-specific syntax. Compose
separate `CellDSL` objects instead of building one global registry:

```python
parser = compose_cell_dsls(shared_cells, content_cells)
```

The first DSL with a matching rule wins. Within each DSL the order is exact
tokens, full-match patterns, predicates, and fallback.

Rules can be scoped by schema attribute name:

```python
@content_cells.token("random", fields={"headline"})
def random_headline(context):
    return context.user_data["headline_factory"]()
```

The literal `random` therefore remains untouched in `category`. Scoped exact
tokens take precedence over a global exact token with the same text.

