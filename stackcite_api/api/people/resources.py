from stackcite import data as db

from stackcite_api import api

from . import schema


class PersonDocument(api.resources.APIDocument):

    _update_schema = schema.UpdatePerson


class PersonCollection(api.resources.APICollection):

    _collection = db.Person
    _document_resource = PersonDocument

    _create_schema = schema.CreatePerson
