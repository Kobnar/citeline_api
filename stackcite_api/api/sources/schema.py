from marshmallow import Schema, fields, validates, ValidationError

from stackcite import data as db

from stackcite_api.api.schema import fields as api_fields


class _MediumChoices(object):

    medium = fields.String(
        default='PRINT', validate=lambda m: m in db.Source.MEDIUMS)

    # @validates('medium')
    # def validate_medium(self, data):
    #     if data not in db.Source.MEDIUMS:
    #         msg = '{} is an invalid medium'
    #         raise ValidationError(msg.format(data))


class UpdateSource(Schema, _MediumChoices):
    title = fields.String()
    description = fields.String()


class CreateSource(Schema, _MediumChoices):
    title = fields.String(required=True)
    description = fields.String()


class UpdateTextSource(Schema, _MediumChoices):
    title = fields.String()
    description = fields.String()
    authors = fields.List(api_fields.ObjectIdField())
    editors = fields.List(api_fields.ObjectIdField())


class CreateTextSource(Schema, _MediumChoices):
    title = fields.String(required=True)
    description = fields.String()
    authors = fields.List(api_fields.ObjectIdField(), required=True)
    editors = fields.List(api_fields.ObjectIdField())


class UpdateBookSource(Schema, _MediumChoices):
    title = fields.String()
    description = fields.String()
    authors = fields.List(api_fields.ObjectIdField())
    editors = fields.List(api_fields.ObjectIdField())
    edition = fields.String()
    publisher = api_fields.ObjectIdField()
    published = fields.Integer()
    location = fields.String()
    isbn10 = api_fields.ISBN10Field()
    isbn13 = api_fields.ISBN13Field()


class CreateBookSource(Schema, _MediumChoices):
    title = fields.String(required=True)
    description = fields.String()
    authors = fields.List(api_fields.ObjectIdField(), required=True)
    editors = fields.List(api_fields.ObjectIdField())
    edition = fields.String()
    publisher = api_fields.ObjectIdField()
    published = fields.Integer()
    location = fields.String()
    isbn10 = api_fields.ISBN10Field()
    isbn13 = api_fields.ISBN13Field()
