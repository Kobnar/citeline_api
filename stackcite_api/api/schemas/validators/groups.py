from marshmallow import validate

from stackcite.data.validators.groups import validate_group


class GroupValidator(validate.Validator):
    """
    A ``marshmallow`` style :class:`bson.User` group validator. Raises
    :class:`marshmallow.ValidationError` if the string provided is not a valid
    :class:`bson.User` group.
    """

    default_message = 'Invalid group: {}'

    def __init__(self, error=None):
        self.error = error or self.default_message

    def _format_error(self, value):
        return self.error.format(value)

    def __call__(self, value):
        message = self._format_error(value)
        if not validate_group(value):
            raise validate.ValidationError(message)
