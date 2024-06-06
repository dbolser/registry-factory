"""Test cases for Registry sharing.
Author: PeterHartog
"""
from dataclasses import dataclass

import pytest

from registry_factory.factory import Factory
from registry_factory.registry import AbstractRegistry


@pytest.fixture(scope="module")
def test_factory() -> Factory:
    """Return a test factory."""
    return Factory  # type: ignore


def test_instantiation(test_factory: Factory) -> None:
    """Test creating a new method with the abstract methods."""

    with pytest.raises(ValueError):
        test_factory()  # type: ignore


def test_inheretence(test_factory: Factory) -> None:
    """Test creating a new method without the abstract methods."""

    class _TestFactory(test_factory):  # type: ignore
        pass


def test_create_registry(test_factory: Factory) -> None:
    """Test creating a new registry."""

    assert issubclass(test_factory.create_registry("test_registry"), AbstractRegistry)  # type: ignore


def test_get_registries(test_factory: Factory) -> None:
    """Test getting all registries."""

    _ = test_factory.create_registry("test_registry")
    print(test_factory.get_registries())

    assert "test_registry" in test_factory.get_registries().keys()


def test_get_subclass_choices(test_factory: Factory) -> None:
    """Test getting the subclass choices."""

    test_registry = test_factory.create_registry("test_registry")
    test_registry.register_prebuilt(lambda: None, "test")

    assert "test" in test_factory.get_options(["test_registry"])


def test_get_subclass_arguments(test_factory: Factory) -> None:
    """Test getting the subclass choices."""

    test_registry = test_factory.create_registry("test_registry")

    @test_registry.register_arguments("test_arg")
    @dataclass
    class TestArguments:
        test_arg: str

    assert TestArguments in test_factory.get_registry_arguments(["test_registry"]).values()
