import unittest

from stackcite.api import testing


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


class SerializableResourceTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def test_missing_schema_does_not_load(self):
        """ValidatedResource.load() does nothing if no schema is set
        """
        from ..api import SerializableResource
        class MockValidatedResource(SerializableResource):
            _DEFAULT_SCHEMA = {}
        resource = MockValidatedResource()
        from marshmallow import ValidationError
        try:
            resource.load({}, 'GET')
        except ValidationError as err:
            msg = 'Validation failed somehow: {}'.format(err)
            self.fail(msg=msg)

    def test_validation_default_is_strict(self):
        """SerializableResource.load() default is set to 'strict=True'
        """
        from . import MockValidatedResource
        resource = MockValidatedResource()
        data = {'fact': 'dogs'}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            resource.load(data, 'GET')

    def test_load_uses_default_schema_if_method_not_set(self):
        """SerializableResource.load() uses a default schema if no method is set
        """
        from . import MockValidatedResource
        resource = MockValidatedResource()
        data = {'fact': 'dogs'}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            resource.load(data)

    def test_load_uses_overidden_schema(self):
        """SerializableResource.load() uses an overridden resource if one is defined
        """
        from . import MockValidatedChildResource
        resource = MockValidatedChildResource()
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            resource.load({}, 'GET')

    def test_load_accepts_list_with_many_set(self):
        """SerializableResource.load() validates a list of objects if many=True
        """
        from . import MockValidatedResource
        resource = MockValidatedResource()
        data = [{'fact': True}, {'fact': False}]
        from marshmallow import ValidationError
        try:
            resource.load(data, 'GET', many=True)
        except ValidationError as err:
            msg = 'List failed to load: {}'.format(err)
            self.fail(msg=msg)

    def test_loads_raises_exception_for_invalid_json(self):
        """SerializableResource.loads() raises an exception for invalid JSON data
        """
        from . import MockValidatedResource
        resource = MockValidatedResource()
        from json import JSONDecodeError
        with self.assertRaises(JSONDecodeError):
            resource.loads('{invalid:"JSON!', 'GET')

    def test_dump_serializes_object_correctly(self):
        """SerializableResource.dump() returns a dictionary with correct values
        """
        from . import MockValidatedResource
        resource = MockValidatedResource()
        from stackcite.api import testing
        doc = testing.mock.MockDocument(fact=True)
        data, errors = resource.dump(doc, 'GET')
        result = data['fact']
        self.assertTrue(result)

    def test_dump_serializes_list_with_many_set(self):
        """SerializableResource.dump() returns a list with correct values
        """
        from . import MockValidatedResource
        resource = MockValidatedResource()
        facts = (True, False, False, True)
        from stackcite.api import testing
        docs = [testing.mock.MockDocument(fact=f) for f in facts]
        data, errors = resource.dump(docs, 'GET', many=True)
        for idx, doc in enumerate(data):
            expected = facts[idx]
            result = data[idx]['fact']
            self.assertEqual(expected, result)

    def test_dumps_returns_str(self):
        """SerializableResource.dumps() returns a string
        """
        from . import MockValidatedResource
        resource = MockValidatedResource()
        from stackcite.api import testing
        doc = testing.mock.MockDocument(fact=True)
        result, errors = resource.dumps(doc, 'GET')
        self.assertTrue(isinstance(result, str))


