"""
Stackcite API relies on custom schemas to convert user-facing API input into
database-layer queries and CRUD operations.
"""

from marshmallow import (
    Schema,
    fields as mm_fields
)

from . import fields as api_fields


POST = 'POST'
GET = 'GET'
PUT = 'PUT'
DELETE = 'DELETE'
API_METHODS = (POST, GET, PUT, DELETE)


class APISchema(Schema):
    """
    A sub-type of :class:`marshmallow.Schema` that provides a ``method``
    context that can be used to enforce specific schema-wide validation rules
    (e.g. :class:`~Person` requires a ``name`` if the HTTP method is ``POST``).
    """

    @property
    def method(self):
        return self.context.get('method')

    @method.setter
    def method(self, value):
        if value and value not in API_METHODS:
            msg = 'Invalid request method: {}'.format(value)
            raise ValueError(msg)
        self.context['method'] = value


class APIDocumentSchema(APISchema):
    """
    A base schema for (de)serializing documents. Each collection class should
    have its own sub-class of :class:`~APIDocumentSchema` to (de)serialize data
    and objects.
    """

    # Query request fields
    fields = api_fields.FieldsListField(load_only=True)

    # Document response fields
    id = api_fields.ObjectIdField(dump_only=True)


class APICollectionSchema(APISchema):
    """
    A generalized schema for (de)serializing one or more documents.

    *Note: Collection-level response metadata (e.g. limit, skip, and count)
    must be compiled manually in the view method, because schemas are intended
    to be database agnostic.*

    :cvar q: An arbitrary query string (``load_only=True``)
    :cvar ids: A comma-separated list of ids (``load_only=True``)
    :cvar limit: The maximum number of documents returned (``load_only=True``)
    :cvar skip: The total number of documents "skipped" (``load_only=True``)
    :cvar count: The total number of documents found (``dump_only=True``)
    :cvar items: A list containing documents matching query (``dump_only=True``)
    :cvar fields: A comma-separated list of field names to include
        (``load_only=True``)
    :cvar id: An individual document id (``dump_only=True``)
    """

    # Collection-only request fields
    q = mm_fields.String(load_only=True)
    ids = api_fields.ListField(api_fields.ObjectIdField, load_only=True)
    limit = mm_fields.Integer(
        missing=100,
        validate=mm_fields.validate.Range(min=1),
        load_only=True)
    skip = mm_fields.Integer(
        missing=0,
        validate=mm_fields.validate.Range(min=0),
        load_only=True)

    # Document/collection request fields
    fields = api_fields.FieldsListField(load_only=True)

    # Document-only response fields
    id = api_fields.ObjectIdField(dump_only=True)


class RetrieveCollection(Schema):
    # DEPRECIATED
    pass
