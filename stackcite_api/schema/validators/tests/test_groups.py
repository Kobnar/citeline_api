import unittest

from stackcite_api import testing


class GroupValidatorTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..groups import GroupValidator
        self.validator = GroupValidator()

    def test_valid_groups_pass_validation(self):
        """GroupValidator accepts all known groups
        """
        from stackcite_api import auth
        from marshmallow import ValidationError
        for group in auth.GROUPS:
            try:
                self.validator(group)
            except ValidationError as err:
                self.fail(err)

    def test_invalid_group_raises_exception(self):
        """GroupValidator raises exception for invalid group
        """
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.validator('invalid')
