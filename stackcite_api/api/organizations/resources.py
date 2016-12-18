from stackcite import data as db

from stackcite_api import resources

from . import schema


class OrganizationDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateOrganization
    }


class OrganizationCollection(resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreateOrganization
    }

    _COLLECTION = db.Organization
    _DOCUMENT_RESOURCE = OrganizationDocument


class PublisherDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdatePublisher
    }


class PublisherCollection(resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreatePublisher
    }

    _COLLECTION = db.Publisher
    _DOCUMENT_RESOURCE = PublisherDocument
