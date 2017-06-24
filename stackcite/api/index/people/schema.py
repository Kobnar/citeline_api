from marshmallow import Schema, fields, validates_schema, ValidationError

from stackcite.api.schema import schema as api_schema


class Name(api_schema.APISchema):
    title = fields.String()
    first = fields.String()
    middle = fields.String()
    last = fields.String()
    full = fields.String()

    @validates_schema
    def validate_schema(self, data):
        if self.method is 'POST':
            self.validate_mutually_exclusive_names(data)
            self.validate_required_names(data)

        elif self.method is 'PUT':
            self.validate_mutually_exclusive_names(data)

    @staticmethod
    def validate_mutually_exclusive_names(data):
        """
        Requires either `full` or individual names may be set, but not both.
        """
        full_name = data.get('full')
        sub_names = data.get('first') or data.get('middle') or data.get('last')
        if full_name and sub_names:
            msg = 'Cannot set "first", "middle", or "last" if "full" is set'
            raise ValidationError(msg, ['full'])

    @staticmethod
    def validate_required_names(data):
        """
        Requires one of `title`, `last`, or `full` must be set in addition to
        :class:`~UpdateName` validation.
        """
        title = data.get('title')
        last_name = data.get('last')
        full_name = data.get('full')
        if not (title or last_name or full_name):
            msg = 'One of "title", "last", or "full" must be set'
            raise ValidationError(msg, ['title', 'last', 'full'])


class Person(api_schema.APIDocumentSchema):
    name = fields.Nested(Name)
    description = fields.String()
    birth = fields.Integer(allow_none=True)
    death = fields.Integer(allow_none=True)

    @validates_schema
    def validate_schema(self, data):
        if self.method is 'POST' and 'name' not in data:
            msg = 'Missing data for required field.'
            raise ValidationError(msg, ['name'])
