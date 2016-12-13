from marshmallow import validate

from stackcite.data.validators.isbns import validate_isbn10, validate_isbn13


class ISBN10Validator(validate.Validator):
    """
    A ``marshmallow`` style :class:`bson.ISBN10` validator. Raises
    :class:`marshmallow.ValidationError` if the string provided is not a valid
    ISBN-10.
    """

    default_message = 'Invalid ISBN-10: {}'

    def __init__(self, error=None):
        self.error = error or self.default_message

    def _format_error(self, value):
        return self.error.format(value)

    def __call__(self, value):
        message = self._format_error(value)
        if not validate_isbn10(value):
            raise validate.ValidationError(message)


class ISBN13Validator(validate.Validator):
    """
    A ``marshmallow`` style :class:`bson.ISBN13` validator. Raises
    :class:`marshmallow.ValidationError` if the string provided is not a valid
    ISBN-13.
    """

    default_message = 'Invalid ISBN-13: {}'

    def __init__(self, error=None):
        self.error = error or self.default_message

    def _format_error(self, value):
        return self.error.format(value)

    def __call__(self, value):
        message = self._format_error(value)
        if not validate_isbn13(value):
            raise validate.ValidationError(message)
