---
icon: lucide/package
---

# Installation

Talika supports Python 3.10 and newer.

The core package has no runtime dependencies:

```bash { .talika-terminal .speed-1 title="Install Talika" }
$ pip install talika
```
```bash { .talika-terminal .speed-1 title="Install Talika" }
$ pip install talika
```
## Optional extras

Install only the integrations you use:

```bash { .talika-terminal .speed-3}
$ pip install "talika[cli]"       # talika check and feature-file discovery
$ pip install "talika[pydantic]"  # Pydantic v2 output models
$ pip install "talika[test]"      # project test dependencies
```

The command line interface is available as:

```bash { .talika-terminal .speed-2 title="Check CLI Entrypoints" }
$ talika --help
$ python -m talika --help
```

## What gets installed

Core parsing imports only the Python standard library. The official Gherkin
parser is loaded lazily by the CLI and checker APIs, so ordinary schema parsing
does not depend on it.

Use the CLI extra when you want to validate `.feature` files without running
pytest:

```bash { .talika-terminal title="Install CLI Extra" }
$ pip install "talika[cli]"
```

Use the Pydantic extra when your schema returns Pydantic models:

```bash { .talika-terminal title="Install Pydantic Extra" }
$ pip install "talika[pydantic]"
```
