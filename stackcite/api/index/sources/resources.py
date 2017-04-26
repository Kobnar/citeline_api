from stackcite import data as db

from stackcite.api import resources

from . import schema


class BookSourceDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdateSource
    }


class BookSourceCollection(resources.APICollectionResource):

    _COLLECTION = db.BookSource
    _DOCUMENT_RESOURCE = BookSourceDocument

    _SCHEMA = {
        'POST': schema.CreateSource
    }


class TextSourceDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdateSource
    }


class TextSourceCollection(resources.APICollectionResource):

    _COLLECTION = db.TextSource
    _DOCUMENT_RESOURCE = TextSourceDocument

    _OFFSPRING = {
        'books': BookSourceCollection
    }

    _SCHEMA = {
        'POST': schema.CreateSource
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
        'POST': schema.CreateSource,
        'GET': schema.RetrieveSources
    }

    def _retrieve(self, query):
        # Converts "q" field into a case-insensitive regex query
        q = query.pop('q', None)
        if q:
            query.update({
                'title': {
                    '$regex': q.lower(),
                    '$options': 'i'
                }
            })
