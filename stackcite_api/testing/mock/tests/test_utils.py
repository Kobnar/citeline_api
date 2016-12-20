import unittest

from stackcite_api import testing


class CreateMockDataTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from ..models import MockDocument
        MockDocument.drop_collection()

    def test_create_mock_data_creates_default_count(self):
        """create_mock_data() creates a default number of documents
        """
        expected = 16
        from ..utils import create_mock_data
        docs = create_mock_data()
        result = len(docs)
        self.assertEqual(expected, result)

    def test_create_mock_data_creates_specific_count(self):
        """create_mock_data() creates a specific number of documents
        """
        expected = 7
        from ..utils import create_mock_data
        docs = create_mock_data(count=expected)
        result = len(docs)
        self.assertEqual(expected, result)

    def test_create_mock_data_saves_nothing_if_not_specified(self):
        """create_mock_data() saves nothing to the database by default
        """
        expected = 0
        from ..utils import create_mock_data
        create_mock_data(count=3)
        from ..models import MockDocument
        docs = MockDocument.objects()
        result = docs.count()
        self.assertEqual(expected, result)

    def test_create_mock_data_saves_data_to_database_if_specified(self):
        """create_mock_data() saves data to the database if 'save=True'
        """
        expected = 3
        from ..utils import create_mock_data
        create_mock_data(count=expected, save=True)
        from ..models import MockDocument
        docs = MockDocument.objects()
        result = docs.count()
        self.assertEqual(expected, result)
