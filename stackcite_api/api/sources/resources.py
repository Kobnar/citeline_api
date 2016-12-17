from stackcite import data as db

from stackcite_api import api

from . import schema


class SourceDocument(api.resources.APIDocument):

    _update_schema = schema.UpdateSource


class SourceCollection(api.resources.APICollection):

    _collection = db.Source
    _document_resource = SourceDocument

    _create_schema = schema.CreateSource


class TextSourceDocument(api.resources.APIDocument):

    _update_schema = schema.UpdateTextSource


class TextSourceCollection(api.resources.APICollection):

    _collection = db.TextSource
    _document_resource = TextSourceDocument

    _create_schema = schema.CreateTextSource


class BookSourceDocument(api.resources.APIDocument):

    _update_schema = schema.UpdateBookSource


class BookSourceCollection(api.resources.APICollection):

    _collection = db.BookSource
    _document_resource = BookSourceDocument

    _create_schema = schema.CreateBookSource
