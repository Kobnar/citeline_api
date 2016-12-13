import unittest

from stackcite_api import testing


class AuthUtilsBaseIntegrationTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from stackcite import data as db
        db.User.drop_collection()
        db.Token.drop_collection()
        self.user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        self.token = db.Token.new(self.user, save=True)


class GetTokenIntegrationTestCase(AuthUtilsBaseIntegrationTestCase):

    def test_get_token_returns_correct_token(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_token
        key = self.token.key
        request = DummyRequest()
        request.authorization = 'Key', key
        result = get_token(request)
        self.assertEqual(self.token, result)

    def test_invalid_key_returns_none(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_token
        request = DummyRequest()
        request.authorization = 'Key', 'invalid_key'
        result = get_token(request)
        self.assertIsNone(result)

    def test_invalid_auth_type_returns_none(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_token
        key = self.token.key
        request = DummyRequest()
        request.authorization = 'Invalid', key
        request.token = get_token(request)
        result = get_token(request)
        self.assertIsNone(result)

    def test_basic_auth_type_returns_none(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_token
        key = self.token.key
        request = DummyRequest()
        request.authorization = 'Basic', key
        result = get_token(request)
        self.assertIsNone(result)


class GetUserIntegrationTestCase(AuthUtilsBaseIntegrationTestCase):

    def test_get_user_returns_correct_user(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_user
        key = self.token.key
        request = DummyRequest()
        request.authorization = 'Key', key
        request.token = self.token
        result = get_user(request)
        self.assertEqual(self.user, result)


class GetGroupsIntegrationTestCase(AuthUtilsBaseIntegrationTestCase):

    def test_get_groups_returns_groups(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_user, get_groups
        expected = self.user.groups
        user_id = self.user.id
        request = DummyRequest()
        request.user = self.user
        result = get_groups(user_id, request)
        self.assertEqual(expected, result)
