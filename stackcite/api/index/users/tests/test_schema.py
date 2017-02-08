import unittest

from stackcite.api import testing


class UpdateUserTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import UpdateUser
        self.schema = UpdateUser()

    def test_invalid_group_fails_validation(self):
        """UpdateUser schema returns an error for an invalid group
        """
        from stackcite.api import auth
        data = {'groups': ['invalid', auth.STAFF]}
        result = self.schema.load(data).errors.keys()
        self.assertIn('groups', result)

    def test_missing_users_group_fails_validation(self):
        """UpdateUser schema returns an error if default group is missing
        """
        from stackcite.api import auth
        data = {'groups': [auth.STAFF, auth.ADMIN]}
        result = self.schema.load(data).errors.keys()
        self.assertIn('groups', result)

    def test_valid_groups_pass_validation(self):
        """UpdateUser schema does not return an error if all groups are valid
        """
        from stackcite.api import auth
        data = {'groups': [auth.USERS, auth.STAFF, auth.ADMIN]}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('groups', result)

    def test_groups_optional(self):
        """UpdateUser schema does not return an error if no groups are defined
        """
        result = self.schema.load({}).errors.keys()
        self.assertNotIn('groups', result)

    def test_new_password_requires_password(self):
        """UpdateUser.new_password requires password
        """
        data = {'new_password': 'N3wPa$$word'}
        result = self.schema.load(data).errors.keys()
        self.assertIn('new_password', result)


class CreateUserTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import CreateUser
        self.schema = CreateUser()

    def test_email_required(self):
        """CreateUser schema returns an error if no email is provided
        """
        result = self.schema.load({}).errors.keys()
        self.assertIn('email', result)

    def test_password_required(self):
        """CreateUser schema returns an error if no email is provided
        """
        result = self.schema.load({}).errors.keys()
        self.assertIn('password', result)

    def test_invalid_group_fails_validation(self):
        """CreateUser schema returns an error for an invalid group
        """
        from stackcite.api import auth
        data = {'groups': ['invalid', auth.STAFF]}
        result = self.schema.load(data).errors.keys()
        self.assertIn('groups', result)

    def test_missing_users_group_fails_validation(self):
        """CreateUser schema returns an error if default group is missing
        """
        from stackcite.api import auth
        data = {'groups': [auth.STAFF, auth.ADMIN]}
        result = self.schema.load(data).errors.keys()
        self.assertIn('groups', result)

    def test_valid_groups_pass_validation(self):
        """CreateUser schema does not return an error if all groups are valid
        """
        from stackcite.api import auth
        data = {'groups': [auth.USERS, auth.STAFF, auth.ADMIN]}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('groups', result)

    def test_groups_optional(self):
        """CreateUser schema does not return an error if no groups are defined
        """
        result = self.schema.load({}).errors.keys()
        self.assertNotIn('groups', result)

