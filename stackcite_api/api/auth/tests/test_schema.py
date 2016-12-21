import unittest

from stackcite_api import testing


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

    def test_email_password_optional_if_key_set(self):
        """Authenticate.key makes 'email' and 'password' fields optional
        """
        data = {
            'key': '3ba7b73edb07bbc8f5ee7a642a27bba555b33bbf8fffd7669f3d2af4'}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('email', result)
        self.assertNotIn('password', result)


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
