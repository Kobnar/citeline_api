import unittest

from stackcite_api import testing


class PersonCollectionIntegrationTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from stackcite.data import Organization
        Organization.drop_collection()
        from ..resources import OrganizationCollection
        self.collection = OrganizationCollection(None, 'organizations')


class PersonCollectionRetrieveTestCase(PersonCollectionIntegrationTestCase):

    def test_retrieve_q_returns_matching_people(self):
        """PersonCollection.retrieve() returns Person documents matching query string
        """
        names = ['Reuters', 'Penguin Books', 'Maxwell Books', 'Time']
        from stackcite import data as db
        for name in names:
            db.Organization(name=name).save()
        query = {'q': 'ook'}
        items, params = self.collection.retrieve(query)
        expected = {'Penguin Books', 'Maxwell Books'}
        results = {o.name for o in items}
        self.assertEqual(expected, results)
