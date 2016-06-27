import unittest

from citeline_api import testing


class AuthUtilsBaseIntegrationTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from citeline import data as db
        db.User.drop_collection()
        db.Token.drop_collection()
        self.user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        self.token = db.Token.new(self.user, save=True)


class GetUserIntegrationTestCase(AuthUtilsBaseIntegrationTestCase):

    def test_get_user_returns_correct_user(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_user
        key = self.token.key
        request = DummyRequest()
        request.authorization = 'Key', key
        user = get_user(request)
        self.assertEqual(self.user, user)

    def test_invalid_key_returns_none(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_user
        request = DummyRequest()
        request.authorization = 'Key', 'invalid_key'
        user = get_user(request)
        self.assertIsNone(user)

    def test_invalid_auth_type_returns_none(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_user
        key = self.token.key
        request = DummyRequest()
        request.authorization = 'Invalid', key
        user = get_user(request)
        self.assertIsNone(user)

    def test_basic_auth_type_returns_none(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_user
        key = self.token.key
        request = DummyRequest()
        request.authorization = 'Basic', key
        user = get_user(request)
        self.assertIsNone(user)


class GetGroupsIntegrationTestCase(AuthUtilsBaseIntegrationTestCase):

    def test_get_groups_returns_groups(self):
        from pyramid.testing import DummyRequest
        from ..utils import get_user, get_groups
        expected = self.user.groups
        user_id = self.user.id
        key = self.token.key
        request = DummyRequest()
        request.authorization = 'Key', key
        request.user = get_user(request) # HACK!
        result = get_groups(user_id, request)
        self.assertEqual(expected, result)
