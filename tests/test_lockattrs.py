from random import randint
from typing import Any

import pytest
from lockattrs import ProtectedAttributeError, protect


class AMeta(type):
    """
    Meta class with locked attributes `data` and `id`.
    """

    @protect(
        ("data", "id"),
    )
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)


class BMeta(type):
    """
    Meta class with all attributes locked.
    """

    @protect()
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)


class A(metaclass=AMeta):
    data = "crucial-data-of-A"
    pass


class B(metaclass=BMeta):
    data = "crucial-data-of-B"


class C:
    """
    Default class without locked attributes.
    """
    pass


class TestLockAttrs:
    def test_set_new_attr(self):
        A.name = "A"
        assert A.name == "A"

        # Attribute name is not locked.
        A.name = "A1"
        assert A.name == "A1"

        # Attribute data is locked.
        assert A.data == "crucial-data-of-A"

    def test_lock_attr(self):
        with pytest.raises(ProtectedAttributeError):
            # Attribute data is locked.
            A.data = "other data"

    def test_lock_all_attrs(self):
        with pytest.raises(ProtectedAttributeError):
            B.data = "overwrite data"

        with pytest.raises(ProtectedAttributeError):
            new_var_name = f"b{randint(0, 1000)}"
            setattr(B, new_var_name, "initial-data")
            setattr(B, new_var_name, "overwrite initial-data")

    def test_benchmark_set_attrs(self, benchmark):
        def test():
            C.name = "hello"
            return C.name

        benchmark.pedantic(test, iterations=20000, rounds=4)
        assert C.name == "hello"

    def test_benchmark_set_attrs_A(self, benchmark):
        def test():
            A.name = "hello"
            return A.name

        benchmark.pedantic(test, iterations=20000, rounds=4)
        assert A.name == "hello"
