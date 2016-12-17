from stackcite import data as db

from stackcite_api import api

from . import schema


class CitationDocument(api.resources.APIDocument):

    _update_schema = schema.UpdateCitation


class CitationCollection(api.resources.APICollection):

    _collection = db.Citation
    _document_resource = CitationDocument

    _create_schema = schema.CreateCitation


class TextCitationDocument(api.resources.APIDocument):

    _update_schema = schema.UpdateTextCitation


class TextCitationCollection(api.resources.APICollection):

    _collection = db.TextCitation
    _document_resource = TextCitationDocument

    _create_schema = schema.CreateTextCitation


class BookCitationDocument(api.resources.APIDocument):

    _update_schema = schema.UpdateBookCitation


class BookCitationCollection(api.resources.APICollection):

    _collection = db.BookCitation
    _document_resource = BookCitationDocument

    _create_schema = schema.CreateBookCitation
