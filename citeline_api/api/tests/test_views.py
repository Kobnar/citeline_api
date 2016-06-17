from citeline_api import testing


class APIIndexViewsTests(testing.views.ViewTestCase):

    layer = testing.layers.UnitTestLayer

    # Define resource and view class under test
    from ..resources import APIIndex
    from ..views import APIIndexViews
    RESOURCE_CLASS = APIIndex
    VIEW_CLASS = APIIndexViews

    def get_view(self, name='api_v1'):
        return super().get_view(name)

    def test_returns_dict(self):
        """APIIndexViews.main() returns a dictionary
        """
        view = self.get_view()
        result = view.main()
        self.assertIsInstance(result, dict)


class APICollectionViewsTestCase(testing.views.CollectionViewTestCase):
    """
    A base test case establishing tests for :class:`.APICollectionViews`
    """
    layer = testing.layers.MongoIntegrationTestLayer

    # Define "mock" traversal resources:
    from ..resources import APICollection
    class _MockAPICollectionResource(APICollection):
        from ..resources import APIDocument
        class _MockAPIDocumentResource(APIDocument):
            pass
        _collection = testing.mock.MockDocument
        _document_resource = _MockAPIDocumentResource

    # Define resource and view class under test
    from ..views import APICollectionViews
    RESOURCE_CLASS = _MockAPICollectionResource
    VIEW_CLASS = APICollectionViews

    def setUp(self):
        testing.mock.MockDocument.drop_collection()
        super().setUp()

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


class APICollectionViewsCreateTestCase(APICollectionViewsTestCase):

    def test_create_returns_id(self):
        """APICollectionViews.create() returns a valid ObjectId
        """
        docs = self.make_data()
        view = self.get_view()
        for doc in docs:
            expected = {
                'id': doc.id,
                'name': doc.name,
                'number': doc.number,
                'fact': doc.fact}
            view.request.json_body = expected
            result = view.create()
            self.assertTrue('id' in result.keys())
            self.assertIsNotNone(result['id'])
            from bson import ObjectId
            try:
                ObjectId(result['id'])
            except TypeError:
                self.fail('APICollectionViews returned something other than '
                          'an ObjectId')
                
    def test_create_returns_person(self):
        """APICollectionViews.create() returns a valid document dictionary
        """
        docs = self.make_data()
        view = self.get_view()
        for doc in docs:
            data = {
                'name': doc.name,
                'number': doc.number,
                'fact': doc.fact}
            view.request.json_body = data
            result = view.create()
            expected = doc.serialize()
            expected['id'] = result['id']
            self.assertEqual(expected, result)

    def test_create_creates_new_person(self):
        """APICollectionViews.create() saves a new MockDocument to the database
        """
        docs = self.make_data()
        view = self.get_view()
        from mongoengine import DoesNotExist, ValidationError
        for doc in docs:
            data = {
                'name': doc.name,
                'number': doc.number,
                'fact': doc.fact}
            view.request.json_body = data
            result = view.create()
            try:
                testing.mock.MockDocument.objects.get(id=result.get('id'))
            except (DoesNotExist, ValidationError) as err:
                self.fail(err)

    def test_create_returns_200_OK(self):
        """APICollectionViews.create() returns 200 OK if successful
        """
        docs = self.make_data()
        view = self.get_view()
        for doc in docs:
            data = {
                'name': doc.name,
                'number': doc.number,
                'fact': doc.fact}
            view.request.json_body = data
            view.create()
            result = view.request.response.status_code
            self.assertEqual(result, 200)

    def test_create_existing_raises_400_BAD_REQUEST(self):
        """APICollectionViews.create() raises 400 BAD REQUEST if the document exists
        """
        view = self.get_view()
        # Create an existing person:
        existing_doc = testing.mock.MockDocument()
        existing_doc.name = 'Mock Document'
        existing_doc.save()
        # Create the same person:
        duplicate_doc = {'name': 'Mock Document'}
        view.request.json_body = duplicate_doc
        from ..exceptions import APIBadRequest
        with self.assertRaises(APIBadRequest):
            view.create()

    def test_no_json_body_returns_400_BadRequest(self):
        """APICollectionViews.create() returns 400 BAD REQUEST if no json_body provided
        """
        self.fail('Need integration tests for JSON errors')


