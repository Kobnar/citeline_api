import unittest

from stackcite.api import testing


class SourceCollectionIntegrationTestCase(unittest.TestCase):

    layer = testing.layers.MongoTestLayer

    def setUp(self):
        from stackcite.data import Source
        Source.drop_collection()
        from ..resources import SourceCollection
        self.collection = SourceCollection(None, 'sources')

    def test_create_book_type_creates_book_document(self):
        """SourceColleciton.create() returns a BookSource instance if type is BOOK
        """
        from stackcite.data import Person
        author = Person()
        author.name.title = 'Test Author'
        author.save()
        data = {
            'type': 'BOOK',
            'title': 'Test Book',
            'authors': [str(author.id)],
            'isbn10': '99-9260-854-4'
        }
        result = self.collection.create(data)
        from stackcite.data import BookSource
        self.assertIsInstance(result, BookSource)

    def test_retrieve_returns_results_matching_q_field(self):
        """SourceCollection.retrieve() returns results matching 'q' parameter
        """
        titles = ['Some Source', 'Some Other Source', 'Others: Another Source']
        from stackcite import data as db
        for title in titles:
            source = db.Source()
            source.title = title
            source.save()
        query = {'q': 'other'}
        expected = {'Some Other Source', 'Others: Another Source'}
        items = self.collection.retrieve(query)
        results = {s.title for s in items}
        self.assertEqual(expected, results)
