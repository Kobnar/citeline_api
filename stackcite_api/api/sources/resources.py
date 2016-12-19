from stackcite import data as db

from stackcite_api import resources

from . import schema


class BookSourceDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateBookSource
    }


class BookSourceCollection(resources.APICollection):

    _COLLECTION = db.BookSource
    _DOCUMENT_RESOURCE = BookSourceDocument

    _SCHEMA = {
        'POST': schema.CreateBookSource
    }


class TextSourceDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateTextSource
    }


class TextSourceCollection(resources.APICollection):

    _COLLECTION = db.TextSource
    _DOCUMENT_RESOURCE = TextSourceDocument

    _OFFSPRING = {
        'books': BookSourceCollection
    }

    _SCHEMA = {
        'POST': schema.CreateTextSource
    }


class SourceDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateSource
    }


class SourceCollection(resources.APICollection):

    _COLLECTION = db.Source
    _DOCUMENT_RESOURCE = SourceDocument

    _OFFSPRING = {
        'text': TextSourceCollection
    }

    _SCHEMA = {
        'POST': schema.CreateSource
    }
