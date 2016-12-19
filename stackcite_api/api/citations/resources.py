from stackcite import data as db

from stackcite_api import resources

from . import schema


class BookCitationDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateBookCitation
    }


class BookCitationCollection(resources.APICollection):

    _COLLECTION = db.BookCitation
    _DOCUMENT_RESOURCE = BookCitationDocument

    _SCHEMA = {
        'POST': schema.CreateBookCitation
    }


class TextCitationDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateTextCitation
    }


class TextCitationCollection(resources.APICollection):

    _COLLECTION = db.TextCitation
    _DOCUMENT_RESOURCE = TextCitationDocument

    _OFFSPRING = {
        'books': BookCitationCollection
    }

    _SCHEMA = {
        'POST': schema.CreateTextCitation
    }


class CitationDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdateCitation
    }


class CitationCollection(resources.APICollection):

    _COLLECTION = db.Citation
    _DOCUMENT_RESOURCE = CitationDocument

    _OFFSPRING = {
        'text': TextCitationCollection
    }

    _SCHEMA = {
        'POST': schema.CreateCitation
    }