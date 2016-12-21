from marshmallow import Schema, fields, validates_schema, ValidationError

from stackcite_api.schema import fields as api_fields


class Authenticate(Schema):
    email = fields.Email()
    password = api_fields.PasswordField()
    key = api_fields.AuthTokenKeyField()

    @validates_schema
    def validate_dependant_fields(self, data):
        err_msg = fields.Field.default_error_messages['required']
        missing_fields = []
        if not data.get('key'):
            if not data.get('email'):
                missing_fields.append('email')
            if not data.get('password'):
                missing_fields.append('password')
        if missing_fields:
            raise ValidationError(err_msg, field_names=missing_fields)


class AuthToken(Schema):
    key = api_fields.AuthTokenKeyField(required=True)
