from stackcite import data as db

from stackcite_api import api

from . import schema


class SourceDocument(api.resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateSource
    }


class SourceCollection(api.resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreateSource
    }

    _COLLECTION = db.Source
    _DOCUMENT_RESOURCE = SourceDocument


class TextSourceDocument(api.resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateTextSource
    }


class TextSourceCollection(api.resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreateTextSource
    }

    _COLLECTION = db.TextSource
    _DOCUMENT_RESOURCE = TextSourceDocument


class BookSourceDocument(api.resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateBookSource
    }


class BookSourceCollection(api.resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreateBookSource
    }

    _COLLECTION = db.BookSource
    _DOCUMENT_RESOURCE = BookSourceDocument
