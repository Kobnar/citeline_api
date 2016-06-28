from .resources import (
    PersonCollection,
    PersonDocument
)


ENDPOINTS = (
    PersonCollection,
    PersonDocument
)


def traversal_factory(parent, name):
    parent[name] = resources.PersonCollection(parent, name)
    return parent
