import unittest

from stackcite.api import testing


class APISchemaTests(unittest.TestCase):

    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from .. import APISchema
        self.schema = APISchema()

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
        self.schema = testing.mock.MockDocumentSchema()
        from .. import schema
        assert isinstance(self.schema, schema.APICollectionSchema)


class APICollectionSchemaLoadTests(APICollectionSchemaTests):

    def test_collection_load_q(self):
        """APICollectionSchema.load() deserializes a query string (collection-level)
        """
        expected = 'some query'
        query = {'q': expected}
        data, errors = self.schema.load(query)
        result = data['q']
        self.assertEqual(result, expected)

    def test_collection_load_ids(self):
        """APICollectionSchema.load() deserializes a list of ids (collection-level)
        """
        from bson import ObjectId
        expected = object_ids = [str(ObjectId()) for _ in range(3)]
        query = {'ids': ','.join(object_ids)}
        data, errors = self.schema.load(query)
        result = data['ids']
        self.assertEqual(result, expected)

    def test_collection_load_limit(self):
        """APICollectionSchema.load() deserializes a limit integer (collection-level)
        """
        expected = 52
        query = {'limit': str(expected)}
        data, errors = self.schema.load(query)
        result = data['limit']
        self.assertEqual(result, expected)

    def test_collection_load_skip(self):
        """APICollectionSchema.load() deserializes a skip integer (collection-level)
        """
        expected = 33
        query = {'skip': str(expected)}
        data, errors = self.schema.load(query)
        result = data['skip']
        self.assertEqual(result, expected)

    def test_collection_load_fields(self):
        """APICollectionSchema.load() deserializes a list of field names (collection-level)
        """
        expected = ['name.full', 'birth']
        query = {'fields': ','.join([f.replace('.', '__') for f in expected])}
        data, errors = self.schema.load(query)
        result = data['fields']
        self.assertEqual(result, expected)

    def test_document_load_fields(self):
        """APICollectionSchema.load() deserializes a list of field names (document-level)
        """
        expected = ['name.full', 'birth']
        query = {'fields': ','.join([f.replace('.', '__') for f in expected])}
        data, errors = self.schema.load(query)
        result = data['fields']
        self.assertEqual(result, expected)


class APICollectionSchemaDumpTests(APICollectionSchemaTests):

    def test_list_dumps_into_list(self):
        """APICollectionSchema.dump() serializes a list of documents if many=True
        """
        expected = [
            {
                'id': None,
                'name': 'Document 0',
                'number': 0,
                'fact': False
            },
            {
                'id': None,
                'name': 'Document 1',
                'number': 1,
                'fact': True
            },
            {
                'id': None,
                'name': 'Document 2',
                'number': 2,
                'fact': False
            }
        ]
        docs = [testing.mock.MockDocument(
                    name='Document {}'.format(n),
                    number=n,
                    fact=bool(n % 2))
                for n in range(3)]
        result, errors = self.schema.dump(docs, many=True)
        self.assertEqual(result, expected)

    def test_document_dumps_into_document(self):
        """APICollectionSchema.dump() serializes a single document if many=False
        """
        expected = {
            'id': None,
            'name': 'Document',
            'number': 42,
            'fact': False}
        doc = testing.mock.MockDocument(**expected)
        result, errors = self.schema.dump(doc, many=False)
        self.assertEqual(result, expected)


class APICollectionSchemaLoadTestsLegacy(APICollectionSchemaTests):

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
