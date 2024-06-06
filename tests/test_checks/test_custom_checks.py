"""Test cases for Registry sharing.
Author: PeterHartog
"""
from typing import Any, Dict, Optional, Tuple

import pytest

from registry_factory.factory import Factory
from registry_factory.patterns.observer import RegistryObserver


@pytest.fixture(scope="module")
def test_factory() -> Factory:
    """Return a test factory."""
    return Factory


@pytest.fixture(scope="module")
def passive_observer() -> RegistryObserver:
    """Return a passive observer."""

    class PassiveObserver(RegistryObserver):
        def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            return (key, {}, obj, None)

        def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            return (key, {}, obj, None)

    return PassiveObserver()


@pytest.fixture(scope="module")
def raise_call_error() -> RegistryObserver:
    """Return an observer that raises an error when calling."""

    class RaiseCallError(RegistryObserver):
        def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            raise ValueError

        def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            return (key, {}, obj, None)

    return RaiseCallError()


@pytest.fixture(scope="module")
def raise_register_error() -> RegistryObserver:
    """Return an observer that raises an error when registering."""

    class RaiseRegisterError(RegistryObserver):
        def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            return (key, {}, obj, None)

        def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            raise ValueError

    return RaiseRegisterError()


@pytest.fixture(scope="module")
def additional_error() -> RegistryObserver:
    """Return an observer that raises an error when additional parameters are passed."""

    class AdditionalError(RegistryObserver):
        def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            if "test" in kwargs:
                raise ValueError
            return (key, {}, obj, None)

        def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            if "test" in kwargs:
                raise ValueError
            return (key, {}, obj, None)

    return AdditionalError()


def test_wrong_instantiation() -> None:
    """Test creating a new method without the abstract methods."""

    class TestCustomCheck(RegistryObserver):
        pass

    with pytest.raises(TypeError):
        TestCustomCheck()


def test_registry_validate_register(test_factory: Factory, raise_register_error: RegistryObserver) -> None:
    """Test the registry with the validate register method."""

    test_registry = test_factory.create_registry("test_registry", shared=False, checks=[raise_register_error])

    with pytest.raises(Exception):

        @test_registry.register("registered")
        def test():
            pass


def test_registry_validate_call(test_factory: Factory, raise_call_error: RegistryObserver) -> None:
    """Test the registry with the validate call method."""

    test_registry = test_factory.create_registry("test_registry", shared=False, checks=[raise_call_error])

    @test_registry.register("registered")
    def test():
        pass

    with pytest.raises(Exception):
        test_registry.get("registered")


def test_registry_additional_params(test_factory: Factory, additional_error: RegistryObserver) -> None:
    """Test the registry with the postcheck and additional parameters."""

    test_registry = test_factory.create_registry("test_registry", shared=False, checks=[additional_error])

    with pytest.raises(Exception):

        @test_registry.register("additional_params", test="")
        def test():
            pass

    with pytest.raises(Exception):

        @test_registry.register("additional_params")
        def test2():
            pass

        test_registry.get("additional_params", test="") == test
