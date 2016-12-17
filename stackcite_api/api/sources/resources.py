from stackcite import data as db

from stackcite_api import api

from . import schema


class SourceDocument(api.resources.APIDocument):

    _schema = {
        'PUT': schema.UpdateSource
    }


class SourceCollection(api.resources.APICollection):

    _schema = {
        'POST': schema.CreateSource
    }

    _collection = db.Source
    _document_resource = SourceDocument


class TextSourceDocument(api.resources.APIDocument):

    _schema = {
        'PUT': schema.UpdateTextSource
    }


class TextSourceCollection(api.resources.APICollection):

    _schema = {
        'POST': schema.CreateTextSource
    }

    _collection = db.TextSource
    _document_resource = TextSourceDocument


class BookSourceDocument(api.resources.APIDocument):

    _schema = {
        'PUT': schema.UpdateBookSource
    }


class BookSourceCollection(api.resources.APICollection):

    _schema = {
        'POST': schema.CreateBookSource
    }

    _collection = db.BookSource
    _document_resource = BookSourceDocument
