from marshmallow import fields, validates_schema, ValidationError

from stackcite.api import schema


class MockDocumentSchema(schema.APICollectionSchema):
    """
    A (de)serialization schema for :class:`~MockDocument`, with matching field
    parameters.

    :cvar name: A string value (required if ``method='POST'``).
    :cvar number: An integer value.
    :cvar fact: A boolean value.
    """

    # TODO: Implement "__gt" and "__lt" query fields
    name = fields.String()
    number = fields.Integer()
    fact = fields.Boolean()

    @validates_schema
    def route_methods(self, data):
        if self.method is 'POST':
            self._validate_required_name_field(data)

    @staticmethod
    def _validate_required_name_field(data):
        if 'name' not in data:
            msg = 'Missing data for required field.'
            raise ValidationError(msg, ['name'])
