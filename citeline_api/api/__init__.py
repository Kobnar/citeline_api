from . import resources, schemas, views


def traversal_factory(parent, name):
    api_index = resources.APIIndex(parent, name)
    return api_index
