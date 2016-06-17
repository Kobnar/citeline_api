import unittest

from citeline_api import testing


class CollectionStrictTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..forms import Collection
        self.schema = Collection(strict=True)

    def tearDown(self):
        pass

    def test_default_limit(self):
        """APICollection.limit defaults to 100 without being set
        """
        result = self.schema.load({})
        self.assertEqual(result.data['limit'], 100)

    def test_default_offset(self):
        """APICollection.offset defaults to 0 without being set
        """
        result = self.schema.load({})
        self.assertEqual(result.data['skip'], 0)

    def test_limit_must_be_greater_than_zero(self):
        """APICollection.limit must be greater than 0
        """
        query = {'limit': 0}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.schema.load(query)

    def test_limit_must_be_greater_than_negative_one(self):
        """APICollection.offset must be greater than -1
        """
        query = {'limit': -1}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.schema.load(query)
