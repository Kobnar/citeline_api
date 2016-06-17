from . import resources, schemas, views
from . import people
from . import organizations as orgs


def traversal_factory(parent, name):
    api_index = resources.APIIndex(parent, name)
    api_index['people'] = people.traversal_factory(api_index, 'people')
    api_index['organizations'] = orgs.traversal_factory(
        api_index, 'organizations')
    return api_index