class APIResourceTests(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        testing.mock.MockDocument.drop_collection()
        self.col_resource = testing.mock.MockAPICollectionResource(
                None, 'mock_collection')


class APICollectionTests(APIResourceTests):

    layer = testing.layers.MongoIntegrationTestLayer

    def test_create_returns_doc(self):
        """APICollection.create() returns document object
        """
        data = {'name': 'Mock Document'}
        result = self.col_resource.create(data)
        self.assertIsInstance(result, testing.mock.MockDocument)

    def test_create_returns_accurate_doc(self):
        """APICollection.create() returns accurately created document
        """
        data = {
            'name': 'Test Document',
            'number': 42,
            'fact': False}
        doc = self.col_resource.create(data)
        for key, expected in data.items():
            result = getattr(doc, key)
            self.assertEqual(expected, result)

    def test_create_creates_document_in_mongodb(self):
        """APICollection.create() saves a document to MongoDB
        """
        data = {'name': 'Mock Document'}
        doc = self.col_resource.create(data)
        from mongoengine import DoesNotExist
        try:
            testing.mock.MockDocument.objects(id=doc.id)
        except DoesNotExist as err:
            self.fail(err)

    def test_retrieve_returns_queryset(self):
        """APICollection.retrieve() returns a queryset of items
        """
        testing.mock.utils.create_mock_data(save=True)
        results = self.col_resource.retrieve()
        from mongoengine import QuerySet
        self.assertIsInstance(results, QuerySet)

    def test_retrieve_returns_zero_count_if_no_documents_exist(self):
        """APICollection.retrieve() returns zero items if no documents exist
        """
        results = self.col_resource.retrieve()
        self.assertEqual(0, results.count())

    def test_retrieve_returns_accurate_count_if_documents_exist(self):
        """APICollection.retrieve() returns an accurate count of items if documents exist
        """
        count = 16
        testing.mock.utils.create_mock_data(count, save=True)
        results = self.col_resource.retrieve()
        self.assertEqual(count, results.count())

    def test_retrieve_with_query_returns_data(self):
        """APICollection.retrieve() returns queryset of items with a valid query
        """
        testing.mock.utils.create_mock_data(save=True)
        query = {'fact': True}
        results = self.col_resource.retrieve(query)
        self.assertGreater(results.count(), 0)

    def test_retrieve_with_query_returns_correct_results(self):
        """APICollection.retrieve() returns a queryset of accurate data with a valid query
        """
        testing.mock.utils.create_mock_data(save=True)
        query = {'fact': True}
        results = self.col_resource.retrieve(query)
        for doc in results:
            self.assertTrue(doc.fact)

    def test_retrieve_filters_fields(self):
        """APICollection.retrieve() filters explicitly named fields
        """
        testing.mock.utils.create_mock_data(save=True)
        results = self.col_resource.retrieve({}, fields=['name', 'fact'])
        for doc in results:
            self.assertIsNone(doc.number)

    def test_retrieve_default_limit(self):
        """APICollection.retrieve() limits results to a default number of items
        """
        testing.mock.utils.create_mock_data(128, save=True)
        results = self.col_resource.retrieve()
        self.assertEqual(100, results.count(True))

    def test_retrieve_override_limit(self):
        """APICollection.retrieve() limits results to an explicit number of items
        """
        testing.mock.utils.create_mock_data(128, save=True)
        results = self.col_resource.retrieve({}, limit=64)
        self.assertEqual(64, results.count(True))

    def test_retrieve_default_skip(self):
        """APICollection.retrieve() skips nothing by default
        """
        testing.mock.utils.create_mock_data(save=True)
        results = self.col_resource.retrieve()
        self.assertEqual(0, results[0].number)

    def test_retrieve_override_skip(self):
        """APICollection.retrieve() skips to defined value
        """
        testing.mock.utils.create_mock_data(save=True)
        results = self.col_resource.retrieve({}, skip=4)
        self.assertEqual(4, results[0].number)

    def test_retrieve_returns_matching_ids(self):
        """APICollection.retrieve() returns documents listed in ids
        """
        from random import randint
        docs = testing.mock.utils.create_mock_data(count=8, save=True)
        # Create a list of all IDs and pop random ones
        expected = [str(d.id) for d in docs]
        for n in range(3):
            r_idx = randint(0, len(expected) - 1)
            expected.pop(r_idx)
        raw_query = {'ids': expected}
        results = self.col_resource.retrieve(raw_query)
        results = [str(r.id) for r in results]
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

    def test_retrieve_returns_obj(self):
        """APIDocument.retrieve() returns a document object
        """
        result = self.doc_resource.retrieve()
        self.assertIsInstance(result, testing.mock.MockDocument)

    def test_retrieve_returns_serialized_data(self):
        """APIDocument.retrieve() returns correct document
        """
        expected = self.doc.id
        result = self.doc_resource.retrieve()
        result = result.id
        self.assertEqual(expected, result)

    def test_retrieve_filters_fields(self):
        """APIDocument.retrieve() filters explicitly named fields on document
        """
        fields = ['name', 'fact']
        result = self.doc_resource.retrieve(fields)
        self.assertIsNone(result.number)

    def test_update_returns_updated_data(self):
        """APIDocument.update() returns document with updated data
        """
        data = {'name': 'Updated Document'}
        result = self.doc_resource.update(data)
        self.assertEqual(result.name, data['name'])

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
        """APIDocument.delete() raises exception if document does not exist
        """
        from bson import ObjectId
        doc_resource = self.col_resource[ObjectId()]
        from mongoengine import DoesNotExist
        with self.assertRaises(DoesNotExist):
            doc_resource.delete()

    def test_delete_deletes_document_in_mongodb(self):
        """APIDocument.delete() deletes document in MongoDB
        """
        self.doc_resource.delete()
        from mongoengine import DoesNotExist
        with self.assertRaises(DoesNotExist):
            testing.mock.MockDocument.objects.get(id=self.doc.id)
