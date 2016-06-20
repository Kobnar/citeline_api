from citeline import data as db

from citeline_api import api

from . import schemas


class OrganizationDocument(api.resources.APIDocument):

    _update_schema = schemas.UpdateOrganization


class OrganizationCollection(api.resources.APICollection):

    _collection = db.Organization
    _document_resource = OrganizationDocument

    _create_schema = schemas.CreateOrganization


class PublisherDocument(api.resources.APIDocument):

    _update_schema = schemas.UpdatePublisher


class PublisherCollection(api.resources.APICollection):

    _collection = db.Publisher
    _document_resource = PublisherDocument

    _create_schema = schemas.CreatePublisher
