import unittest

from stackcite.api import testing


class ObjectIdValidatorTests(unittest.TestCase):

    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from ..oids import ObjectIdValidator
        self.validator = ObjectIdValidator()

    def test_invalid_objectids_raise_exception(self):
        """ObjectIdValidator raises exception for invalid ObjectIds
        """
        from marshmallow import ValidationError
        invalid_oids = testing.data.invalid_object_ids()
        for oid in invalid_oids:
            with (self.assertRaises(ValidationError)):
                self.validator(oid)

    def test_valid_objectids_dont_raise_exception(self):
        """ObjectIdValidator does not raise exception for valid ObjectIds
        """
        from marshmallow import ValidationError
        valid_oids = testing.data.valid_object_ids()
        for oid in valid_oids:
            try:
                self.validator(oid)
            except ValidationError:
                msg = 'Valid ObjectId failed validaiton: {}'.format(oid)
                self.fail(msg)
