import unittest

from stackcite.api import testing


class PasswordValidatorTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..passwords import PasswordValidator
        self.validator = PasswordValidator()

    def test_invalid_passwords_raise_exception(self):
        """PasswordValidator raises exception for invalid passwords
        """
        from marshmallow import ValidationError
        invalid_passwords = testing.data.invalid_passwords()
        for password in invalid_passwords:
            with (self.assertRaises(ValidationError)):
                self.validator(password)

    def test_valid_passwords_dont_raise_exception(self):
        """PasswordValidator does not raise exception for valid passwords
        """
        from marshmallow import ValidationError
        valid_passwords = testing.data.valid_passwords()
        for password in valid_passwords:
            try:
                self.validator(password)
            except ValidationError:
                msg = 'Valid password failed validation: {}'.format(password)
                self.fail(msg)
