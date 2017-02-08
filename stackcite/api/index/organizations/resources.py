from stackcite import data as db

from stackcite.api import resources

from . import schema


class PublisherDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdatePublisher
    }


class PublisherCollection(resources.APICollectionResource):

    _COLLECTION = db.Publisher
    _DOCUMENT_RESOURCE = PublisherDocument

    _SCHEMA = {
        'POST': schema.CreatePublisher
    }


class OrganizationDocument(resources.APIDocumentResource):

    _SCHEMA = {
        'PUT': schema.UpdateOrganization
    }


class OrganizationCollection(resources.APICollectionResource):

    _COLLECTION = db.Organization
    _DOCUMENT_RESOURCE = OrganizationDocument

    _OFFSPRING = {
        'publishers': PublisherCollection
    }

    _SCHEMA = {
        'POST': schema.CreateOrganization,
        'GET': schema.RetrieveOrganizations
    }

    def _retrieve(self, query):
        # Converts "q" field into a case-insensitive regex query
        q = query.pop('q', None)
        if q:
            query.update({
                'name': {
                    '$regex': q.lower(),
                    '$options': 'i'
                }
            })
