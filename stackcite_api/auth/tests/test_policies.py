import unittest

from stackcite_api import testing


def _make_request(key):
    from pyramid.testing import DummyRequest
    api_header = {'API_KEY': key}
    request = DummyRequest()
    request.headers.update(api_header)
    return request


class AuthPolicyIntegrationTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from stackcite import data as db
        from ..policies import TokenAuthenticationPolicy
        self.auth_pol = TokenAuthenticationPolicy()
        db.User.drop_collection()
        db.Token.drop_collection()
        self.user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        self.token = db.Token.new(self.user, save=True)

    def test_authenticated_userid_works_with_static_callback(self):
        from pyramid.testing import DummyRequest
        request = DummyRequest()
        request.user = self.user
        expected = self.user.id
        result = self.auth_pol.authenticated_userid(request)
        self.assertEqual(expected, result)

    def test_unauthenticated_userid_returns_user_id(self):
        from pyramid.testing import DummyRequest
        expected = self.user.id
        request = DummyRequest()
        request.user = self.user
        result = self.auth_pol.unauthenticated_userid(request)
        self.assertEqual(expected, result)

    def test_authenticated_userid_returns_user_id(self):
        from pyramid.testing import DummyRequest
        expected = self.user.id
        request = DummyRequest()
        request.user = self.user
        result = self.auth_pol.authenticated_userid(request)
        self.assertEqual(expected, result)

    def test_effective_principals_includes_user_id(self):
        from pyramid.testing import DummyRequest
        request = DummyRequest()
        request.user = self.user
        result = self.auth_pol.effective_principals(request)
        self.assertIn(self.user.id, result)
