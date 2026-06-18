"""Module entry point for ``python -m bdd_tablex``.

Running the package as a module delegates to the same CLI entry point as the
``bdd-tablex`` console script.

!!! example
    ```bash
    python -m bdd_tablex describe tests/support/schemas.py:UserTable
    ```
"""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
