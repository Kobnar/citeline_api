from stackcite import data as db

from stackcite_api import resources

from . import schema


class PublisherDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdatePublisher
    }


class PublisherCollection(resources.APICollection):

    _COLLECTION = db.Publisher
    _DOCUMENT_RESOURCE = PublisherDocument

    _SCHEMA = {
        'POST': schema.CreatePublisher
    }


class OrganizationDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateOrganization
    }


class OrganizationCollection(resources.APICollection):

    _COLLECTION = db.Organization
    _DOCUMENT_RESOURCE = OrganizationDocument

    _OFFSPRING = {
        'publishers': PublisherCollection
    }

    _SCHEMA = {
        'POST': schema.CreateOrganization
    }
