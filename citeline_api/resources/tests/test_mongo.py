import unittest

from citeline_api import testing


class MockResourceTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    # Define "mock" traversal resources:
    from ..mongo import CollectionResource
    class _MockCollectionResource(CollectionResource):
        from ..mongo import DocumentResource
        class _MockDocumentResource(DocumentResource):
            pass
        _collection = testing.mock.MockDocument
        _document_resource = _MockDocumentResource

    def setUp(self):
        testing.mock.MockDocument.drop_collection()
        self.col_rec = self._MockCollectionResource(None, 'mock_collection')

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


class CollectionResourceTestCase(MockResourceTestCase):

    def test_getitem_accepts_objectid(self):
        """CollectionResource.__getitem__() accepts a BSON ObjectId object
        """
        from bson import ObjectId
        id = ObjectId()
        try:
            self.col_rec[id]
        except KeyError as err:
            self.fail(err)

    def test_getitem_accepts_objectid_string(self):
        """CollectionResource.__getitem__() accepts a properly formatted ID string
        """
        from bson.objectid import ObjectId
        id = str(ObjectId())
        try:
            self.col_rec[id]
        except KeyError as err:
            self.fail(err)

    def test_getitem_returns_child_index(self):
        """CollectionResource.__getitem__() returns a child IndexResource if it is not an ObjectId
        """
        from .. import IndexResource
        self.col_rec['ux'] = IndexResource
        result = self.col_rec['ux']
        self.assertIsInstance(result, IndexResource)
        self.assertEqual(result.__name__, 'ux')

    def test_getitem_raises_key_error_for_invalid_objectid_string_if_not_child(self):
        """CollectionResource.__getitem__() raises `KeyError` if `name' is not an ObjectId or child name
        """
        with self.assertRaises(KeyError):
            self.col_rec['nonsense']

    def test_collection_is_read_only(self):
        """CollectionResource.collection is read-only
        """
        with self.assertRaises(AttributeError):
            self.col_rec.collection = testing.mock.MockDocument

    def test_collection_is_set(self):
        """CollectionResource.collection is set correctly
        """
        self.assertEqual(self.col_rec.collection, testing.mock.MockDocument)

    def test_create_returns_mock_document(self):
        """CollectionResource.create() returns a new document
        """
        data = {'name': 'doc 4'}
        doc = self.col_rec.create(data)
        self.assertIsInstance(doc, testing.mock.MockDocument)

    def test_create_sets_value(self):
        """CollectionResource.create() sets correct values
        """
        data = {'name': 'doc 4'}
        doc = self.col_rec.create(data)
        self.assertEqual(doc.name, data['name'])

    def test_create_saves_to_mongo(self):
        """CollectionResource.create() saves a new document to MongoDB
        """
        data = {'name': 'doc 4'}
        doc = self.col_rec.create(data)
        result = testing.mock.MockDocument.objects.get(id=doc.id)
        self.assertIsInstance(result, testing.mock.MockDocument)

    def test_create_sets_values_in_mongo(self):
        """CollectionResource.create() sets correct values to new document in MongoDB
        """
        data = {'name': 'doc 4'}
        doc = self.col_rec.create(data)
        result = testing.mock.MockDocument.objects.get(id=doc.id)
        self.assertEqual(result.name, doc.name)

    def test_create_raises_raises_exception_if_data_is_invalid(self):
        """CollectionResource.create() raises ValidationError if data is invalid
        """
        data = {'number': 'invalid integer'}
        from mongoengine import ValidationError
        with self.assertRaises(ValidationError):
            self.col_rec.create(data)

    def test_create_raises_exception_if_unique_field_already_exists(self):
        """CollectionResource.create() raises NotUniqueError if unique field already existsßß
        """
        self.make_data(3, save=True)
        data = {'name': 'document 1'}
        from mongoengine import NotUniqueError
        with self.assertRaises(NotUniqueError):
            self.col_rec.create(data)

    def test_retrieve_accepts_valid_query_types(self):
        """CollectionResource.retrieve() does not raise TypeError if query is a dict or None
        """
        good_queries = ({'name': 'Document 0'}, None)
        for query in good_queries:
            try:
                self.col_rec.retrieve(query)
            except TypeError as err:
                self.fail(err)

    def test_retrieve_returns_all_docs_without_query(self):
        """CollectionResource.retrieve() returns all documents if no query is provided
        """
        self.make_data(3, save=True)
        results = self.col_rec.retrieve()
        names = [x.name for x in results]
        self.assertEqual(len(results), 3)
        for x in results:
            self.assertIn(x.name, names)

    def test_retrieve_returns_matching_docs(self):
        """CollectionResource.retrieve() returns all documents matching query
        """
        self.make_data(save=True)
        query = {'fact': True}
        results = self.col_rec.retrieve(query)
        names = [x.name for x in results]
        self.assertEqual(len(results), 8)
        for x in results:
            self.assertIn(x.name, names)

    def test_retrieve_only_returns_explicitly_named_fields(self):
        """CollectionResource.retrieve() only returns explicitly named fields if set
        """
        self.make_data(20, save=True)
        fields = ['number']
        results = self.col_rec.retrieve(fields=fields)
        for doc in results:
            self.assertIsNone(doc.name)

    def test_retrieve_limit_default_100(self):
        """CollectionResource.retrieve() limits 100 results by default
        """
        self.make_data(200, save=True)
        results = self.col_rec.retrieve()
        results = [x.name for x in results]
        self.assertEqual(100, len(results))

    def test_retrieve_limit_override(self):
        """CollectionResource.retrieve() can return an arbitrary number of documents
        """
        self.make_data(200, save=True)
        results = self.col_rec.retrieve(limit=42)
        results = [x.name for x in results]
        self.assertEqual(42, len(results))

    def test_retrieve_skip_default(self):
        """CollectionResource.retrieve() skips 0 results by default
        """
        self.make_data(200, save=True)
        results = self.col_rec.retrieve()
        results = [x.name for x in results]
        self.assertEqual(results[0], 'document 0')

    def test_retrieve_skip_override(self):
        """CollectionResource.retrieve() can skip an arbitrary number of documents
        """
        self.make_data(200, save=True)
        results = self.col_rec.retrieve(skip=42)
        results = [x.name for x in results]
        self.assertEqual(results[0], 'document 42')
        self.assertEqual(results[-1], 'document 141')

    def test_retrieve_returns_empty_list_if_nothing_found(self):
        """CollectionResource.retrieve() returns empty list if nothing is found
        """
        expected = []
        result = [x for x in self.col_rec.retrieve()]
        self.assertEqual(expected, result)


