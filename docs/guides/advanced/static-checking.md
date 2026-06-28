---
icon: lucide/terminal
---

# Static Checking

Install the CLI extra:

```bash { .talika-terminal title="Install CLI Extra" }
$ pip install "talika[cli]"
```

Then validate feature-file tables without running pytest scenarios:

```bash { .talika-terminal title="Validate Feature Tables" }
$ talika check features/users.feature \
  --schema app.schemas:UserTable \
  --step "the users:" \
  --format json
```

## What check runs

`talika check` discovers matching Gherkin data tables, converts them to
source-aware `TableData`, and parses them with `error_mode="collect"`.

That means normal parsers and validators run. If they need deterministic
project dependencies, provide a context factory:

```bash { .talika-terminal title="Check With Context" }
$ talika check features/users.feature \
  --schema app.schemas:UserTable \
  --context-factory app.schemas:checking_context
```

The factory must be a zero-argument callable that returns a mapping.

## Exit codes

- `0`: valid
- `1`: validation failures
- `2`: filters matched no tables

Use `--scenario` and `--step` to narrow which tables are checked.
