import unittest


class MockDocumentSchemaTests(unittest.TestCase):

    def make_schema(self, method=None):
        from .. import MockDocumentSchema
        schema = MockDocumentSchema()
        schema.method = method
        return schema


class CreateMockDocumentSchema(MockDocumentSchemaTests):

    def setUp(self):
        self.schema = self.make_schema(method='POST')

    def test_name_required(self):
        """MockDocumentSchema validation requires 'name' field for POST
        """
        data = {'number': 42}
        result, errors = self.schema.load(data)
        self.assertIn('name', errors.keys())


class RetrieveMockDocumentSchema(MockDocumentSchemaTests):

    def setUp(self):
        self.schema = self.make_schema(method='GET')


class UpdateMockDocumentSchema(MockDocumentSchemaTests):

    def setUp(self):
        self.schema = self.make_schema(method='PUT')

    def test_unknown_field_dropped(self):
        """MockDocumentSchema validation drops an unknown field for PUT
        """
        data = {
            'name': 'Document',
            'unknown': 'field'}
        result, errors = self.schema.load(data)
        self.assertNotIn('unknown', result.keys())
