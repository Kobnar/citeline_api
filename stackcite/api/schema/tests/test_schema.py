import unittest

from stackcite.api import testing


class APISchemaTests(unittest.TestCase):

    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from .. import APISchema
        self.schema = APISchema()
        document_schema = testing.mock.MockDocumentSchema
        self.schema.context['document_schema'] = document_schema

    def test_invalid_method_raises_exception(self):
        """APICollectionSchema.method raises exception for an invalid method
        """
        from .. import schema
        scheme = schema.APICollectionSchema()
        with self.assertRaises(ValueError):
            scheme.method = 'invalid_method'

    def test_valid_methods_do_not_raise_exception(self):
        """APICollectionSchema.method does not raise exceptions for valid schemas
        """
        from .. import schema
        scheme = schema.APICollectionSchema()
        for method in schema.API_METHODS:
            try:
                scheme.method = method
            except ValueError as err:
                msg = 'Unexpected exception raised: {}'.format(err)
                self.fail(msg=msg)

    def test_nested_schema_recieves_method_context(self):
        """APICollectionSchema passes method context to a nested schema
        """
        expected = 'POST'
        from .. import schema
        class ParentSchema(schema.APICollectionSchema):
            from marshmallow import fields, validates_schema
            child = fields.Nested(schema.APICollectionSchema)
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

    layer = testing.layers.BaseTestLayer

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

    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from .. import APICollectionSchema
        self.schema = APICollectionSchema()
        document_schema = testing.mock.MockDocumentSchema()
        self.schema.context['document_schema'] = document_schema


class APICollectionSchemaLoadTests(APICollectionSchemaTests):

    def test_returns_q(self):
        """APICollectionSchema.q loads a query string
        """
        query = {'q': 'some query'}
        data, errors = self.schema.load(query)
        expected = 'some query'
        result = data['q']
        self.assertEqual(expected, result)

    def test_returns_tokenized_ids(self):
        """APICollectionSchema.ids loads a tokenized list of ObjectId strings
        """
        query = {'ids': '594e050330f19315e6ceff4a,594e050330f19315e6ceff4b'}
        data, errors = self.schema.load(query)
        expected = ['594e050330f19315e6ceff4a', '594e050330f19315e6ceff4b']
        result = data['ids']
        self.assertListEqual(expected, result)

    def test_ids_must_be_valid_ids(self):
        """APICollectionSchema.ids logs error loading invalid ObjectId strings
        """
        query = {'ids': 'badid,AnotherBadId,576a6d7530f1936f09e5'}
        data, errors = self.schema.load(query)
        self.assertIn('ids', errors)

    def test_returns_tokenized_fields(self):
        """APICollectionSchema.fields loads a tokenized list of field names
        """
        query = {'fields': 'id,name,number'}
        data, errors = self.schema.load(query)
        expected = ['id', 'name', 'number']
        result = data['fields']
        self.assertListEqual(expected, result)

    def test_default_limit(self):
        """APICollectionSchema.limit defaults to loading 100 without being set
        """
        result = self.schema.load({})
        self.assertEqual(result.data['limit'], 100)

    def test_limit_must_be_gte_1(self):
        """APICollectionSchema.limit must be greater than or equal to 1
        """
        query = {'limit': 0}
        data, errors = self.schema.load(query)
        self.assertIn('limit', errors)

    def test_default_skip(self):
        """APICollectionSchema.skip defaults to loading 0 without being set
        """
        result = self.schema.load({})
        self.assertEqual(result.data['skip'], 0)

    def test_skip_must_be_gte_0(self):
        """APICollectionSchema.skip must be greater than or equal to 0
        """
        query = {'skip': -1}
        data, errors = self.schema.load(query)
        self.assertIn('skip', errors)

    def test_single_returns_tokenized_fields(self):
        """APICollectionSchema.load() returns fields from component schema
        """
        query = {'fields': 'id,name,number'}
        data, errors = self.schema.load(query)
        expected = ['id', 'name', 'number']
        result = data['fields']
        self.assertListEqual(expected, result)
