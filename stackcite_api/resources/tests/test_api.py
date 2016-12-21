import unittest

from stackcite_api import testing


class EndpointResourceTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from . import MockEndpointResource
        self.config = MockEndpointResource.MockConfig()
        self.resource = MockEndpointResource()

    def test_add_views_adds_own_view(self):
        """APIIndexResource.add_views() adds own view class to configuration object
        """
        self.resource.add_views(self.config)
        results = [v['context'] for v in self.config.views]
        from . import MockEndpointResource
        self.assertIn(MockEndpointResource, results)

    def test_add_views_adds_offspring_views(self):
        """APIIndexResource.add_views() adds offspring view classes to configuration object
        """
        self.resource.add_views(self.config)
        results = [v['view_class'] for v in self.config.views
                   if v['view_class'] is 'TEST']
        self.assertEqual(2, len(results))


class ValidatedResourceTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def test_validation_default_is_strict(self):
        """ValidatedResource.validate() default is set to 'strict=True'
        """
        from . import MockValidatedResource
        resource = MockValidatedResource()
        data = {'required': 'dogs'}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            resource.validate('GET', data)

    def test_validate_uses_overidden_schema(self):
        """ValidatedResource.validate() uses an overridden resource if one is defined
        """
        from . import MockValidatedChildResource
        resource = MockValidatedChildResource()
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            resource.validate('GET', {})


