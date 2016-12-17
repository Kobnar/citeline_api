from stackcite import data as db

from stackcite_api import api

from . import schema


class OrganizationDocument(api.resources.APIDocument):

    _schema = {
        'PUT': schema.UpdateOrganization
    }


class OrganizationCollection(api.resources.APICollection):

    _schema = {
        'POST': schema.CreateOrganization
    }

    _collection = db.Organization
    _document_resource = OrganizationDocument


class PublisherDocument(api.resources.APIDocument):

    _schema = {
        'PUT': schema.UpdatePublisher
    }


class PublisherCollection(api.resources.APICollection):

    _schema = {
        'POST': schema.CreatePublisher
    }

    _collection = db.Publisher
    _document_resource = PublisherDocument
