from marshmallow import Schema, fields, validates_schema, ValidationError

from stackcite.api.schema import (
    fields as api_fields,
    schema as api_forms
)


class Name(Schema):
    title = fields.String()
    first = fields.String()
    middle = fields.String()
    last = fields.String()
    full = fields.String()


class Person(Schema):
    id = api_fields.ObjectIdField()
    name = fields.Nested(Name)
    description = fields.String()
    birth = fields.Integer(allow_none=True)
    death = fields.Integer(allow_none=True)


class UpdateName(Schema):

    title = fields.String()
    first = fields.String()
    middle = fields.String()
    last = fields.String()
    full = fields.String()

    @validates_schema
    def validate_names(self, data):
        """
        Requires either `full` or individual names may be set, but not both.
        """
        full_name = data.get('full')
        sub_names = data.get('first') or data.get('middle') or data.get('last')
        if full_name and sub_names:
            msg = 'Cannot set "first", "middle", or "last" if "full" is set'
            raise ValidationError(msg, ['full'])


class CreateName(UpdateName):

    @validates_schema
    def validate_names(self, data):
        """
        Requires one of `title`, `last`, or `full` must be set in addition to
        :class:`~UpdateName` validation.
        """
        super().validate_names(data)
        title = data.get('title')
        last_name = data.get('last')
        full_name = data.get('full')
        if not (title or last_name or full_name):
            msg = 'One of "title", "last", or "full" must be set'
            raise ValidationError(msg, ['title', 'last', 'full'])


class UpdatePerson(Schema):
    name = fields.Nested(UpdateName)
    description = fields.String()
    birth = fields.Integer(allow_none=True)
    death = fields.Integer(allow_none=True)


class CreatePerson(UpdatePerson):
    name = fields.Nested(CreateName, required=True)


class RetrievePeople(api_forms.RetrieveCollection):
    q = fields.String()
