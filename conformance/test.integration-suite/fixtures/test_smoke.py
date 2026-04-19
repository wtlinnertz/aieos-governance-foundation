"""Fixture: minimal passing integration-test suite.

Integration-style tests typically probe behavior involving multiple
components or dependency fixtures. The skeleton here keeps the scope
identical to test.unit-suite so the conformance shape is consistent —
richer integration fixtures (containerized deps, env-var consumption)
belong in adapter-specific extended suites.
"""

import os


def test_trivial_integration_passes():
    assert 1 + 1 == 2


def test_environment_readable():
    # Integration suites may assert environment presence without coupling to
    # specific values. PATH is always present on POSIX runners.
    assert "PATH" in os.environ
