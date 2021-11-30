# Locking Class Attributes
[![tests](https://github.com/simphotonics/lockattrs/actions/workflows/tests.yml/badge.svg)](https://github.com/simphotonics/lockattrs/actions/workflows/tests.yml)
[![docs](https://raw.githubusercontent.com/simphotonics/lockattrs/main/images/docs-badge.svg)](https://lockattrs.simphotonics.com)

Most object oriented languages (C++, Java, Dart, Kotlin, Swift)
include visibiliy modifiers. This enables
encapsulation where for example the inner workings of a class
can be detached from the outside world and thus protected from
direct modification.

Python on the other hand does not have a language-backed concept
of privacy. Instead functions or variables with an identifier
that starts with an underscore are
deemed private and should not be modified or otherwise
relied upon since they may change in a future version of the module.

In some cases, certain attributes may be crucial for the
correct working a class and the programmer might
want to pervent any inadvertent modification.

The package [`lockattrs`][lockattrs] provides a decorator that can
be used with the method `__setattr__` to lock certain attributes
or all attributes.

Note that despite the name similarity [`lockattrs`][lockattrs] is
not related to the package [`attrs`][attrs] providing
a concise way of creating and validating data classes.


## Installation

To install the package [`lockattrs`][lockattrs] use the command:
```Console
$ pip install lockattrs
```

## Usage

This package provides the decorator function [`protect`][protect] which can be
used to prevent modification of attributes
after they have been initially set.

The intended use-case is demonstrated below. Locking the
instance attributes of a meta-class is equivalent to
locking the class attributes of the class (the meta-class instance).

Using the decorator [`protect`][protect] involves the following steps:

1. Declare a class or meta-class.
2. Override the method `__setattr__`.
3. Decorate `__setattr__` with the function [`protect`][protect].
4. Optionally: Specify which attributes should be locked and
   what type of error should be raised during an attribute
   modification attempt.

``` Python
from lockattrs import protect

class AMeta(type):
    """
    Meta class of A.
    """
    @protect(('data','id'), )
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)

class A(metaclass=AMeta):
    data = 'crucial-data'
    pass

A.data = 'initial-data' # First initiation is OK. Attribute 'data' is now locked.
A.data = 'new-data'     # Raises an error (default type: ProtectedAttributeError).

A.name = 'A'
A.name = 'A1'           # OK, since the attribute 'name' is not locked.
```

Note: Locking certain attributes may be prohibitively
costly in terms of computational time
when used with objects that are
instantiated often (for example in a loop)
and where attributes are set/modified frequently.

The benchmarks below were produced using the package
[`pytest-benchmark`][pytest-benchmark] on a PC with 32GB RAM
and an Intel Core i5-6260U CPU running at 1.80GHz.
As the mean runtimes show, setting an attribute of class `A`
takes approximately 40 times as long compared to a standard class
(without an annotated `__setattr__` method).


``` Console
--------------------------------- benchmark: 2 tests -----------------------------------
Name (time in ns)                   Mean              StdDev          Rounds  Iterations
----------------------------------------------------------------------------------------
test_benchmark_set_attrs        348.8611 (1.0)       66.8829 (1.0)         4       20000
test_benchmark_set_attrs_A   13,496.0524 (38.69)    912.2178 (13.64)       4       20000
----------------------------------------------------------------------------------------
```


## Features and bugs

Please file feature requests and bugs at the [issue tracker].
Contributions are welcome.

[issue tracker]: https://github.com/simphotonics/lockattrs/issues

[attrs]: https://pypi.org/project/attrs

[protect]: http://lockattrs.simphotonics.com/reference/lockattrs/decorators/#protect

[pypi]: https:://pypi.org

[pytest]: https://pypi.org/project/pytest/

[pytest-benchmark]: https://pypi.org/project/pytest-benchmark/

[lockattrs]: https://github.com/simphotonics/lockattrs