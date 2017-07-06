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
    A base schema for validating queries and deserializing documents.
    """

    # Query request fields
    fields = api_fields.FieldsField(load_only=True)

    # Document response fields
    id = api_fields.ObjectIdField(dump_only=True)


class APICollectionSchema(APISchema):
    """
    A general schema for validating collection-level queries.
    """

    # TODO: Encapsulate document serialization.

    # Query request fields
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
    fields = api_fields.FieldsField(load_only=True)


class RetrieveCollection(Schema):
    # DEPRECIATED
    pass
