# bdd-tablex Examples

This folder is a docs-ready playground for learning bdd-tablex in small, ordered steps.

The examples are intentionally split by concept. The `users/` track teaches row tables, parser behavior, schema evolution, validation, output objects, and API styles. The `cms/` track teaches column tables, variants, references, source metadata, CellDSL, transformers, introspection, static checking, and CLI usage. The `complete/` track combines many of those ideas only after the focused examples have introduced them separately.

Every leaf folder is standalone:

- `README.md` explains the concept as a tutorial page.
- A `.feature` file shows the BDD table a feature author would write.
- A `test_*.py` file contains the schema, step bindings, deterministic helpers, and assertions.
- CLI examples include `schemas.py` so command-line imports do not load pytest-bdd scenario decorators.

## Learning Path

1. Start with `users/01_row_tables/01_basic_required_fields`.
2. Continue through `users/02_parsers`, especially `02_boolean_custom_vocabulary` and `07_empty_cell_policies`.
3. Read `users/03_schema_evolution` when table language changes over time.
4. Read `users/04_validation_and_errors` before writing project validators.
5. Read `users/05_outputs_and_api_styles` when choosing between records, dataclasses, Pydantic, functional helpers, and the pytest fixture.
6. Move into `cms/01_column_tables` for column-oriented modeling.
7. Use `cms/02_variants` for discriminated content records.
8. Use `cms/03_references_and_sources` when records point at each other or diagnostics need source metadata.
9. Use `cms/04_cell_dsl` for project-owned cell shorthand.
10. Use `cms/05_transformers` for compact table syntax and source-preserving rewrites.
11. Use `cms/06_tooling` for schema descriptions, static checking, and CLI workflows.
12. Finish with `complete/01_complete_cms_walkthrough`.

## CLI Schema Import Rule

When using `bdd-tablex describe` or `bdd-tablex check`, point `--schema` at a plain module that only declares schemas. Do not point CLI commands at pytest-bdd test modules containing `@scenario(...)` decorators, because those decorators expect pytest configuration to be active.

For example:

````powershell
bdd-tablex describe examples/cms/06_tooling/03_cli_describe/schemas.py:ContentTable
```

````powershell
bdd-tablex check examples/cms/06_tooling/04_cli_check_json/content.feature `
  --schema examples/cms/06_tooling/04_cli_check_json/schemas.py:ContentTable `
  --step "the following statically checked content exists:" `
  --format json
```



