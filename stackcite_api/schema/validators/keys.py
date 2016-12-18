from marshmallow import validate

from stackcite.data.validators.keys import validate_key


class TokenKeyValidator(validate.Validator):
    """
    A ``marshmallow`` style :class:`bson.Token` key validator. Raises
    :class:`marshmallow.ValidationError` if the string provided is not a valid
    :class:`bson.Token` key.
    """

    default_message = 'Invalid API token key: {}'

    def __init__(self, error=None):
        self.error = error or self.default_message

    def _format_error(self, value):
        return self.error.format(value)

    def __call__(self, value):
        message = self._format_error(value)
        if not validate_key(value):
            raise validate.ValidationError(message)
