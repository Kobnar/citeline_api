from stackcite import data as db

from stackcite_api import resources

from . import schema


class PersonDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdatePerson
    }


class PersonCollection(resources.APICollectionResource):

    _COLLECTION = db.Person
    _DOCUMENT_RESOURCE = PersonDocument

    _SCHEMA = {
        'POST': schema.CreatePerson
    }
