from stackcite import data as db

from stackcite.api import resources

from . import schema


class BookCitationDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdateBookCitation
    }


class BookCitationCollection(resources.APICollectionResource):

    _COLLECTION = db.BookCitation
    _DOCUMENT_RESOURCE = BookCitationDocument

    _SCHEMA = {
        'POST': schema.CreateBookCitation
    }


class TextCitationDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdateTextCitation
    }


class TextCitationCollection(resources.APICollectionResource):

    _COLLECTION = db.TextCitation
    _DOCUMENT_RESOURCE = TextCitationDocument

    _SCHEMA = {
        'POST': schema.CreateTextCitation
    }


class CitationDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdateCitation
    }


class CitationCollection(resources.APICollectionResource):

    _COLLECTION = db.Citation
    _DOCUMENT_RESOURCE = CitationDocument

    _SCHEMA = {
        'POST': schema.CreateCitation
    }