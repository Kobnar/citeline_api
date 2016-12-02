import unittest

from citeline_api import testing


class UsersResourceTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def test_duplicate_user_returns_sanitized_error(self):
        self.fail()

    def test_user_can_only_see_own_content(self):
        self.fail()
