from stackcite import data as db

from stackcite_api import api

from . import schema


class OrganizationDocument(api.resources.APIDocument):

    _update_schema = schema.UpdateOrganization


class OrganizationCollection(api.resources.APICollection):

    _collection = db.Organization
    _document_resource = OrganizationDocument

    _create_schema = schema.CreateOrganization


class PublisherDocument(api.resources.APIDocument):

    _update_schema = schema.UpdatePublisher


class PublisherCollection(api.resources.APICollection):

    _collection = db.Publisher
    _document_resource = PublisherDocument

    _create_schema = schema.CreatePublisher
