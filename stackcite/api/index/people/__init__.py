from .resources import (
    PersonCollection,
    PersonDocument
)


def traversal_factory(parent, name):
    return PersonCollection(parent, name)
