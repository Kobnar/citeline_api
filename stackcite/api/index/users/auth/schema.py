from marshmallow import Schema, fields, validates_schema, ValidationError

from stackcite.api.schema import fields as api_fields


class Authenticate(Schema):
    email = fields.Email(required=True)
    password = api_fields.PasswordField(required=True)


class AuthToken(Schema):
    key = api_fields.AuthTokenKeyField(required=True)
