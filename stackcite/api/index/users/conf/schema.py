from marshmallow import Schema, fields

from stackcite.api.schema import fields as api_fields


class CreateConfirmationToken(Schema):
    email = fields.Email(required=True)


class UpdateConfirmationToken(Schema):
    key = api_fields.AuthTokenKeyField(required=True)
