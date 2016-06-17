from marshmallow import fields

from . import validators


class ObjectIdField(fields.String):
    """
    An ObjectId field that automatically validates its content.

    :param args: The same positional arguments that
        :class:`marshmallow.fields.String` receives.
    :param kwargs: The same keyword arguments that
        :class:`marshmallow.fields.String` receives.
    """
    default_error_messages = {'invalid': 'Not a valid BSON-style ObjectId.'}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # Insert validation into self.validators so that multiple errors can be
        # stored.
        self.validators.insert(0, validators.oids.ObjectIdValidator(
            error=self.error_messages['invalid']))


class UsernameField(fields.String):
    """
    A Username field that automatically validates its content.

    :param args: The same positional arguments that
        :class:`marshmallow.fields.String` receives.
    :param kwargs: The same keyword arguments that
        :class:`marshmallow.fields.String` receives.
    """
    default_error_messages = {'invalid': 'Not a valid username.'}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # Insert validation into self.validators so that multiple errors can be
        # stored.
        self.validators.insert(0, validators.usernames.UsernameValidator(
            error=self.error_messages['invalid']))


class PasswordField(fields.String):
    """
    A Password field that automatically validates its content.

    :param args: The same positional arguments that
        :class:`marshmallow.fields.String` receives.
    :param kwargs: The same keyword arguments that
        :class:`marshmallow.fields.String` receives.
    """
    default_error_messages = {'invalid': 'Not a valid password.'}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # Insert validation into self.validators so that multiple errors can be
        # stored.
        self.validators.insert(0, validators.passwords.PasswordValidator(
            error=self.error_messages['invalid']))


class ListField(fields.Field):
    """
    A list of values.
    """
    def _deserialize(self, value, attr, data):
        if not value:
            return []
        else:
            return value.split(',')


class FieldsField(fields.Field):
    """
    A list of field names.

    NOTE: This schema will automatically convert underscore subfield notation
    into dot notation so it works with back-end resources.
    """
    def _deserialize(self, value, attr, data):
        if not value:
            return []
        else:
            return value.replace('__', '.').split(',')