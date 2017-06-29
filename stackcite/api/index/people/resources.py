from stackcite import data as db

from stackcite.api import resources

from . import schema


class PersonDocument(resources.APIDocumentResource):

    _DOCUMENT_SCHEMA = schema.Person
    _SCHEMA = schema.Person


class PersonCollection(resources.APICollectionResource):

    _COLLECTION = db.Person
    _DOCUMENT_RESOURCE = PersonDocument

    _SCHEMA = schema.Person

    def _retrieve(self, query):
        # TODO: It has been said this will lead to heat death at scale.
        if query:
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
