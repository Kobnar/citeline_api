import unittest

from stackcite.api import testing


class AuthTokenKeyValidatorTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..keys import AuthTokenKeyValidator
        self.validator = AuthTokenKeyValidator()

    def test_invalid_keys_raise_exception(self):
        """AuthTokenKeyValidator raises exception for invalid keys
        """
        from marshmallow import ValidationError
        invalid_keys = testing.data.invalid_keys()
        for key in invalid_keys:
            with (self.assertRaises(ValidationError)):
                self.validator(key)

    def test_valid_keys_dont_raise_exception(self):
        """AuthTokenKeyValidator does not raise exception for valid keys
        """
        from marshmallow import ValidationError
        valid_keys = testing.data.valid_keys()
        for key in valid_keys:
            try:
                self.validator(key)
            except ValidationError:
                msg = 'Valid key failed validation: {}'.format(key)
                self.fail(msg)
