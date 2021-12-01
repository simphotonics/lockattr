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


class D:
    """
    Class with locked instance attributes.
    """

    @protect(("id", "data"))
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)


class E:
    """
    Class with all instance attributes locked.
    """

    @protect()
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)


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

    def test_error_message(self):
        try:
            B.data = 98
        except ProtectedAttributeError as error:
            assert (
                error.__str__()
                == "Class attribute 'data' must not be modified."
            )

    def test_benchmark_set_attrs(self, benchmark):
        def test():
            C.name = "hello"
            return C.name

        benchmark.pedantic(test, iterations=2000, rounds=5)
        assert C.name == "hello"

    def test_benchmark_set_attrs_A(self, benchmark):
        def test():
            A.name = "hello"
            return A.name

        benchmark.pedantic(test, iterations=2000, rounds=5)
        assert A.name == "hello"


class TestLockInstanceAttrs:
    def test_set_new_attr(self):
        d = D()
        d.name = "d"
        assert d.name == "d"

        # Attribute name is not locked.
        d.name = "d1"
        assert d.name == "d1"

        d.data = "crucial-data-of-d"
        # Attribute data is locked.
        assert d.data == "crucial-data-of-d"

    def test_lock_attr(self):
        d = D()
        d.data = "data-of-d"
        with pytest.raises(ProtectedAttributeError):
            # Attribute data is locked.
            d.data = "other data"

    def test_lock_all_attrs(self):
        e = E()
        e.data = "one"
        with pytest.raises(ProtectedAttributeError):
            e.data = "overwrite data"

        with pytest.raises(ProtectedAttributeError):
            new_var_name = f"b{randint(0, 1000)}"
            setattr(e, new_var_name, "initial-data")
            setattr(e, new_var_name, "overwrite initial-data")

    def test_error_message(self):
        d = D()
        d.data = 1
        try:
            d.data = 98
        except ProtectedAttributeError as error:
            assert (
                error.__str__()
                == "Class attribute 'data' must not be modified."
            )
