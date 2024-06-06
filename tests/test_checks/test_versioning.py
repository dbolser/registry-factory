"""Test cases for Registry meta information through versioning (other meta modules: accreditation).
Author: PeterHartog
"""
from dataclasses import dataclass
from typing import Any

import pytest

from registry_factory.checks.versioning import Versioning
from registry_factory.factory import Factory
from registry_factory.registry import AbstractRegistry


@pytest.fixture(scope="module")
def test_factory() -> Factory:
    """Return a test factory."""
    return Factory


@pytest.fixture(scope="module")
def test_forced_registry(test_factory: Factory) -> AbstractRegistry:
    """Return a test factory."""
    return test_factory.create_registry("test_registry", shared=False, checks=[Versioning(forced=True)])


@pytest.fixture(scope="module")
def test_unforced_registry(test_factory: Factory) -> AbstractRegistry:
    """Return a test factory."""
    return test_factory.create_registry("test_registry", shared=False, checks=[Versioning(forced=False)])


@pytest.fixture(scope="module")
def forced_registered_object(test_forced_registry: AbstractRegistry) -> None:
    """Return a test object."""

    @test_forced_registry.register("registered", version="0.0.1", date="2020-01-01")
    def test():
        pass

    return test


@pytest.fixture(scope="module")
def unforced_registered_object(test_unforced_registry: AbstractRegistry) -> None:
    """Return a test object."""

    @test_unforced_registry.register("test", version="0.0.1", date="2020-01-01")
    def test():
        pass

    return test


def test_versioning(test_forced_registry: AbstractRegistry) -> None:
    """Test the versioning."""

    @test_forced_registry.register("test", version="0.0.0", date="2020-01-01")
    def test():
        pass


def test_double_versioning(test_forced_registry: AbstractRegistry) -> None:
    """Test the versioning."""

    @test_forced_registry.register("test1", version="0.0.0", date="2020-01-01")
    def test1():
        pass

    @test_forced_registry.register("test2", version="0.0.1", date="2020-01-01")
    def test2():
        pass


def test_forced(test_forced_registry: AbstractRegistry) -> None:
    """Test the forced versioning."""

    with pytest.raises(Exception):

        @test_forced_registry.register("test3")
        def test():
            pass


def test_get_versioning(test_forced_registry: AbstractRegistry, forced_registered_object: Any) -> None:
    """Test the get versioning."""

    assert test_forced_registry.get("registered", version="0.0.1", date="2020-01-01") == forced_registered_object


def test_get_wrong_versioning(test_forced_registry: AbstractRegistry) -> None:
    """Test the get wrong versioning."""

    with pytest.raises(Exception):
        test_forced_registry.get("registered", version="0.0.2", date="2020-01-01")


def test_get_no_versioning(test_forced_registry: AbstractRegistry) -> None:
    """Test the get no versioning."""

    with pytest.raises(Exception):
        test_forced_registry.get("registered")


def test_get_incomplete_versioning(test_forced_registry: AbstractRegistry) -> None:
    """Test the get incomplete versioning."""

    with pytest.raises(Exception):
        test_forced_registry.get("registered", version="0.0.1")


def test_get_version(test_forced_registry: AbstractRegistry) -> None:
    """Test the get incomplete versioning."""

    assert test_forced_registry.get_info("registered", version="0.0.1")["date"] == "2020-01-01"


def test_custom_version(test_factory: Factory) -> None:
    """Test custom versioning."""

    @dataclass
    class CustomFields:
        """Custom fields."""

        version: str
        date: str
        environment: str

    Registry = test_factory.create_registry(
        "test_registry", shared=True, checks=[Versioning(CustomFields, forced=False)]
    )

    @Registry.register("test", version="0.0.1", date="2020-01-01", environment="test")
    def test():
        pass

    assert Registry.get_info("test", version="0.0.1")["environment"] == "test"
