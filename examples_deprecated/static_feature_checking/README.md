# Static feature-table checking

The checker parses `.feature` files with the official Gherkin parser and runs
matching tables through a schema without executing pytest scenarios:

```python
diagnostics = check_feature(
    "users.feature",
    schema=UserTable,
    step="the following users:",
)
```

Every diagnostic retains exact feature-file line and column coordinates.

Install the optional CLI dependency and check a local schema file:

```powershell
pip install "bdd-tablex[cli]"
bdd-tablex check examples/static_feature_checking/invalid_users.feature `
  --schema examples/static_feature_checking/schemas.py:CheckedUserTable `
  --step "the following statically checked users:"
```

The command exits with `1` for invalid tables, `0` when all matched tables are
valid, and `2` when filters match no tables. Use
`--context-factory module:function` when custom parsers or
validators need deterministic project services during static checking.
