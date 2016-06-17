from citeline import data as db

from citeline_api import api

from . import schemas


class BookSourceDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateBookSource


class BookSourceCollection(api.resources.APICollection):

    _collection = db.BookSource
    _document_resource = BookSourceDocument

    _create_schema = schemas.CreateBookSource
    _retrieve_schema = api.schemas.forms.RetrieveCollection
