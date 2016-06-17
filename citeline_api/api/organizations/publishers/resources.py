from citeline import data as db

from citeline_api import api

from . import schemas


class PublisherDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdatePublisher


class PublisherCollection(api.resources.APICollection):

    _collection = db.Publisher
    _document_resource = PublisherDocument

    _create_schema = schemas.CreatePublisher
    _retrieve_schema = api.schemas.forms.RetrieveCollection
