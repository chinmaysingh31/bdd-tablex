from importlib.metadata import version

import bdd_tablex


def test_public_version_matches_distribution_metadata():
    assert bdd_tablex.__version__ == version("bdd-tablex")


def test_public_all_exports_are_available_at_top_level():
    assert bdd_tablex.__all__
    for name in bdd_tablex.__all__:
        assert getattr(bdd_tablex, name)
