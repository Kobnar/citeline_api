import unittest

from stackcite.api import testing


class APISchemaStrictTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def test_method_parameter_sets_method_property(self):
        """APISchema.__init__() method parameter sets APISchema.method property
        """
        from .. import forms
        expected = 'POST'
        schema = forms.APISchema(method=expected)
        result = schema.method
        self.assertEqual(expected, result)

    def test_invalid_method_raises_exception(self):
        """APISchema.__init__() raises exception for an invalid method
        """
        from .. import forms
        with self.assertRaises(AssertionError):
            forms.APISchema(method='invalid_method')


class CollectionStrictTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..forms import RetrieveCollection
        self.schema = RetrieveCollection(strict=True)

    def tearDown(self):
        pass

    def test_ids_deserializes_list_of_objectids(self):
        """APICollection.ids deserializes a list of valid ObjectId strings
        """
        import bson
        expected = [str(bson.ObjectId()) for n in range(3)]
        query = {'ids': ','.join(expected)}
        result = self.schema.load(query).data['ids']
        self.assertEqual(expected, result)

    def test_ids_must_be_valid_ids(self):
        """APICollection.ids must be a list of valid ObjectId strings
        """
        query = {'ids': 'badid,AnotherBadId,576a6d7530f1936f09e5'}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.schema.load(query)

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

    def test_skip_must_be_greater_than_negative_one(self):
        """APICollection.skip must be greater than -1
        """
        query = {'skip': -1}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.schema.load(query)
