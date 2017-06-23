# Style Guide

***Note:*** *This style guide is the development of experimentation. Many parts
of this project have not been updated to reflect these practices. Please fix
them when you see them.*

## Naming

### Naming Data (variables, properties, attributes, etc.)

#### Class constants should be defined in all-caps...

```python
class SomeClass(object):
    SOME_CONSTANT = 'This never changes, unless overridden by a child class.'
```

### Naming Classes

#### Indicate interface classes w/ prefix `I`...

```python
class IMovable(object):

    SPEED = NotImplemented
    
    def move(self, direction):
        raise NotImplementedError()
```

#### Indicate abstract classes w/ prefix `A`...

```python
class ANameable(object):

    def __init__(self, name):
        self._name = self.validate(name)
        
    @staticmethod
    def validate(name):
        if not isinstance(name, str):
            raise TypeError()
        return name
    
    @property
    def name(self):
        return self._name
```

## Commenting

#### Use docstrings to explain each test...

```python
import unittest

class SomeTestCase(unittest.TestCase):
    
    def test_method_does_some_thing(self):
    """SomeClass.method() does something
    """
    # ...
    
    def test_property_is_something(self):
    """SomeClass.property is something
    """
    # ...
```

## Testing

### Structuring Test Cases

#### Generalize repetitive tasks into parent test cases...

```python
import unittest

class ParentTestCase(unittest.TestCase):

    def make_test_data(self):
        # Generate some generalized data for testing

class ChildTestCase(ParentTestCase):
    
    def test_data(self):
        data = self.make_test_data()
        # Do something with generalized test data
```

### Importing Dependencies

#### Explicitly define `expected` and `result` (where applicable)...

#### Import libraries for each test when needed...
