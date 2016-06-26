from . import resources, views, schemas


def traversal_factory(parent, name):
    parent[name] = resources.AuthResource(parent, name)
    return parent