class DocumentResourceTestCase(MockResourceTestCase):
    """
    Integration tests for :class:`resources.DocumentResource`.
    """

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        super(DocumentResourceTestCase, self).setUp()
        docs = self.make_data(20, save=True)
        self.doc_ids = [d.id for d in docs]
        self.doc_rec = self.col_rec[self.doc_ids[0]]

    def test_id_is_read_only(self):
        """DocumentResource.id is read-only
        """
        with self.assertRaises(AttributeError):
            self.doc_rec.id = 'string'

    def test_id_is_string(self):
        """DocumentResource.id returns a string
        """
        self.assertIsInstance(self.doc_rec.id, str)

    def test_id_is_objectid(self):
        """DocumentResource.id is properly set as target ObjectId
        """
        self.assertEqual(self.doc_rec.id, str(self.doc_ids[0]))

    def test_collection_is_read_only(self):
        """DocumentResource.collection is read-only
        """
        with self.assertRaises(AttributeError):
            self.doc_rec.collection = 'string'

    def test_collection_is_parent_collection(self):
        """DocumentResource.collection is the same as it's parent's
        """
        self.assertEqual(
            self.doc_rec.collection,
            self.col_rec.collection)

    def test_retrieve_returns_document(self):
        """DocumentResource.retrieve() returns a document if it exists
        """
        result = self.doc_rec.retrieve()
        self.assertIsInstance(result, testing.mock.MockDocument)
        self.assertEqual(result.id, self.doc_ids[0])

    def test_retrieve_raises_exception_if_doc_does_not_exist(self):
        """DocumentResource.retrieve() raises DoesNotExist if document does not exist
        """
        from bson import ObjectId
        obj_id = ObjectId()
        bad_doc_rec = self.col_rec[obj_id]
        from mongoengine import DoesNotExist
        with self.assertRaises(DoesNotExist):
            bad_doc_rec.retrieve()

    def test_retrieve_only_returns_explicitly_named_fields(self):
        """DocumentResource.retrieve() only returns explicitly named fields if set
        """
        fields = ['name']
        result = self.doc_rec.retrieve(fields)
        self.assertIsNone(result.number)

    def test_update_returns_true(self):
        """DocumentResource.update() returns `True` if update was successful
        """
        update = {'name': 'new name'}
        result = self.doc_rec.update(update)
        self.assertTrue(result)

    def test_update_saves_to_mongodb(self):
        """DocumentResource.update() saves changes to MongoDB
        """
        update = {'name': 'new name'}
        self.doc_rec.update(update)
        result = testing.mock.MockDocument.objects.get(id=self.doc_ids[0])
        self.assertEqual(result.name, update['name'])

    def test_update_raises_exception_if_document_does_not_exist(self):
        """DocumentResource.update() raises DoesNotExist if document does not exist
        """
        from bson import ObjectId
        obj_id = ObjectId()
        bad_doc_rec = self.col_rec[obj_id]
        update = {'name': 'new name'}
        from mongoengine import DoesNotExist
        with self.assertRaises(DoesNotExist):
            bad_doc_rec.update(update)

    def test_update_raises_exception_if_data_is_invalid(self):
        """DocumentResource.update() raises ValidationError with invalid data
        """
        update = {'number': 'invalid number'}
        from mongoengine import ValidationError
        with self.assertRaises(ValidationError):
            self.doc_rec.update(update)

    def test_delete_removes_from_mongodb(self):
        """DocumentResource.delete() removes the document from MongoDB
        """
        self.doc_rec.delete()
        result = testing.mock.MockDocument.objects(id=self.doc_ids[0])
        self.assertFalse(result)
