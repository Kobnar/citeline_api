import unittest

from stackcite.api import testing


class APISchemaTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

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
        scheme = ParentSchema(strict=True)
        scheme.method = 'POST'
        try:
            scheme.load({'child': {}})
        except ValueError as err:
            self.fail(err)


class APIDocumentSchemaTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from .. import schema
        self.schema = schema.APIDocumentSchema(strict=True)

    def test_fields_loads(self):
        """APIDocumentSchema.fields loads data
        """
        payload = {'fields': 'name,number'}
        data, errors = self.schema.load(payload)
        self.assertIn('fields', data)

    def test_fields_does_not_dump(self):
        """APIDocumentSchema.fields does not dump data
        """
        payload = {'fields': ['name', 'number']}
        data, errors = self.schema.dump(payload)
        self.assertNotIn('fields', data)

    def test_fields_loads_list_of_strings(self):
        """APIDocumentSchema.fields parses a string of field names into a list
        """
        payload = {'fields': 'name,number'}
        data, errors = self.schema.load(payload)
        expected = ['name', 'number']
        result = data['fields']
        self.assertListEqual(expected, result)


class APICollectionSchemaTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from .. import schema
        self.schema = schema.APICollectionSchema(strict=True)

    def test_q_loads(self):
        """APICollectionSchema.q loads data
        """
        payload = {'q': 'some query'}
        data, errors = self.schema.load(payload)
        self.assertIn('q', data)

    def test_q_does_not_dump(self):
        """APICollectionSchema.q does not dump data
        """
        payload = {'q': 'some query'}
        data, errors = self.schema.dump(payload)
        self.assertNotIn('q', data)

    def test_ids_loads(self):
        """APICollectionSchema.ids loads data
        """
        from bson import ObjectId
        payload = {'ids': str(ObjectId())}
        data, errors = self.schema.load(payload)
        self.assertIn('ids', data)

    def test_ids_does_not_dump(self):
        """APICollectionSchema.ids does not dump data
        """
        from bson import ObjectId
        payload = {'ids': [str(ObjectId())]}
        data, errors = self.schema.dump(payload)
        self.assertNotIn('ids', data)

    def test_limit_loads(self):
        """APICollectionSchema.limit loads data
        """
        payload = {'limit': 120}
        data, errors = self.schema.load(payload)
        self.assertIn('limit', data)

    def test_limit_does_not_dump(self):
        """APICollectionSchema.limit does not dump data
        """
        payload = {'limit': 120}
        data, errors = self.schema.dump(payload)
        self.assertNotIn('limit', data)

    def test_skip_loads(self):
        """APICollectionSchema.skip loads data
        """
        payload = {'skip': 120}
        data, errors = self.schema.load(payload)
        self.assertIn('skip', data)

    def test_skip_does_not_dump(self):
        """APICollectionSchema.skip does not dump data
        """
        payload = {'skip': 120}
        data, errors = self.schema.dump(payload)
        self.assertNotIn('skip', data)

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
