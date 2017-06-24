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
    Provides helper setters/getters for common schema contexts (e.g. request
    method).
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
    A default validation schema to perform CRUD operations on a document
    resource.
    """

    # Query request fields
    fields = api_fields.FieldsField(load_only=True)

    # Document response fields
    id = api_fields.ObjectIdField(dump_only=True)


class APICollectionSchema(APISchema):
    """
    A schema designed to coordinate (de)serializing collections of documents,
    based on the context of the request (e.g. method).

    The `load` and `dump` methods of this schema are designed to handle the
    data differently if it is a collection or a single document. If it is a
    single document, both methods will bypass collection-level
    (de)serialization.
    """

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

    # Collection response fields
    # count = mm_fields.Integer(
    #     validate=mm_fields.validate.Range(min=0),
    #     dump_only=True)

    @property
    def document_schema(self):
        return self.context.get('document_schema')

    @document_schema.setter
    def document_schema(self, value):
        if isinstance(value, Schema):
            self.context['document_schema'] = value
        else:
            msg = 'Invalid schema: {}'.format(value)
            raise TypeError(msg)

    def load(self, query, single=None, **kwargs):
        if single:
            return self.document_schema.load(query)
        else:
            return super().load(query)

    def dump(self, data, single=None, **kwargs):
        if single:
            return self.document_schema.dump(data)
        else:
            return super().dump(data)


class RetrieveCollection(Schema):
    pass
