from citeline import data as db

from citeline_api import api

from . import schemas


class BookCitationDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateBookCitation


class BookCitationCollection(api.resources.APICollection):

    _collection = db.BookCitation
    _document_resource = BookCitationDocument

    _create_schema = schemas.CreateBookCitation
    _retrieve_schema = api.schemas.forms.RetrieveCollection
