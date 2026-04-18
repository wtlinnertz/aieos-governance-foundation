"""Fixture: minimal passing unit-test suite.

The conformance adapter under test runs against this file and emits canonical
JUnit findings. The expected shape lives at ../expected/smoke.junit.json.

This file is intentionally tiny — one passing test, one skipped test — so the
adapter has something meaningful to process without needing external dependencies.
"""

import pytest


def test_addition_is_correct() -> None:
    assert 1 + 1 == 2


@pytest.mark.skip(reason="fixture includes a skipped case so adapters handle it")
def test_placeholder_skipped() -> None:
    pass
