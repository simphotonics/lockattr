# Locking Attributes Python
[![tests](https://github.com/simphotonics/lockattrs/actions/workflows/test.yml/badge.svg)](https://github.com/simphotonics/lockattrs/actions/workflows/test.yml)
<!-- [![Python](https://simphotonics.com/images/docs-badge.svg)](https://generic-validation.simphotonics.com) -->

In most object oriented languages like C++, Java, Dart, Kotlin,
..., class variables and functions can be declared `private`.
This enables encapsulation where the inner workings of a class
are detached from the outside world and thus protected from
direct modification.

Python on the other hand does not have a language-backed concept
of privacy. Instead functions or variables  whose name start with an
underscore are deemed private and should not be modified or otherwise
relied upon since they may change in a future version of the module.

In some cases, certain attributes may be crucial for the
correct working a class and inadverted modification
must be prevented.

The package [`lockattrs`][lockattrs] provides a decorator that can
be used with the method `__setattr__` to lock certain attributes
or all attributes.


## Installation

To install the package [`lockattrs`][lockattrs] use the command:
```Console
$ pip install lockattrs
```

## Usage

This package provides the function `lockattrs` which can be
used to prevent modification of attributes
after they have been initially set.

The intended use-case is demonstrated below. Locking the
instance attributes of a meta-class is equivalent to
locking the class attributes of the class (the meta-class instance).

Using the decorator `lockattrs` involves the following steps:
1. Declare a class or meta-class.
2. Override the method `__setattr__`
3. Decorate `__setattr__` with the function `lockattrs`.
4. Optionally specify which attributes should be locked and
   what type of error should be raised during an attribute
   modification attempt.

``` Python
import lockattrs

class AMeta(type):
    """
    Meta class of A.
    """
    @lockattrs(('data','id'), )
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)

class A(metaclass=AMeta):
    data = 'crucial-data'
    pass

A.data = 'new-data'
```

Note: Locking certain attributes may be prohibitively
costly in terms of computational time
when used with objects that are
instantiated frequently (for example in a loop)
and where attributes are set frequently.

As the benchmarks below show, setting an attribute of class `A`
takes approximately 40 times as long compare to a standard class
(without an annotated `__setattr__` method).


``` Console
----------------------------------- benchmark: 2 tests ----------------------------------------
Name (time in ns)                     Mean              StdDev               Rounds  Iterations
-----------------------------------------------------------------------------------------------
test_benchmark_set_attrs          348.8611 (1.0)       66.8829 (1.0)              4       20000
test_benchmark_set_attrs_A     13,496.0524 (38.69)    912.2178 (13.64)            4       20000
-----------------------------------------------------------------------------------------------
```


## Features and bugs

Please file feature requests and bugs at the [issue tracker].
Contributions are welcome.

[issue tracker]: https://github.com/simphotonics/lockattrs/issues

[pypi]: https:://pypi.org

[pytest]: https://pypi.org/project/pytest/

[lockattrs]: https://github.com/simphotonics/lockattrs