class APICollectionViewsRetrieveTestCase(APICollectionViewsTestCase):

    def test_retrieve_gets_all_documents(self):
        """APICollectionViews.retrieve() returns all expected results
        """
        docs = self.make_data(save=True)
        view = self.get_view()
        view.request.params = {}
        results = view.retrieve()
        results = [d['name'] for d in results]
        expected = [d.name for d in docs]
        for doc in results:
            self.assertIn(doc, expected)

    def test_retrieve_includes_properly_serialized_id(self):
        """APICollectionViews.retrieve() returned an id
        """
        self.make_data(save=True)
        view = self.get_view()
        view.request.params = {}
        results = view.retrieve()
        from bson import ObjectId
        for person in results:
            try:
                ObjectId(person['id'])
            except TypeError:
                self.fail('APICollectionViews.retrieve() return an invalid id')
            except KeyError:
                self.fail('APICollectionViews.retrieve() did not return an id')

    def test_retrieve_includes_intended_fields(self):
        """ APICollectionViews.retrieve() properly serializes each object
        """
        docs = self.make_data(save=True)
        view = self.get_view()
        view.request.params = {}
        results = view.retrieve()
        for idx, result in enumerate(results):
            expected = docs[idx].serialize()
            expected['id'] = result['id']
            self.assertEqual(expected, result)

    def test_retrieve_returns_200_OK(self):
        """APICollectionViews.retrieve() returns 200 OK if documents exist
        """
        self.make_data(save=True)
        view = self.get_view()
        view.retrieve()
        result = view.request.response.status_code
        self.assertEqual(result, 200)

    def test_retrieve_returns_empty_list_if_no_results(self):
        """APICollectionViews.retrieve() returns an empty list if there are no results
        """
        view = self.get_view()
        view.request.params = {'name': 'John'}
        expected = []
        result = view.retrieve()
        self.assertEqual(expected, result)

    def test_retrieve_returns_404_NOT_FOUND_if_no_results(self):
        """APICollectionViews.retrieve() returns 404 NOT FOUND if there are no results
        """
        view = self.get_view()
        view.request.params = {'name': 'John'}
        view.retrieve()
        result = view.request.response.status_code
        self.assertEqual(404, result)


class APIDocumentViewsTestCase(testing.views.DocumentViewTestCase):
    """
    A test case for :class:`.APIDocumentViews`.
    """
    layer = testing.layers.MongoIntegrationTestLayer

    # Define "mock" traversal resources:
    from ..resources import APICollection
    class _MockAPICollectionResource(APICollection):
        from ..resources import APIDocument
        class _MockAPIDocumentResource(APIDocument):
            pass
        _collection = testing.mock.MockDocument
        _document_resource = _MockAPIDocumentResource

    # Define resource and view class under test
    from ..views import APIDocumentViews
    RESOURCE_CLASS = _MockAPICollectionResource
    VIEW_CLASS = APIDocumentViews

    def setUp(self):
        testing.mock.MockDocument.drop_collection()
        super().setUp()

    def get_view(self, object_id=None, name='documents'):
        return super().get_view(object_id, name)

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


class APIDocumentViewsRetrieveTestCase(APIDocumentViewsTestCase):

    def test_retrieve_returns_correct_person(self):
        """APIDocumentViews.retrieve() returns correct Person data
        """
        documents = self.make_data(save=True)
        for doc in documents:
            view = self.get_view(doc.id)
            # Work around missing default schema:
            view.request.params = ()
            result = view.retrieve()
            self.assertEqual(doc.serialize(), result)

    def test_retrieve_filters_fields(self):
        """APIDocumentViews.retrieve() filters explicitly named fields
        """
        documents = self.make_data(save=True)
        for document in documents:
            view = self.get_view(document.id)
            view.request.params = ['id', 'number']
            result = view.retrieve()
            self.assertEqual(str(document.id), result['id'])
            self.assertNotIn('name', result.keys())
            self.assertEqual(document.number, result['number'])

    def test_existing_person_returns_200_OK(self):
        """APIDocumentViews.retrieve() returns 200 OK if found
        """
        documents = self.make_data(save=True)
        ids = [doc.id for doc in documents]
        for pid in ids:
            view = self.get_view(pid)
            # Work around missing default schema:
            view.request.params = ()
            view.retrieve()
            result = view.request.response.status_code
            self.assertEqual(result, 200)

    def test_missing_document_raises_404_NOT_FOUND(self):
        """APIDocumentViews.retrieve() raises 404 NOT FOUND if document does not exist
        """
        from bson import ObjectId
        pid = ObjectId()
        view = self.get_view(pid)
        # Work around missing default schema:
        view.request.params = ()
        from ..exceptions import APINotFound
        with self.assertRaises(APINotFound):
            view.retrieve()


