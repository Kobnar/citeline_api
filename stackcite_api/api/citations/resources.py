from stackcite import data as db

from stackcite_api import api

from . import schema


class CitationDocument(api.resources.APIDocument):

    _update_schema = schema.UpdateCitation


class CitationCollection(api.resources.APICollection):

    _COLLECTION = db.Citation
    _DOCUMENT_RESOURCE = CitationDocument

    _create_schema = schema.CreateCitation


class TextCitationDocument(api.resources.APIDocument):

    _update_schema = schema.UpdateTextCitation


class TextCitationCollection(api.resources.APICollection):

    _COLLECTION = db.TextCitation
    _DOCUMENT_RESOURCE = TextCitationDocument

    _create_schema = schema.CreateTextCitation


class BookCitationDocument(api.resources.APIDocument):

    _update_schema = schema.UpdateBookCitation


class BookCitationCollection(api.resources.APICollection):

    _COLLECTION = db.BookCitation
    _DOCUMENT_RESOURCE = BookCitationDocument

    _create_schema = schema.CreateBookCitation
