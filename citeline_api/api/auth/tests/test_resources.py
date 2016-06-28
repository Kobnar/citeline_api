import unittest

from citeline_api import testing


def make_user(email, password, save=False):
    from citeline.data import User
    user = User(email)
    user.password = password
    if save:
        user.save()
    return user


class AuthResourceIntegrationTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from citeline.data import Token, User
        User.drop_collection()
        Token.drop_collection()
        from ..resources import AuthResource
        self.collection = AuthResource(None, 'auth')

    def test_login_updates_last_login(self):
        """AuthResource.login() updates User.last_login with a more recent time
        """
        from citeline.data import User
        email = 'test@email.com'
        password = 'T3stPa$$word'
        # Create user and set last_login
        user = make_user(email, password)
        prev_login = user.touch_login()
        user.save()
        # Wait 0.1 seconds
        import time
        time.sleep(0.001)
        # Log in user
        auth_data = {'email': email, 'password': password}
        self.collection.create(auth_data)
        # Query updated user
        user = User.objects.get(email=email)
        last_login = user.last_login
        login_delta = last_login - prev_login
        self.assertGreater(login_delta.microseconds, 1000)

    def test_login_returns_user(self):
        """AuthResource.login() returns a dict containing a user
        """
        email = 'test@email.com'
        password = 'T3stPa$$word'
        # Create user
        user = make_user(email, password)
        user.save()
        # Log in user
        auth_data = {'email': email, 'password': password}
        result = self.collection.create(auth_data)
        self.assertIn('user', result.keys())

    def test_login_returns_token(self):
        """AuthResource.login() returns a dict containing an API token
        """
        email = 'test@email.com'
        password = 'T3stPa$$word'
        # Create user
        user = make_user(email, password)
        user.save()
        # Log in user
        auth_data = {'email': email, 'password': password}
        result = self.collection.create(auth_data)
        self.assertIn('token', result.keys())