class APIResourceTests(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        testing.mock.MockDocument.drop_collection()
        self.col_resource = testing.mock.MockAPICollectionResource(
                None, 'mock_collection')

class APICollectionTests(APIResourceTests):

    layer = testing.layers.MongoIntegrationTestLayer

    def test_create_returns_dict(self):
        """APICollection.create() returns a dictionary
        """
        data = {'name': 'Mock Document'}
        result = self.col_resource.create(data)
        self.assertIsInstance(result, dict)

    def test_create_returns_serialized_data(self):
        """APICollection.create() returns accurately serialized documents
        """
        docs = testing.mock.utils.create_mock_data()
        for doc in docs:
            expected = {
                'name': doc.name,
                'number': doc.number,
                'fact': doc.fact}
            result = self.col_resource.create(expected)
            result.pop('id')
            self.assertEqual(expected, result)

    def test_create_creates_document_in_mongodb(self):
        """APICollection.create() saves a document to MongoDB
        """
        data = {'name': 'Mock Document'}
        doc = self.col_resource.create(data)
        from mongoengine import DoesNotExist
        try:
            testing.mock.MockDocument.objects(id=doc['id'])
        except DoesNotExist as err:
            self.fail(err)

    def test_retrieve_returns_list(self):
        """APICollection.retrieve() returns a list of items if documents exist
        """
        testing.mock.utils.create_mock_data(save=True)
        results = self.col_resource.retrieve()['items']
        msg = 'No data was returned'
        self.assertNotEqual(results, [], msg=msg)
        self.assertIsInstance(results, list)

    def test_retrieve_returns_accurate_count_if_documents_exist(self):
        """APICollection.retrieve() returns an accurate count of items if documents exist
        """
        count = 16
        testing.mock.utils.create_mock_data(count, save=True)
        result = self.col_resource.retrieve()['count']
        self.assertEqual(count, result)

    def test_retrieve_returns_empty_list_if_nothing_exists(self):
        """APICollection.retrieve() returns an empty list of items if nothing is found
        """
        expected = []
        result = self.col_resource.retrieve()['items']
        self.assertEqual(expected, result)

    def test_retrieve_returns_zero_count_if_nothing_exists(self):
        """APICollection.retrieve() returns a count of zero if nothing is found
        """
        expected = 0
        result = self.col_resource.retrieve()['count']
        self.assertEqual(expected, result)

    def test_retrieve_returns_serialized_data(self):
        """APICollection.retrieve() returns a list of accurately serialized documents
        """
        docs = testing.mock.utils.create_mock_data(save=True)
        results = self.col_resource.retrieve()
        for idx, doc in enumerate(docs):
            result = results['items'][idx]
            expected = {
                'id': str(doc.id),
                'name': doc.name,
                'number': doc.number,
                'fact': doc.fact}
            self.assertEqual(expected, result)

    def test_retrieve_with_query_returns_data(self):
        """APICollection.retrieve() returns a list of items data with a valid query
        """
        testing.mock.utils.create_mock_data(save=True)
        raw_query = {'fact': True}
        results = self.col_resource.retrieve(raw_query)
        self.assertGreater(len(results), 0)

    def test_retrieve_with_query_returns_correct_results(self):
        """APICollection.retrieve() returns a list of accurate data with a valid query
        """
        testing.mock.utils.create_mock_data(save=True)
        raw_query = {'fact': True}
        results = self.col_resource.retrieve(raw_query)['items']
        for doc in results:
            self.assertTrue(doc['fact'])

    def test_retrieve_filters_fields(self):
        """APICollection.retrieve() filters explicitly named fields
        """
        docs = testing.mock.utils.create_mock_data(save=True)
        query = {'fields': 'name,fact'}
        results = self.col_resource.retrieve(query)
        for idx, doc in enumerate(docs):
            result = results['items'][idx]
            expected = {
                'name': doc.name,
                'fact': doc.fact}
            self.assertEqual(expected, result)

    def test_retrieve_default_limit(self):
        """APICollection.retrieve() limits results to a default number of items
        """
        testing.mock.utils.create_mock_data(128, save=True)
        results = self.col_resource.retrieve()['items']
        self.assertEqual(100, len(results))

    def test_retrieve_override_limit(self):
        """APICollection.retrieve() limits results to an explicit number of items
        """
        testing.mock.utils.create_mock_data(128, save=True)
        results = self.col_resource.retrieve({'limit': 64})['items']
        self.assertEqual(64, len(results))

    def test_retrieve_default_skip(self):
        """APICollection.retrieve() skips nothing by default
        """
        testing.mock.utils.create_mock_data(save=True)
        result = self.col_resource.retrieve()['items'][0]
        self.assertEqual(0, result['number'])

    def test_retrieve_override_skip(self):
        """APICollection.retrieve() skips to an explicit value
        """
        testing.mock.utils.create_mock_data(save=True)
        result = self.col_resource.retrieve({'skip': 4})['items'][0]
        self.assertEqual(4, result['number'])

    def test_retrieve_returns_matching_ids(self):
        """APICollection.retrieve() returns documents listed in ids"""
        from random import randint
        docs = testing.mock.utils.create_mock_data(count=8, save=True)
        expected = [str(d.id) for d in docs]
        for n in range(3):
            r_idx = randint(0, len(expected) - 1)
            expected.pop(r_idx)
        query = {'ids': ','.join(expected)}
        results = [r['id'] for r in self.col_resource.retrieve(query)['items']]
        self.assertEqual(expected, results)

    def test_get_params_default_values(self):
        """APICollection.get_params() outputs default values
        """
        expected = {
            'fields': (),
            'limit': 100,
            'skip': 0}
        query, results = self.col_resource.get_params({})
        self.assertEqual(expected, results)

    def test_modifies_source_dict(self):
        """APICollection.get_params() does not modify the source dictionary
        """
        source = {
            'name': 'Document 0',
            'number': 12,
            'fact': True,
            'fields': ['id', 'name']}
        self.col_resource.get_params(source)
        self.assertTrue('fields' in source.keys())

    def test_fields_set(self):
        """APICollection.get_params() extracts a value for fields
        """
        source = {
            'name': 'Document 0',
            'number': 12,
            'fact': True,
            'fields': 'id,name'}
        query, result = self.col_resource.get_params(source)
        self.assertEqual('id,name', result['fields'])

    def test_limit_set(self):
        """APICollection.get_params() extracts a value for limit
        """
        source = {
            'name': 'Document 0',
            'number': 12,
            'fact': True,
            'limit': 32}
        query, result = self.col_resource.get_params(source)
        self.assertEqual(32, result['limit'])

    def test_skip_set(self):
        """APICollection.get_params() extracts a value for skip
        """
        source = {
            'name': 'Document 0',
            'number': 12,
            'fact': True,
            'skip': 13}
        query, result = self.col_resource.get_params(source)
        self.assertEqual(13, result['skip'])


class APIDocumentTests(APIResourceTests):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        super(APIDocumentTests, self).setUp()
        docs = testing.mock.utils.create_mock_data(save=True)
        self.doc = docs[8]
        self.doc_resource = self.col_resource[self.doc.id]

    def test_retrieve_raises_exeption_if_does_not_exist(self):
        """APIDocument.retrieve() raises exception if document does not exist
        """
        from bson import ObjectId
        doc_resource = self.col_resource[ObjectId()]
        from mongoengine import DoesNotExist
        with self.assertRaises(DoesNotExist):
            doc_resource.retrieve()

    def test_retrieve_returns_dict(self):
        """APIDocument.retrieve() returns a dictionary
        """
        result = self.doc_resource.retrieve()
        self.assertIsInstance(result, dict)

    def test_retrieve_returns_serialized_data(self):
        """APIDocument.retrieve() returns accurately serialized document
        """
        expected = {
            'id': str(self.doc.id),
            'name': self.doc.name,
            'number': self.doc.number,
            'fact': self.doc.fact}
        result = self.doc_resource.retrieve()
        self.assertEqual(expected, result)

    def test_retrieve_filters_fields(self):
        """APIDocument.retrieve() filters explicitly named fields
        """
        query = {'fields': 'name,fact'}
        expected = {
            'name': self.doc.name,
            'fact': self.doc.fact}
        result = self.doc_resource.retrieve(query)
        self.assertEqual(expected, result)

    def test_update_returns_updated_data(self):
        """APIDocument.update() returns updated data
        """
        data = {'name': 'Updated Document'}
        result = self.doc_resource.update(data)
        self.assertEqual(result['name'], data['name'])

    def test_update_updates_document_in_mongodb(self):
        """APIDocument.update() updates document in MongoDB
        """
        data = {'name': 'Updated Document'}
        self.doc_resource.update(data)
        result = testing.mock.MockDocument.objects.get(id=self.doc.id)
        self.assertEqual(result.name, data['name'])

    def test_delete_returns_true_if_successful(self):
        """APIDocument.delete() returns True if successful
        """
        result = self.doc_resource.delete()
        self.assertTrue(result)

    def test_delete_returns_false_if_document_does_not_exist(self):
        """APIDocument.delete() returns False if document does not exist
        """
        from bson import ObjectId
        doc_resource = self.col_resource[ObjectId()]
        result = doc_resource.delete()
        self.assertFalse(result)

    def test_delete_deletes_document_in_mongodb(self):
        """APIDocument.delete() deletes document in MongoDB
        """
        self.doc_resource.delete()
        from mongoengine import DoesNotExist
        with self.assertRaises(DoesNotExist):
            testing.mock.MockDocument.objects.get(id=self.doc.id)
