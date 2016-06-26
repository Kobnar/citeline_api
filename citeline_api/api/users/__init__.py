from . import resources, views, schemas


def traversal_factory(parent, name):
    parent[name] = resources.UserCollection(parent, name)
    return parent
