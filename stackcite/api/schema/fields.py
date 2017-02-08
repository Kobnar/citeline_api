from marshmallow import fields

from . import validators


class AuthTokenKeyField(fields.String):
    """
    A AuthToken key field that automatically validates its content.

    :param args: The same positional arguments that
        :class:`marshmallow.fields.String` receives.
    :param kwargs: The same keyword arguments that
        :class:`marshmallow.fields.String` receives.
    """
    default_error_messages = {'invalid': 'Not a valid API token key.'}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # Insert validation into self.validators so that multiple errors can be
        # stored.
        self.validators.insert(0, validators.keys.AuthTokenKeyValidator(
            error=self.error_messages['invalid']))


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


class ISBN10Field(fields.String):
    """
    An ISBN-10 field that automatically validates its content.

    :param args: The same positional arguments that
        :class:`marshmallow.fields.String` receives.
    :param kwargs: The same keyword arguments that
        :class:`marshmallow.fields.String` receives.
    """
    default_error_messages = {'invalid': 'Not a valid ISBN-10.'}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # Insert validation into self.validators so that multiple errors can be
        # stored.
        self.validators.insert(0, validators.isbns.ISBN10Validator(
            error=self.error_messages['invalid']))


class GroupField(fields.String):
    """
    A user group name.

    :param args: The same positional arguments that
        :class:`marshmallow.fields.String` receives.
    :param kwargs: The same keyword arguments that
        :class:`marshmallow.fields.String` receives.
    """
    default_error_messages = {'invalid': 'Not a valid group'}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # Insert validation into self.validators so that multiple errors can be
        # stored.
        self.validators.insert(0, validators.groups.GroupValidator(
            error=self.error_messages['invalid']))


class ISBN13Field(fields.String):
    """
    An ISBN-13 field that automatically validates its content.

    :param args: The same positional arguments that
        :class:`marshmallow.fields.String` receives.
    :param kwargs: The same keyword arguments that
        :class:`marshmallow.fields.String` receives.
    """
    default_error_messages = {'invalid': 'Not a valid ISBN-13.'}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # Insert validation into self.validators so that multiple errors can be
        # stored.
        self.validators.insert(0, validators.isbns.ISBN13Validator(
            error=self.error_messages['invalid']))


class ListField(fields.List):
    """
    A list of values.
    """
    def _deserialize(self, value, attr, data):
        if not value:
            value = []
        else:
            value = value.split(',')
        return super()._deserialize(value, attr, data)


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
