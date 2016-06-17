from citeline import data as db

from citeline_api import api

from . import schemas


class PersonDocument(api.resources.APIDocument):

    _retrieve_schema = api.schemas.forms.RetrieveDocument
    _update_schema = schemas.UpdatePerson


class PersonCollection(api.resources.APICollection):

    _collection = db.Person
    _document_resource = PersonDocument

    _create_schema = schemas.CreatePerson
    _retrieve_schema = api.schemas.forms.RetrieveCollection
