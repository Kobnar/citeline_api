from marshmallow import validate

from citeline.data.validators.passwords import validate_password


class PasswordValidator(validate.Validator):
    """
    A ``marshmallow`` style :class:`bson.Password` validator. Raises
    :class:`marshmallow.ValidationError` if the string provided is not a valid
    :class:`bson.Password`.
    """

    default_message = 'Invalid password: {}'

    def __init__(self, error=None):
        self.error = error or self.default_message

    def _format_error(self, value):
        return self.error.format(value)

    def __call__(self, value):
        message = self._format_error(value)
        if not validate_password(value):
            raise validate.ValidationError(message)
