from stackcite import data as db

from stackcite_api import resources

from . import schema


class BookSourceDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdateBookSource
    }


class BookSourceCollection(resources.APICollectionResource):

    _COLLECTION = db.BookSource
    _DOCUMENT_RESOURCE = BookSourceDocument

    _SCHEMA = {
        'POST': schema.CreateBookSource
    }


class TextSourceDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdateTextSource
    }


class TextSourceCollection(resources.APICollectionResource):

    _COLLECTION = db.TextSource
    _DOCUMENT_RESOURCE = TextSourceDocument

    _OFFSPRING = {
        'books': BookSourceCollection
    }

    _SCHEMA = {
        'POST': schema.CreateTextSource
    }


class SourceDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdateSource
    }


class SourceCollection(resources.APICollectionResource):

    _COLLECTION = db.Source
    _DOCUMENT_RESOURCE = SourceDocument

    _OFFSPRING = {
        'text': TextSourceCollection
    }

    _SCHEMA = {
        'POST': schema.CreateSource
    }
