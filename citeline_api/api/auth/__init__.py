from .resources import AuthResource


ENDPOINTS = (AuthResource,)


def traversal_factory(parent, name):
    parent[name] = resources.AuthResource
    return parent
