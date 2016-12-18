from stackcite import data as db

from stackcite_api import api

from . import schema


class PersonDocument(api.resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdatePerson
    }


class PersonCollection(api.resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreatePerson
    }

    _COLLECTION = db.Person
    _DOCUMENT_RESOURCE = PersonDocument
