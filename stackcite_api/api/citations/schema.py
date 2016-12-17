from marshmallow import Schema, fields

from stackcite_api.api.schema import fields as api_fields


class UpdateCitation(Schema):
    source = api_fields.ObjectIdField()
    note = fields.String()


class CreateCitation(Schema):
    source = api_fields.ObjectIdField(required=True)
    note = fields.String()


class UpdateTextCitation(Schema):
    source = api_fields.ObjectIdField()
    note = fields.String()
    text = fields.String()


class CreateTextCitation(Schema):
    source = api_fields.ObjectIdField(required=True)
    note = fields.String()
    text = fields.String(required=True)


class UpdateBookCitation(Schema):
    source = api_fields.ObjectIdField()
    note = fields.String()
    text = fields.String()
    pages = fields.List(fields.Integer())


class CreateBookCitation(Schema):
    source = api_fields.ObjectIdField(required=True)
    note = fields.String()
    text = fields.String(required=True)
    pages = fields.List(fields.Integer())

