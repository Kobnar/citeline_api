import unittest

from citeline_api import testing


def _make_request(key):
    from pyramid.testing import DummyRequest
    api_header = {'API_KEY': key}
    request = DummyRequest()
    request.headers.update(api_header)
    return request


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
        from ..utils import get_user
        key = self.token.key
        request = _make_request(key)
        user = get_user(request)
        self.assertEqual(self.user, user)


class GetGroupsIntegrationTestCase(AuthUtilsBaseIntegrationTestCase):

    def test_get_groups_returns_groups(self):
        from ..utils import get_user, get_groups
        expected = self.user.groups
        user_id = self.user.id
        key = self.token.key
        request = _make_request(key)
        request.user = get_user(request) # HACK!
        result = get_groups(user_id, request)
        self.assertEqual(expected, result)
