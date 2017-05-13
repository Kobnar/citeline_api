from marshmallow import (
    Schema,
    fields as mm_fields
)

from . import fields as api_fields


API_METHODS = ('POST', 'GET', 'PUT', 'DELETE')


class APISchema(Schema):
    """
    A default schema class that stores a "method" context, used to enforce
    method-specific requirements on an API schema.
    """

    def __init__(self, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: Depreciate this pattern (might mess with nested schemas) (?)
        if method:
            self.method = method

    @property
    def method(self):
        return self.context.get('method')

    @method.setter
    def method(self, value):
        if value and value not in API_METHODS:
            msg = 'Invalid request method: {}'.format(value)
            raise ValueError(msg)
        self.context['method'] = value


class APICollectionSchema(APISchema):
    """
    A default validation schema to query operations for a MongoDB collection.
    The fields in this schema only apply to "loading" request data and should
    only be used for retrieving a collection or individual documents.

    By default, schema sets both `limit=100` and `skip=0` to avoid massive
    database dumps.
    """

    q = mm_fields.String(load_only=True)
    ids = api_fields.ListField(api_fields.ObjectIdField, load_only=True)
    fields = api_fields.FieldsField(load_only=True)
    limit = mm_fields.Integer(
        missing=100,
        validate=mm_fields.validate.Range(min=1),
        load_only=True)
    skip = mm_fields.Integer(
        missing=0,
        validate=mm_fields.validate.Range(min=0),
        load_only=True)
