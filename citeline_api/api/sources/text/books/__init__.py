from . import resources, views, schemas


def traversal_factory(parent, name):
    return resources.BookSourceCollection(parent, name)
