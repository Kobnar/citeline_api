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


class TextSourceDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateTextSource


class TextSourceCollection(api.resources.APICollection):

    _collection = db.TextSource
    _document_resource = TextSourceDocument

    _create_schema = schemas.CreateTextSource
    _retrieve_schema = api.schemas.forms.RetrieveCollection


class BookSourceDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateBookSource


class BookSourceCollection(api.resources.APICollection):

    _collection = db.BookSource
    _document_resource = BookSourceDocument

    _create_schema = schemas.CreateBookSource
    _retrieve_schema = api.schemas.forms.RetrieveCollection
