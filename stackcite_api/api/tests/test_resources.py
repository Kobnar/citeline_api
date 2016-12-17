import unittest

from stackcite_api import testing


class APIResourceTests(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    # Define "mock" traversal resources and schema:
    from ..resources import APICollection
    class _MockAPICollectionResource(APICollection):
        from ..schema import forms
        class _MockAPIRetrieveCollectionSchema(forms.RetrieveCollection):
            from marshmallow import fields
            name = fields.String()
            number = fields.Integer()
            fact = fields.Bool()
        from ..resources import APIDocument
        class _MockAPIDocumentResource(APIDocument):
            pass
        _collection = testing.mock.MockDocument
        _document_resource = _MockAPIDocumentResource
        _schema = {'GET': _MockAPIRetrieveCollectionSchema}

    def setUp(self):
        # Drops existing.mock.MockDocument data:
        testing.mock.MockDocument.drop_collection()
        # Define testing resource:
        self.col_resource = self._MockAPICollectionResource(
                None, 'mock_collection')

    def make_data(self, data_range=16, save=False):
        docs = []
        for n in range(data_range):
            name = 'document {}'.format(n)
            doc = testing.mock.MockDocument()
            doc.name = name
            doc.number = n
            doc.fact = bool(n % 2)
            if save:
                doc.save()
            docs.append(doc)
        return docs


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
        docs = self.make_data()
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
        """APICollection.retrieve() returns a list if documents exist
        """
        self.make_data(save=True)
        results = self.col_resource.retrieve()
        msg = 'No data was returned'
        self.assertNotEqual(results, [], msg=msg)
        self.assertIsInstance(results, list)

    def test_retrieve_returns_empty_list_if_nothing_exists(self):
        """APICollection.retrieve() returns an empty list if nothing is found
        """
        expected = []
        result = self.col_resource.retrieve()
        self.assertEqual(expected, result)

    def test_retrieve_returns_serialized_data(self):
        """APICollection.retrieve() returns accurately serialized documents
        """
        docs = self.make_data(save=True)
        results = self.col_resource.retrieve()
        for idx, doc in enumerate(docs):
            result = results[idx]
            expected = {
                'id': str(doc.id),
                'name': doc.name,
                'number': doc.number,
                'fact': doc.fact}
            self.assertEqual(expected, result)

    def test_retrieve_with_query_returns_data(self):
        """APICollection.retrieve() returns data with a valid query
        """
        self.make_data(save=True)
        raw_query = {'fact': True}
        results = self.col_resource.retrieve(raw_query)
        self.assertNotEqual([], results)

    def test_retrieve_with_query_returns_correct_results(self):
        """APICollection.retrieve() returns accurate data with a valid query
        """
        self.make_data(save=True)
        raw_query = {'fact': True}
        results = self.col_resource.retrieve(raw_query)
        for doc in results:
            self.assertTrue(doc['fact'])

    def test_retrieve_filters_fields(self):
        """APICollection.retrieve() filters explicitly named fields
        """
        docs = self.make_data(save=True)
        query = {'fields': 'name,fact'}
        results = self.col_resource.retrieve(query)
        for idx, doc in enumerate(docs):
            result = results[idx]
            expected = {
                'name': doc.name,
                'fact': doc.fact}
            self.assertEqual(expected, result)

    def test_retrieve_default_limit(self):
        """APICollection.retrieve() limits results to a default value
        """
        self.make_data(128, save=True)
        results = self.col_resource.retrieve()
        self.assertEqual(100, len(results))

    def test_retrieve_override_limit(self):
        """APICollection.retrieve() limits results to an explicit value
        """
        self.make_data(128, save=True)
        results = self.col_resource.retrieve({'limit': 64})
        self.assertEqual(64, len(results))

    def test_retrieve_default_skip(self):
        """APICollection.retrieve() skips nothing by default
        """
        self.make_data(save=True)
        result = self.col_resource.retrieve()[0]
        self.assertEqual(0, result['number'])

    def test_retrieve_override_skip(self):
        """APICollection.retrieve() skips to an explicit value
        """
        self.make_data(save=True)
        result = self.col_resource.retrieve({'skip': 4})[0]
        self.assertEqual(4, result['number'])

    def test_retrieve_returns_matching_ids(self):
        """APICollection.retrieve() returns documents listed in ids"""
        from random import randint
        docs = self.make_data(data_range=8, save=True)
        expected = [str(d.id) for d in docs]
        for n in range(3):
            r_idx = randint(0, len(expected) - 1)
            expected.pop(r_idx)
        query = {'ids': ','.join(expected)}
        results = [r['id'] for r in self.col_resource.retrieve(query)]
        self.assertEqual(expected, results)

    def test_get_commons_default_values(self):
        """APICollection.get_commons() outputs default values
        """
        expected = ((), 100, 0)
        results = self.col_resource.get_commons({})
        self.assertEqual(expected, results)

    def test_modifies_source_dict(self):
        """APICollection.get_commons() modifies the source dictionary
        """
        source = {
            'name': 'Document 0',
            'number': 12,
            'fact': True,
            'fields': ['id' 'name']}
        self.col_resource.get_commons(source)
        self.assertFalse('fields' in source.keys())

    def test_fields_set(self):
        """APICollection.get_commons() extracts a value for fields
        """
        source = {
            'name': 'Document 0',
            'number': 12,
            'fact': True,
            'fields': 'id,name'}
        result = self.col_resource.get_commons(source)
        self.assertEqual('id,name', result[0])

    def test_limit_set(self):
        """APICollection.get_commons() extracts a value for limit
        """
        source = {
            'name': 'Document 0',
            'number': 12,
            'fact': True,
            'limit': 32}
        result = self.col_resource.get_commons(source)
        self.assertEqual(32, result[1])

    def test_skip_set(self):
        """APICollection.get_commons() extracts a value for set
        """
        source = {
            'name': 'Document 0',
            'number': 12,
            'fact': True,
            'skip': 13}
        result = self.col_resource.get_commons(source)
        self.assertEqual(13, result[2])


class APIDocumentTests(APIResourceTests):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        super(APIDocumentTests, self).setUp()
        docs = self.make_data(save=True)
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
