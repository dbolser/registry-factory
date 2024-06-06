"""Test cases for Registry factory pattern ensurance.
Author: PeterHartog
"""
from typing import Any

import pytest

from registry_factory.checks.testing import Testing as _Testing
from registry_factory.factory import Factory
from registry_factory.registry import AbstractRegistry


class CallableTestModule:
    """Module to test."""

    def __init__(self, key: str, obj: Any, **kwargs):
        self.name = obj
        self.assert_name()

    def assert_name(self):
        assert self.name == "test", "Name is not test"


@pytest.fixture(scope="module")
def test_factory() -> Factory:
    """Return a test factory."""
    return Factory


@pytest.fixture(scope="module")
def test_forced_registry(test_factory: Factory) -> AbstractRegistry:
    """Return a test factory."""
    return test_factory.create_registry(
        "test_registry", shared=False, checks=[_Testing(test_module=CallableTestModule, forced=True)]
    )


@pytest.fixture(scope="module")
def test_unforced_registry(test_factory: Factory) -> AbstractRegistry:
    """Return a test factory."""
    return test_factory.create_registry(
        "test_registry", shared=False, checks=[_Testing(test_module=CallableTestModule, forced=False)]
    )


def test_testing(test_forced_registry: AbstractRegistry) -> None:
    """Test the pattern."""

    test_forced_registry.register_prebuilt(key="name_test", obj="test")


def test_wrong_pattern_unforced(test_unforced_registry: AbstractRegistry) -> None:
    """Test the wrong pattern."""

    with pytest.warns():
        test_unforced_registry.register_prebuilt(key="wrong_name_test", obj="not_test")


def test_wrong_pattern_forced(test_forced_registry: AbstractRegistry) -> None:
    """Test the wrong pattern."""

    with pytest.raises(Exception):
        test_forced_registry.register_prebuilt(key="wrong_name_test", obj="not_test")
