from . import resources, views, schemas
from . import publishers as pubs


def traversal_factory(parent, name):
    org_api = resources.OrganizationCollection(parent, name)
    org_api['publishers'] = pubs.traversal_factory(org_api, 'publishers')
    return org_api
