from marshmallow import fields, validates_schema, ValidationError

from stackcite.api import schema


class MockDocumentSchema(schema.APIDocumentSchema):
    name = fields.String()
    number = fields.Integer()
    fact = fields.Boolean()

    @validates_schema
    def route_methods(self, data):
        if self.method:
            if self.method is 'POST':
                self._validate_required_name_field(data)

    @staticmethod
    def _validate_required_name_field(data):
        if 'name' not in data:
            msg = 'Missing data for required field.'
            raise ValidationError(msg, ['name'])
