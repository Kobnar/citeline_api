from marshmallow import validate

from citeline.data.validators.usernames import validate_username


class UsernameValidator(validate.Validator):
    """
    A ``marshmallow`` style :class:`bson.Username` validator. Raises
    :class:`marshmallow.ValidationError` if the string provided is not a valid
    :class:`bson.Username`.
    """

    default_message = 'Invalid password: {}'

    def __init__(self, error=None):
        self.error = error or self.default_message

    def _format_error(self, value):
        return self.error.format(value)

    def __call__(self, value):
        message = self._format_error(value)
        if not validate_username(value):
            raise validate.ValidationError(message)
