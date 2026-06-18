from importlib.metadata import version

import bdd_tablex


def test_public_version_matches_distribution_metadata():
    assert bdd_tablex.__version__ == version("bdd-tablex")
