import unittest

from stackcite.api import testing


class APISchemaTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def test_method_parameter_sets_method_property(self):
        """APISchema.__init__() method parameter sets APISchema.method property
        """
        from .. import schema
        expected = 'POST'
        schema = schema.APISchema(method=expected)
        result = schema.method
        self.assertEqual(expected, result)

    def test_invalid_method_parameter_raises_exception(self):
        """APISchema.__init__() raises exception for an invalid method
        """
        from .. import schema
        with self.assertRaises(ValueError):
            schema.APISchema(method='invalid_method')

    def test_invalid_method_raises_exception(self):
        """APISchema.method raises exception for an invalid method
        """
        from .. import schema
        scheme = schema.APISchema()
        with self.assertRaises(ValueError):
            scheme.method = 'invalid_method'

    def test_valid_methods_do_not_raise_exception(self):
        """APISchema.method does not raise exceptions for valid schemas
        """
        from .. import schema
        scheme = schema.APISchema()
        for method in schema.API_METHODS:
            try:
                scheme.method = method
            except ValueError as err:
                msg = 'Unexpected exception raised: {}'.format(err)
                self.fail(msg=msg)

    def test_nexted_schema_recieves_method_context(self):
        """APISchema passes method context to a nested schema
        """
        expected = 'POST'
        from .. import schema
        class ParentSchema(schema.APISchema):
            from marshmallow import fields, validates_schema
            child = fields.Nested(schema.APISchema)
            @validates_schema
            def validate_method(self, data):
                if self.method is not expected:
                    msg = 'Method context not passed to nested schema: {} != {}'
                    raise ValueError(msg.format(expected, self.method))
        scheme = ParentSchema(method='POST', strict=True)
        try:
            scheme.load({'child': {}})
        except ValueError as err:
            self.fail(err)


class APICollectionSchemaTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from .. import schema
        self.schema = schema.APICollectionSchema(strict=True)

    def test_ids_deserializes_list_of_ids(self):
        """APICollectionSchema.ids deserializes a list of valid ObjectId strings
        """
        import bson
        expected = [str(bson.ObjectId()) for n in range(3)]
        query = {'ids': ','.join(expected)}
        result = self.schema.load(query).data['ids']
        self.assertEqual(expected, result)

    def test_ids_must_be_valid_ids(self):
        """APICollectionSchema.ids must be a list of valid ObjectId strings
        """
        query = {'ids': 'badid,AnotherBadId,576a6d7530f1936f09e5'}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.schema.load(query)

    def test_default_limit(self):
        """APICollectionSchema.limit defaults to 100 without being set
        """
        result = self.schema.load({})
        self.assertEqual(result.data['limit'], 100)

    def test_default_skip(self):
        """APICollectionSchema.skip defaults to 0 without being set
        """
        result = self.schema.load({})
        self.assertEqual(result.data['skip'], 0)

    def test_limit_must_be_greater_than_zero(self):
        """APICollectionSchema.limit must be greater than 0
        """
        query = {'limit': 0}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.schema.load(query)

    def test_skip_must_be_greater_than_negative_one(self):
        """APICollectionSchema.skip must be greater than -1
        """
        query = {'skip': -1}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.schema.load(query)
