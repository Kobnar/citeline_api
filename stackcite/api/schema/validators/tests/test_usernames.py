import unittest

from stackcite.api import testing


class UsernameValidatorTests(unittest.TestCase):

    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from ..usernames import UsernameValidator
        self.validator = UsernameValidator()

    def test_invalid_usernames_raise_exception(self):
        """UsernameValidator raises exception for invalid usernames
        """
        from marshmallow import ValidationError
        invalid_usernames = testing.data.invalid_usernames()
        for username in invalid_usernames:
            with (self.assertRaises(ValidationError)):
                self.validator(username)

    def test_valid_usernames_dont_raise_exception(self):
        """UsernameValidator does not raise exception for valid usernames
        """
        from marshmallow import ValidationError
        valid_usernames = testing.data.valid_usernames()
        for username in valid_usernames:
            try:
                self.validator(username)
            except ValidationError:
                msg = 'Valid username failed validation: {}'.format(username)
                self.fail(msg)
