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
