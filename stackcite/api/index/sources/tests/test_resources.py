import unittest

from stackcite.api import testing


class SourceCollectionIntegrationTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from stackcite.data import Source
        Source.drop_collection()
        from ..resources import SourceCollection
        self.collection = SourceCollection(None, 'sources')

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
        items, params = self.collection.retrieve(query)
        results = {s.title for s in items}
        self.assertEqual(expected, results)
