from citeline import data as db

from citeline_api import api

from . import schemas


class CitationDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateCitation


class CitationCollection(api.resources.APICollection):

    _collection = db.Citation
    _document_resource = CitationDocument

    _create_schema = schemas.CreateCitation
    _retrieve_schema = api.schemas.forms.RetrieveCollection


class TextCitationDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateTextCitation


class TextCitationCollection(api.resources.APICollection):

    _collection = db.TextCitation
    _document_resource = TextCitationDocument

    _create_schema = schemas.CreateTextCitation
    _retrieve_schema = api.schemas.forms.RetrieveCollection


class BookCitationDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateBookCitation


class BookCitationCollection(api.resources.APICollection):

    _collection = db.BookCitation
    _document_resource = BookCitationDocument

    _create_schema = schemas.CreateBookCitation
    _retrieve_schema = api.schemas.forms.RetrieveCollection
