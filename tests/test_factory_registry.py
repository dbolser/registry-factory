"""Test cases for Factory Registry registration.
Author: PeterHartog
"""
from typing import Any

import pytest

from registry_factory.factory import Factory
from registry_factory.registry import AbstractRegistry
from registry_factory.utils import RegistrationError, RegistrationWarning


@pytest.fixture(scope="module")
def test_registry() -> AbstractRegistry:
    """Return a test registry."""
    return Factory.create_registry("test_registry", shared=False)


@pytest.fixture(scope="module")
def registered_object(test_registry: AbstractRegistry) -> Any:
    """Return a test object."""

    @test_registry.register("registered")
    def test():
        pass

    return test


@pytest.fixture(scope="module")
def prebuilt_object(test_registry: AbstractRegistry) -> Any:
    """Return a test object."""

    def test():
        pass

    test_registry.register_prebuilt(test, "prebuilt")
    return test


def test_inheritance(test_registry: AbstractRegistry) -> None:
    """Test the inheritance of the Registry class."""
    assert issubclass(test_registry, AbstractRegistry)  # type: ignore


def test_register(test_registry: AbstractRegistry, registered_object: Any) -> None:
    """Test the register method."""
    assert test_registry.get("registered") == registered_object


def test_register_prebuilt(test_registry: AbstractRegistry, prebuilt_object: Any) -> None:
    """Test the register prebuilt method."""
    assert test_registry.get("prebuilt") == prebuilt_object


def test_validate_choice(test_registry: AbstractRegistry) -> None:
    """Test the validate_choice method."""

    test_registry.validate_choice("registered")  # Should not raise an error
    with pytest.raises(RegistrationError):
        test_registry.validate_choice("unregistered")


def test_get(test_registry: AbstractRegistry, registered_object: Any) -> None:
    """Test the get method."""

    assert test_registry.get("registered") == registered_object
    with pytest.raises(RegistrationError):
        test_registry.get("unregistered")


def test_check_choice(test_registry: AbstractRegistry) -> None:
    """Test the check_choice method."""

    assert test_registry.check_choice("registered") is True
    with pytest.warns(RegistrationWarning):
        assert test_registry.check_choice("unregistered") is False


def test_double_register(test_registry: AbstractRegistry) -> None:
    """Test the register method with a double registration."""

    with pytest.raises(KeyError):

        @test_registry.register("registered")
        def test1():
            pass

    with pytest.raises(KeyError):

        @test_registry.register("prebuilt")
        def test2():
            pass

    with pytest.raises(KeyError):

        def test3():
            pass

        test_registry.register_prebuilt(obj=test3, key="registered")

    with pytest.raises(KeyError):

        def test4():
            pass

        test_registry.register_prebuilt(obj=test4, key="prebuilt")


def test_reset(test_registry: AbstractRegistry) -> None:
    """Test the reset method."""

    test_registry.reset()
    with pytest.raises(RegistrationError):
        test_registry.get("registered")
