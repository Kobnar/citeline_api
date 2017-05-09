from stackcite.api import resources

from . import models, schema


class MockDocumentResource(resources.DocumentResource):
    """
    A "mock" :class:`~DocumentResource` used for testing.
    """


class MockCollectionResource(resources.CollectionResource):
    """
    A "mock" :class:`~CollectionResource` used for testing with
    :class:`~MockDocumentResource` defined as its child and
    :class:`~MockDocument` as its associated MongoDB collection.
    """
    _COLLECTION = models.MockDocument
    _DOCUMENT_RESOURCE = MockDocumentResource


class MockIndexResource(resources.IndexResource):
    """
    A "mock" :class:`~IndexResource` used for testing.
    """


class MockAPIDocumentResource(resources.APIDocumentResource):
    """
    A "mock" :class:`~APIDocumentResource` used for testing with
    :class:`~MockUpdateDocumentSchema` defined as a validation schema for
    'PUT' operations.
    """
    _DOCUMENT_SCHEMA = schema.MockDocumentSchema
    _SCHEMA = {
        'PUT': schema.MockUpdateDocumentSchema,
        'GET': schema.MockRetrieveDocumentSchema
    }


class MockAPICollectionResource(resources.APICollectionResource):
    """
    A "mock" :class:`~APICollectionResource` used for testing with
    :class:`~MockAPIDocumentResource` defined as its child,
    :class:`~MockDocument` as its associated MongoDB collection. and
    :class:`~MockCreateDocumentSchema` defined as a validation schema for
    'POST' operations.
    """
    _COLLECTION = models.MockDocument
    _DOCUMENT_RESOURCE = MockAPIDocumentResource
    _DOCUMENT_SCHEMA = schema.MockDocumentSchema
    _SCHEMA = {
        'POST': schema.MockCreateDocumentSchema,
        'GET': schema.MockRetrieveCollectionSchema}


class MockAPIIndexResource(resources.APIIndexResource):
    """
    A "mock" :class:`~APIIndexResource` used for testing.
    """
