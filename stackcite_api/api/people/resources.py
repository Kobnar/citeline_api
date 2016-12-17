from stackcite import data as db

from stackcite_api import api

from . import schema


class PersonDocument(api.resources.APIDocument):

    _schema = {
        'PUT': schema.UpdatePerson
    }


class PersonCollection(api.resources.APICollection):

    _schema = {
        'POST': schema.CreatePerson
    }

    _collection = db.Person
    _document_resource = PersonDocument
