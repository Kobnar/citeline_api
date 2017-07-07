from marshmallow import fields

from . import validators


class AuthTokenKeyField(fields.String):
    """
    A field that validates authentication tokens.

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
    A field that validates :class:`bson.ObjectId` keys.

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
    A field that validates username strings.

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
    A field that validates secure passwords.

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


class GroupField(fields.String):
    """
    A field that validates group names.

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


class ISBN10Field(fields.String):
    """
    A field that validates ISBN-10 values.

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


class ISBN13Field(fields.String):
    """
    A field that validates ISBN-13 values.

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
    A field that converts an API signature list (e.g. ``'this,that'``) into a
    python list (e.g. ``['this', 'that']``).

    :param args: The same positional arguments that
        :class:`marshmallow.fields.String` receives.
    :param kwargs: The same keyword arguments that
        :class:`marshmallow.fields.String` receives.
    """
    def _deserialize(self, value, attr, data):
        if not value:
            value = []
        else:
            value = value.split(',')
        return super()._deserialize(value, attr, data)


class FieldsField(fields.Field):
    """
    A field that converts an API signature list of field names (e.g.
    ``'person__name__first,person__birth'``) into a python list of field names,
    specified with dot-notation (e.g. ``['person.name.first',
    'person.birth']``).
    """
    def _deserialize(self, value, attr, data):
        # TODO: Inherit from ListField?
        if not value:
            return []
        else:
            return value.replace('__', '.').split(',')
