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
        'POST': schema.CreatePerson,
        'GET': schema.RetrievePeople
    }

    def _retrieve(self, query):
        # Converts "q" field into a case-insensitive regex query
        q = query.pop('q', None)
        if q:
            query.update({
                'name.title': {
                    '$regex': q.lower(),
                    '$options': 'i'
                }
            })