class APIDocumentViewsUpdateTestCase(APIDocumentViewsTestCase):

    def test_update_returns_changes(self):
        """APIDocumentViews.update() returns updated Person data
        """
        # Build data:
        documents = self.make_data(save=True)
        for doc in documents:
            # Build view:
            view = self.get_view(doc.id)
            view.request.json_body = {'fact': not doc.fact}
            # Update and verify:
            result = view.update()
            self.assertEqual(doc.name, result['name'])
            self.assertNotEqual(doc.fact, result['fact'])

    def test_update_changes_person(self):
        """APIDocumentViews.update() changes Person data in MongoDB
        """
        # Build data:
        documents = self.make_data(save=True)
        for doc in documents:
            # Build view:
            view = self.get_view(doc.id)
            view.request.json_body = {'fact': not doc.fact}
            # Update and compare to direct query:
            view_result = view.update()
            mongo_result = testing.mock.MockDocument.objects.get(id=doc.id)
            self.assertEqual(mongo_result.serialize(), view_result)

    def test_update_changes_only_one_person(self):
        """APIDocumentViews.update() does not change any other data in MongoDB
        """
        # Build data:
        documents = self.make_data(save=True)
        # Select a random target and update its name:
        from random import randint
        target = documents.pop(randint(0, len(documents) - 1))
        view = self.get_view(target.id)
        view.request.json_body = {'name': 'Unique Document'}
        view.update()
        # Check that everybody else is the same with a direct query:
        for doc in documents:
            mongo_result = testing.mock.MockDocument.objects.get(id=doc.id)
            self.assertNotEqual(mongo_result.fact, 'Unique Document')

    def test_successful_update_returns_200_OK(self):
        """APIDocumentViews.update() returns 200 OK if successful
        """
        documents = self.make_data(save=True)
        pids = [doc.id for doc in documents]
        for pid in pids:
            view = self.get_view(pid)
            view.request.json_body = {'fact': True}
            view.update()
            result = view.request.response.status_code
            self.assertEqual(result, 200)

    def test_missing_person_raises_404_NotFound(self):
        """APIDocumentViews.update() raises 404 NOT FOUND if person does not exist
        """
        from bson import ObjectId
        pid = ObjectId()
        view = self.get_view(pid)
        view.request.json_body = {'fact': True}
        from ..exceptions import APINotFound
        with self.assertRaises(APINotFound):
            view.update()


class APIDocumentViewsDeleteTestCase(APIDocumentViewsTestCase):

    def test_delete_deletes_correct_person(self):
        """APIDocumentViews.delete() deletes the correct document in MongoDB
        """
        # Build data:
        documents = self.make_data(save=True)
        # Delete a random person:
        from random import randint
        target = documents.pop(randint(0, len(documents) - 1))
        view = self.get_view(target.id)
        from ..exceptions import APINoContent
        try:
            view.delete()
        except APINoContent:
            # Make sure that person is deleted
            from mongoengine import DoesNotExist
            with self.assertRaises(DoesNotExist):
                testing.mock.MockDocument.objects.get(id=target.id)

    def test_delete_deletes_only_one_person(self):
        """APIDocumentViews.delete() does not delete any other document in MongoDB
        """
        # Build data:
        documents = self.make_data(save=True)
        # Delete a random person:
        from random import randint
        target = documents.pop(randint(0, len(documents) - 1))
        view = self.get_view(target.id)
        from ..exceptions import APINoContent
        try:
            view.delete()
        except APINoContent:
            # Make sure nobody else is deleted
            from mongoengine import DoesNotExist
            for doc in documents:
                try:
                    testing.mock.MockDocument.objects.get(id=doc.id)
                except DoesNotExist:
                    self.fail('{} should exist in the database'.format(doc.id))

    def test_delete_sucess_raises_204_NO_CONTENT(self):
        """APIDocumentViews.delete() raises 204 NO CONTENT if successful
        """
        # Build data:
        documents = self.make_data(save=True)
        # Delete a random document:
        from random import randint
        target = documents.pop(randint(0, len(documents) - 1))
        view = self.get_view(target.id)
        from ..exceptions import APINoContent
        with self.assertRaises(APINoContent):
            view.delete()

    def test_delete_missing_person_returns_404_NotFound(self):
        """APIDocumentViews.delete() returns 404 NOT FOUND if person does not exist
        """
        # Build data:
        self.make_data(save=True)
        from bson import ObjectId
        pid = ObjectId()
        view = self.get_view(pid)
        from ..exceptions import APINotFound
        with self.assertRaises(APINotFound):
            view.delete()
