"""Test cases for Registry arguments.
"""

from dataclasses import dataclass
from typing import Any

import pytest

from registry_factory.registry import AbstractRegistry, Registry
from registry_factory.utils import RegistrationError, RegistrationWarning


@pytest.fixture(scope="module")
def test_registry() -> AbstractRegistry:
    """Return a test registry."""
    return Registry


@pytest.fixture(scope="module")
def registered_object(test_registry: AbstractRegistry) -> Any:
    """Return a test object."""

    @test_registry.register_arguments("registered")
    @dataclass
    class Test:
        arg1 = 1

    return Test


def test_register_arguments(test_registry: AbstractRegistry, registered_object: Any) -> None:
    """Test the register_arguments method."""
    assert test_registry.get_arguments("registered") == registered_object


def test_register_arguments_not_dataclass(test_registry: AbstractRegistry) -> None:
    """Test the register_arguments method with a non dataclass."""

    with pytest.raises(RegistrationError):

        @test_registry.register_arguments("registered_non_dataclass")
        def test():
            pass


def test_register_arguments_not_dataclass_warning(test_registry: AbstractRegistry) -> None:
    """Test the register_arguments method with a non dataclass and a warning."""
    with pytest.warns(RegistrationWarning):

        @test_registry.register_arguments("registered_non_dataclass")
        class Test:
            arg1 = 1


def test_register_arguments_already_registered(test_registry: AbstractRegistry, registered_object: Any) -> None:
    """Test the register_arguments method with a already registered key."""

    with pytest.raises(KeyError):

        @test_registry.register_arguments("registered")
        @dataclass
        class Test:
            arg1 = 1
