"""Test cases for Registry sharing options.
Author: PeterHartog
"""

import pytest

from registry_factory.factory import Factory
from registry_factory.registry import AbstractRegistry
from registry_factory.utils import RegistrationError


@pytest.fixture(scope="module")
def test_factory() -> Factory:
    """Return a test factory."""
    return Factory


@pytest.fixture(scope="module")
def test_registry(test_factory: Factory) -> AbstractRegistry:
    """Return a test registry."""
    return Factory.create_registry("test_registry", shared=True)


@pytest.fixture(scope="module")
def test_shared_registry(test_factory: Factory) -> AbstractRegistry:
    """Return a test registry."""
    return Factory.create_registry("test_shared_registry", shared=True)


@pytest.fixture(scope="module")
def test_unshared_registry(test_factory: Factory) -> AbstractRegistry:
    """Return an unshared test registry."""
    return Factory.create_registry("test_unshared_registry", shared=False)


def test_shared_register(test_registry: AbstractRegistry, test_shared_registry: AbstractRegistry) -> None:
    """Test the register method for shared registries."""

    @test_registry.register("shared_registered")
    def test():
        pass

    assert test_shared_registry.get("shared_registered") == test


def test_unshared_register(test_registry: AbstractRegistry, test_unshared_registry: AbstractRegistry) -> None:
    """Test the register method for unshared registries."""

    @test_registry.register("unshared_registered")
    def test():
        pass

    with pytest.raises(RegistrationError):
        test_unshared_registry.get("unshared_registered")


def test_shared_register_prebuilt(test_registry: AbstractRegistry, test_shared_registry: AbstractRegistry) -> None:
    """Test the register prebuilt method for shared registries."""

    def test():
        pass

    test_registry.register_prebuilt(test, "shared_prebuilt")
    assert test_shared_registry.get("shared_prebuilt") == test


def test_unshared_register_prebuilt(test_registry: AbstractRegistry, test_unshared_registry: AbstractRegistry) -> None:
    """Test the register prebuilt method for unshared registries."""

    def test():
        pass

    test_registry.register_prebuilt(test, "unshared_prebuilt")
    with pytest.raises(RegistrationError):
        test_unshared_registry.get("unshared_prebuilt")


def test_shared_validate_choice(test_registry: AbstractRegistry, test_shared_registry: AbstractRegistry) -> None:
    """Test the validate_choice method for shared registries."""

    test_registry.validate_choice("shared_registered")  # Should not raise an error
    test_shared_registry.validate_choice("shared_registered")


def test_unshared_validate_choice(test_registry: AbstractRegistry, test_unshared_registry: AbstractRegistry) -> None:
    """Test the validate_choice method for unshared registries."""

    test_registry.validate_choice("shared_registered")  # Should not raise an error
    with pytest.raises(RegistrationError):
        test_unshared_registry.validate_choice("shared_registered")


def test_shared_double_register(test_registry: AbstractRegistry, test_shared_registry: AbstractRegistry) -> None:
    """Test the register method with a double registration for shared registries."""

    @test_registry.register("shared_double_registered")
    def test():
        pass

    def test2():
        pass

    test_registry.register_prebuilt(test2, "shared_double_prebuilt")

    with pytest.raises(KeyError):

        @test_shared_registry.register("shared_double_registered")
        def test3():
            pass

    with pytest.raises(KeyError):

        @test_shared_registry.register("shared_double_prebuilt")
        def test4():
            pass


def test_unshared_double_register(test_registry: AbstractRegistry, test_unshared_registry: AbstractRegistry) -> None:
    """Test the register method with a double registration for unshared registries."""

    @test_registry.register("unshared_double_registered")
    def test():
        pass

    def test2():
        pass

    test_registry.register_prebuilt(test2, "unshared_double_prebuilt")

    @test_unshared_registry.register("unshared_double_registered")
    def test3():
        pass

    @test_unshared_registry.register("unshared_double_prebuilt")
    def test4():
        pass
