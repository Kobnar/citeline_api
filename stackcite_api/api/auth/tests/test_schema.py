import unittest

from stackcite_api import testing


class AuthenticateTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import Authenticate
        self.schema = Authenticate()

    def test_email_field_required(self):
        result = self.schema.load({}).errors.keys()
        self.assertIn('email', result)

    def test_password_field_required(self):
        result = self.schema.load({}).errors.keys()
        self.assertIn('password', result)


class TokenTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import Token
        self.schema = Token()

    def test_token_field_required(self):
        result = self.schema.load({}).errors.keys()
        self.assertIn('token', result)
