import unittest

from stackcite_api import testing


def make_person(data, save=False):
    from stackcite.data import Person
    person = Person()
    person.deserialize(data)
    if save:
        person.save()
    return person


class PersonCollectionIntegrationTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from stackcite.data import Person
        Person.drop_collection()
        from ..resources import PersonCollection
        self.collection = PersonCollection(None, 'people')


class PersonCollectionCreateTestCase(PersonCollectionIntegrationTestCase):

    def test_create_valid_person_returns_dict_with_id(self):
        """PersonCollection.create() returns a dictionary with an ObjectId
        """
        data = {'name': {'full': 'John Nobody Doe'}}
        result = self.collection.create(data)
        self.assertIsNotNone(result.id)

    def test_create_invalid_person_raises_exception(self):
        """PersonCollection.create() raises exception for invalid data
        """
        from marshmallow import ValidationError
        data = {'name': {'first': 'John', 'full': 'John Nobody Doe'}}
        with self.assertRaises(ValidationError):
            self.collection.create(data)


class PersonCollectionRetrieveTestCase(PersonCollectionIntegrationTestCase):

    def test_get_schema_defined(self):
        """PersonCollection has 'GET' schema defined
        """
        # Without a schema, 'fields' is passed back to mongo.DocumentResource
        # as a string, which raises an AssertionError
        query = {'fields': 'id,name'}
        try:
            self.collection.retrieve(query)
        except AssertionError:
            msg = 'PersonCollection has no GET schema'
            self.fail(msg)

    def test_retrieve_people_returns_all_people(self):
        """PersonCollection.retrieve() returns ObjectIds for everybody in the database
        """
        from stackcite.testing.data import people as ppl
        people = [make_person(p, save=True) for p in ppl()]
        results, params = self.collection.retrieve()
        results = [str(r.id) for r in results]
        for pid in people:
            expected = str(pid.id)
            self.assertIn(expected, results)

    def test_retrieve_q_returns_matching_people(self):
        """PersonCollection.retrieve() returns Person documents matching query string
        """
        names = ['J.N. Doe', 'Arthur Brooks', 'James McArthur']
        from stackcite import data as db
        for name in names:
            person = db.Person()
            person.name.title = name
            person.save()
        query = {'q': 'arthur'}
        items, params = self.collection.retrieve(query)
        expected = {'Arthur Brooks', 'James McArthur'}
        results = {p.name.title for p in items}
        self.assertEqual(expected, results)

    def test_retrieve_q_returns_matching_people_w_multiple_fields(self):
        """PersonCollection.retrieve() returns Person documents w/ matching title or full name
        """
        names = (
            ('J.N. Doe', 'John Doe'),
            ('John Scott', 'Wilbur Darling'),
            ('Maxwell Ohm', 'Maxwell Ohm'))
        from stackcite import data as db
        for title, full_name in names:
            person = db.Person()
            person.name.title = title
            person.name.full = full_name
            person.save()
        query = {'q': 'john'}
        items, params = self.collection.retrieve(query)
        expected = {'J.N. Doe', 'John Scott'}
        results = {p.name.title for p in items}
        self.assertEqual(expected, results)


class PersonDocumentIntegrationTestCase(PersonCollectionIntegrationTestCase):

    def setUp(self):
        super().setUp()
        from random import randint
        from stackcite.testing.data import people as ppl
        people = ppl()
        rand_idx = randint(0, len(people) - 1)
        person = make_person(people[rand_idx], save=True)
        self.document = self.collection[person.id]


class PersonDocumentRetrieveTestCase(PersonDocumentIntegrationTestCase):

    def test_get_schema_defined(self):
        """PersonDocment has 'GET' schema defined
        """
        # Without a schema, 'fields' is passed back to mongo.DocumentResource
        # as a string, which raises an AssertionError
        query = {'fields': 'id,name'}
        try:
            self.collection.retrieve(query)
        except AssertionError:
            msg = 'PersonCollection has no GET schema defined'
            self.fail(msg)

    def test_retrieve_returns_person(self):
        """PersonDocument.retrieve() returns data with the correct ObjectId
        """
        expected = str(self.document.id)
        result, params = self.document.retrieve()
        result = str(result.id)
        self.assertEqual(expected, result)


class PersonDocumentUpdateTestCase(PersonDocumentIntegrationTestCase):

    def test_update_returns_updated_data(self):
        """PersonDocument.update() returns a dict of updated data
        """
        expected = 'Updated Person'
        data = {'name': {'title': expected}}
        result = self.document.update(data)
        result = result.name.title
        self.assertEqual(expected, result)

    def test_update_with_invalid_data_raises_exception(self):
        """PersonDocument.update() raises ValidationError with invalid data
        """
        from marshmallow import ValidationError
        data = {'name': {'first': 'John', 'full': 'John Nobody Doe'}}
        with self.assertRaises(ValidationError):
            self.document.update(data)
