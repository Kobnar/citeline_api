import unittest

from stackcite.api import testing


class AuthenticateTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import Authenticate
        self.schema = Authenticate()

    def test_email_field_required(self):
        """Authenticate.email is a required field
        """
        result = self.schema.load({}).errors.keys()
        self.assertIn('email', result)

    def test_password_field_required(self):
        """Authenticate.password is a required field
        """
        result = self.schema.load({}).errors.keys()
        self.assertIn('password', result)


class AuthTokenTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import AuthToken
        self.schema = AuthToken()

    def test_token_field_required(self):
        """Authenticate.token is a required field
        """
        result = self.schema.load({}).errors.keys()
        self.assertIn('key', result)
