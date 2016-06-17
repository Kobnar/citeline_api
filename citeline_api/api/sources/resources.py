from citeline import data as db

from citeline_api import api

from . import schemas


class SourceDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateSource


class SourceCollection(api.resources.APICollection):

    _collection = db.Source
    _document_resource = SourceDocument

    _create_schema = schemas.CreateSource
    _retrieve_schema = api.schemas.forms.RetrieveCollection
