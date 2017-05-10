from marshmallow import Schema, fields

from stackcite.api.schema import (
    fields as api_fields
)

from stackcite.api.index.users import schema as user_schema


class ConfirmToken(Schema):
    key = api_fields.AuthTokenKeyField()
    user = fields.Nested(user_schema.User)
    issued = fields.DateTime()


class CreateConfirmationToken(Schema):
    email = fields.Email(required=True)


class UpdateConfirmationToken(Schema):
    key = api_fields.AuthTokenKeyField(required=True)
