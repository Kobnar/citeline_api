from citeline import data as db

from citeline_api import api

from . import schemas


class OrganizationDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateOrganization


class OrganizationCollection(api.resources.APICollection):

    _collection = db.Organization
    _document_resource = OrganizationDocument

    _create_schema = schemas.CreateOrganization
    _retrieve_schema = api.schemas.forms.RetrieveCollection
