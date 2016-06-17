from citeline import data as db

from citeline_api import api

from . import schemas


class TextSourceDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateTextSource


class TextSourceCollection(api.resources.APICollection):

    _collection = db.TextSource
    _document_resource = TextSourceDocument

    _create_schema = schemas.CreateTextSource
    _retrieve_schema = api.schemas.forms.RetrieveCollection
