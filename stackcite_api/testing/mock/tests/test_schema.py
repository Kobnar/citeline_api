import unittest


class MockUpdateDocumentSchemaTestCase(unittest.TestCase):

    def setUp(self):
        from .. import MockUpdateDocumentSchema
        self.test_schema = MockUpdateDocumentSchema()

    def test_unknown_field_dropped(self):
        """MockUpdateDocumentSchema validation drops an unknown field
        """
        data = {
            'name': 'Document',
            'unknown': 'field'}
        result, errors = self.test_schema.load(data)
        self.assertNotIn('unknown', result.keys())


class MockCreateDocumentSchemaTestCase(unittest.TestCase):

    def setUp(self):
        from .. import MockCreateDocumentSchema
        self.test_schema = MockCreateDocumentSchema()

    def test_fact_accepted(self):
        """MockCreateDocumentSchema inherits 'fact' field from MockUpdateDocumentSchema
        """
        data = {
            'name': 'Document',
            'fact': True}
        result, errors = self.test_schema.load(data)
        self.assertIn('fact', result.keys())

    def test_name_required(self):
        """MockCreateDocumentSchema validation requires 'name' field
        """
        data = {'number': 42}
        result, errors = self.test_schema.load(data)
        self.assertIn('name', errors.keys())
