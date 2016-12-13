from stackcite import data as db

from stackcite_api import api

from . import schemas


class SourceDocument(api.resources.APIDocument):

    _update_schema = schemas.UpdateSource


class SourceCollection(api.resources.APICollection):

    _collection = db.Source
    _document_resource = SourceDocument

    _create_schema = schemas.CreateSource


class TextSourceDocument(api.resources.APIDocument):

    _update_schema = schemas.UpdateTextSource


class TextSourceCollection(api.resources.APICollection):

    _collection = db.TextSource
    _document_resource = TextSourceDocument

    _create_schema = schemas.CreateTextSource


class BookSourceDocument(api.resources.APIDocument):

    _update_schema = schemas.UpdateBookSource


class BookSourceCollection(api.resources.APICollection):

    _collection = db.BookSource
    _document_resource = BookSourceDocument

    _create_schema = schemas.CreateBookSource
