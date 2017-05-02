from .resources import (
    OrganizationCollection,
    OrganizationDocument,
    PublisherCollection,
    PublisherDocument
)


def traversal_factory(parent, name):
    organizations = OrganizationCollection(parent, name)
    organizations['publishers'] = PublisherCollection
    return organizations
