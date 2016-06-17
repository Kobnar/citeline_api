from . import resources, schemas, views
from . import people


def traversal_factory(parent, name):
    api_index = resources.APIIndex(parent, name)
    api_index['people'] = people.traversal_factory(api_index, 'people')
    return api_index
