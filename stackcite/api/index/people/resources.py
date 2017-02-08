from stackcite import data as db

from stackcite.api import resources

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
        # TODO: It has been said this will lead to heat death at scale.
        q = query.pop('q', None)
        if q:
            query.update({
                '$or': [
                    {
                        'name.title': {
                            '$regex': q.lower(),
                            '$options': 'i'
                        }
                    },
                    {
                        'name.full': {
                            '$regex': q.lower(),
                            '$options': 'i'
                        }
                    }
                ]

            })
