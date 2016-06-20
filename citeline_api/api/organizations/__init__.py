from . import resources, views, schemas


def traversal_factory(parent, name):
    org_api = resources.OrganizationCollection(parent, name)
    org_api['publishers'] = resources.PublisherCollection(org_api, 'publishers')
    return org_api
