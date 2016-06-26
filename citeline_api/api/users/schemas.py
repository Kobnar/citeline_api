from marshmallow import Schema, fields

from citeline_api.api.schemas import fields as api_fields


class UpdateUser(Schema):
    email = fields.Email()
    password = api_fields.PasswordField()


class CreateUser(Schema):
    email = fields.Email(required=True)
    password = api_fields.PasswordField(required=True)
