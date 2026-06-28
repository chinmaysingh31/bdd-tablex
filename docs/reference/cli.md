---
icon: lucide/terminal
---

# CLI

The CLI is installed with:

```bash { .talika-terminal title="Install CLI" }
$ pip install "talika[cli]"
```

## check

```bash { .talika-terminal title="Run Static Checks" }
$ talika check PATH... --schema module:SchemaClass
```

Options:

- `--step TEXT`
- `--scenario NAME`
- `--format text|json`
- `--context-factory module:function`

Exit codes:

- `0`: valid
- `1`: diagnostics found
- `2`: no matching tables

## describe

```bash { .talika-terminal title="Describe Schema" }
$ talika describe module:SchemaClass
$ talika describe module:SchemaClass --format json
```

## Checker APIs

```python
discover_feature_tables(path, *, step=None, scenario=None)
check_feature(path, *, schema, step=None, scenario=None, context=None)
```

`FeatureTable` describes one discovered table. `FeatureDiagnostic` pairs a
feature-table location with a `TableError`.
