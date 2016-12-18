from stackcite import data as db

from stackcite_api import resources

from . import schema


class CitationDocument(resources.APIDocument):

    _update_schema = schema.UpdateCitation


class CitationCollection(resources.APICollection):

    _COLLECTION = db.Citation
    _DOCUMENT_RESOURCE = CitationDocument

    _create_schema = schema.CreateCitation


class TextCitationDocument(resources.APIDocument):

    _update_schema = schema.UpdateTextCitation


class TextCitationCollection(resources.APICollection):

    _COLLECTION = db.TextCitation
    _DOCUMENT_RESOURCE = TextCitationDocument

    _create_schema = schema.CreateTextCitation


class BookCitationDocument(resources.APIDocument):

    _update_schema = schema.UpdateBookCitation


class BookCitationCollection(resources.APICollection):

    _COLLECTION = db.BookCitation
    _DOCUMENT_RESOURCE = BookCitationDocument

    _create_schema = schema.CreateBookCitation
