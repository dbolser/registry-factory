"""Test cases for Registry factory pattern ensurance.
Author: PeterHartog
"""
import pytest

from registry_factory.checks.factory_pattern import FactoryPattern
from registry_factory.factory import Factory
from registry_factory.registry import AbstractRegistry


class Pattern:
    """Test pattern."""

    def __init__(self, name):
        self.name = name

    def hello_world(self):
        """Hello world."""
        print("Hello world")


@pytest.fixture(scope="module")
def test_factory() -> Factory:
    """Return a test factory."""
    return Factory


@pytest.fixture(scope="module")
def test_forced_registry(test_factory: Factory) -> AbstractRegistry:
    """Return a test factory."""
    return test_factory.create_registry(
        "test_registry", shared=False, checks=[FactoryPattern(factory_pattern=Pattern, forced=True)]
    )


@pytest.fixture(scope="module")
def test_forced_shared_registry(test_factory: Factory) -> AbstractRegistry:
    """Return a test factory."""
    return test_factory.create_registry(
        "test_registry", shared=True, checks=[FactoryPattern(factory_pattern=Pattern, forced=True)]
    )


@pytest.fixture(scope="module")
def test_unforced_registry(test_factory: Factory) -> AbstractRegistry:
    """Return a test factory."""
    return test_factory.create_registry(
        "test_registry", shared=False, checks=[FactoryPattern(factory_pattern=Pattern, forced=False)]
    )


@pytest.fixture(scope="module")
def test_unforced_shared_registry(test_factory: Factory) -> AbstractRegistry:
    """Return a test factory."""
    return test_factory.create_registry(
        "test_registry", shared=True, checks=[FactoryPattern(factory_pattern=Pattern, forced=False)]
    )


def test_pattern(test_forced_registry: AbstractRegistry) -> None:
    """Test the pattern."""

    test_forced_registry.register_prebuilt(key="pattern_test", obj=Pattern)


def test_wrong_pattern(test_forced_registry: AbstractRegistry, test_unforced_registry: AbstractRegistry) -> None:
    """Test the wrong pattern."""

    with pytest.warns():
        test_unforced_registry.register_prebuilt(key="wrong_pattern_test", obj="wrong_pattern")

    with pytest.raises(Exception):
        test_forced_registry.register_prebuilt(key="wrong_pattern_test", obj="wrong_pattern")


def test_inhereted_pattern(test_forced_registry: AbstractRegistry) -> None:
    """Test inhereted pattern."""

    class InheretedPattern(Pattern):
        pass

    class DoubleInheretedPattern(InheretedPattern):
        pass

    test_forced_registry.register_prebuilt(key="inhereted_test", obj=InheretedPattern)
    test_forced_registry.register_prebuilt(key="double_inhereted_test", obj=DoubleInheretedPattern)


def test_wrong_inhereted_pattern(
    test_forced_registry: AbstractRegistry, test_unforced_registry: AbstractRegistry
) -> None:
    """Test wrong inhereted pattern."""

    class WrongPattern:
        pass

    with pytest.warns():
        test_unforced_registry.register_prebuilt(key="wrong_inhereted_test", obj=WrongPattern)

    with pytest.raises(Exception):
        test_forced_registry.register_prebuilt(key="wrong_inhereted_test", obj=WrongPattern)


def test_common_pattern(test_forced_registry: AbstractRegistry) -> None:
    """Test common pattern."""

    class CommonPattern:
        def __init__(self, name):
            self.name = name

        def hello_world(self):
            """Hello world."""
            print("Hello world")

    test_forced_registry.register_prebuilt(key="common_pattern_test", obj=CommonPattern)


def test_wrong_common_pattern(test_forced_registry: AbstractRegistry, test_unforced_registry: AbstractRegistry) -> None:
    """Test wrong common pattern."""

    class WrongPattern:
        def __init__(self, name):
            self.name = name

        def hello_world2(self):
            """Hello world 2."""
            print("Hello world 2: Electric Boogaloo")

    with pytest.warns():
        test_unforced_registry.register_prebuilt(key="wrong_common_pattern_test", obj=WrongPattern)

    with pytest.raises(Exception):
        test_forced_registry.register_prebuilt(key="wrong_common_pattern_test", obj=WrongPattern)
