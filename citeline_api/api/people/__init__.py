from . import resources, views, schemas


def traversal_factory(parent, name):
    parent[name] = resources.PersonCollection(parent, name)
    return parent
