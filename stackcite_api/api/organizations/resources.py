from stackcite import data as db

from stackcite_api import api

from . import schema


class OrganizationDocument(api.resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateOrganization
    }


class OrganizationCollection(api.resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreateOrganization
    }

    _COLLECTION = db.Organization
    _DOCUMENT_RESOURCE = OrganizationDocument


class PublisherDocument(api.resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdatePublisher
    }


class PublisherCollection(api.resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreatePublisher
    }

    _COLLECTION = db.Publisher
    _DOCUMENT_RESOURCE = PublisherDocument
