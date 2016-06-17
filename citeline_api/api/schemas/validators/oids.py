from marshmallow import validate

from citeline.data.validators.oids import validate_objectid


class ObjectIdValidator(validate.Validator):
    """
    A ``marshmallow`` style :class:`bson.ObjectId` validator. Raises
    :class:`marshmallow.ValidationError` if the string provided is not a valid
    :class:`bson.ObjectId`.
    """

    default_message = 'Invalid ObjectId: {}'

    def __init__(self, error=None):
        self.error = error or self.default_message

    def _format_error(self, value):
        return self.error.format(value)

    def __call__(self, value):
        message = self._format_error(value)
        if not validate_objectid(value):
            raise validate.ValidationError(message)
