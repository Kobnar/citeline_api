from .resources import (
    OrganizationCollection,
    OrganizationDocument,
    PublisherCollection,
    PublisherDocument
)


ENDPOINTS = (
    OrganizationCollection,
    OrganizationDocument,
    PublisherCollection,
    PublisherDocument
)


def traversal_factory(parent, name):
    parent[name] = resources.OrganizationCollection(parent, name)
    parent[name]['publishers'] = resources.PublisherCollection(parent[name], 'publishers')
    return parent
