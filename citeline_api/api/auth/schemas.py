from marshmallow import Schema, fields

from citeline_api.api.schemas import fields as api_fields


class Authenticate(Schema):
    email = fields.Email(required=True)
    password = api_fields.PasswordField(required=True)


class Token(Schema):
    token = api_fields.TokenKeyField(required=True)
