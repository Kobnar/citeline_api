from marshmallow import (
    Schema,
    fields,
    validates,
    validates_schema,
    ValidationError
)

from stackcite.data import User

from stackcite.api.schema import fields as api_fields


def _validate_default_groups(value):
    for default_group in User.DEFAULT_GROUPS:
        if default_group not in value:
            msg = 'Default group missing: {} not in {}'.format(
                default_group, value)
            raise ValidationError(msg)


class UpdateUser(Schema):
    email = fields.Email()
    password = api_fields.PasswordField()
    groups = fields.List(api_fields.GroupField())
    new_password = api_fields.PasswordField()

    @validates('groups')
    def validate_groups(self, value):
        _validate_default_groups(value)

    @validates_schema
    def validate_new_password(self, data):
        new_password = data.get('new_password')
        password = data.get('password')
        if new_password and not password:
            msg = 'Setting a new password requires the existing password'
            raise ValidationError(msg, ['new_password'])


class CreateUser(Schema):
    email = fields.Email(required=True)
    password = api_fields.PasswordField(required=True)
    groups = fields.List(api_fields.GroupField())

    @validates('groups')
    def validate_groups(self, value):
        _validate_default_groups(value)
