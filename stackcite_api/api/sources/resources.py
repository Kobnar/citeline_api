from stackcite import data as db

from stackcite_api import resources

from . import schema


class SourceDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateSource
    }


class SourceCollection(resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreateSource
    }

    _COLLECTION = db.Source
    _DOCUMENT_RESOURCE = SourceDocument


class TextSourceDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateTextSource
    }


class TextSourceCollection(resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreateTextSource
    }

    _COLLECTION = db.TextSource
    _DOCUMENT_RESOURCE = TextSourceDocument


class BookSourceDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateBookSource
    }


class BookSourceCollection(resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreateBookSource
    }

    _COLLECTION = db.BookSource
    _DOCUMENT_RESOURCE = BookSourceDocument
