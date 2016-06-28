from .resources import (
    UserCollection,
    UserDocument
)


ENDPOINTS = (
    UserCollection,
    UserDocument
)


def traversal_factory(parent, name):
    parent[name] = resources.UserCollection(parent, name)
    return parent
