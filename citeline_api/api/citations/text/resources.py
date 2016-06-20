from citeline import data as db

from citeline_api import api

from . import schemas


class TextCitationDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdateTextCitation


class TextCitationCollection(api.resources.APICollection):

    _collection = db.TextCitation
    _document_resource = TextCitationDocument

    _create_schema = schemas.CreateTextCitation
    _retrieve_schema = api.schemas.forms.RetrieveCollection
