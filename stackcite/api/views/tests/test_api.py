from stackcite.api import testing


class APIExceptionViewsTestCase(testing.views.ExceptionViewTestCase):

    layer = testing.layers.UnitTestLayer

    from ..api import APIExceptionViews
    VIEW_CLASS = APIExceptionViews


class APINotFoundViewsTestCase(APIExceptionViewsTestCase):

    from pyramid.exceptions import HTTPNotFound
    EXCEPTION_CLASS = HTTPNotFound

    def test_status_code_matches_404_exception_code(self):
        """APIExceptionViews.exception() sets status code to 404 (Not Found)
        """
        expected = 404
        view = self.get_view()
        view.exception()
        result = view.request.response.status_code
        self.assertEqual(expected, result)

    def test_code_is_not_none(self):
        """APIExceptionViews.exception() sets code field
        """
        expected = 404
        view = self.get_view()
        result = view.exception()['code']
        self.assertEqual(expected, result)


class APIIndexViewsTestCase(testing.views.ViewTestCase):

    from ..api import APIIndexViews
    VIEW_CLASS = APIIndexViews

    from stackcite.api.resources import APIIndexResource
    RESOURCE_CLASS = APIIndexResource

    def test_retrieve_raises_no_content_exception(self):
        """APIIndexViews raises 204 NO CONTENT exception
        """
        from stackcite.api.exceptions import APINoContent
        view = self.get_view()
        with self.assertRaises(APINoContent):
            view.retrieve()


class APIViewsIntegrationTestCase(object):
    """
    A base test case for API views providing a custom view/schema for the
    :class:`~MockDocument` class.

    NOTE: This class must be defined before any other testing view classes in
    cases of multiple inheritance.
    """

    layer = testing.layers.MongoIntegrationTestLayer

    RESOURCE_CLASS = testing.mock.MockAPICollectionResource


class APICollectionViewsIntegrationTestCase(
        APIViewsIntegrationTestCase,
        testing.views.CollectionViewTestCase):

    # Define resource and view class under test
    from ..api import APICollectionViews
    VIEW_CLASS = APICollectionViews

    def setUp(self):
        testing.mock.MockDocument.drop_collection()
        super().setUp()


class APICollectionViewsCreateTestCase(APICollectionViewsIntegrationTestCase):

    def test_create_returns_id(self):
        """APICollectionViews.create() returns a valid ObjectId
        """
        docs = testing.mock.utils.create_mock_data()
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
                
    def test_create_returns_document(self):
        """APICollectionViews.create() returns a valid document dictionary
        """
        docs = testing.mock.utils.create_mock_data()
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

    def test_create_creates_new_document(self):
        """APICollectionViews.create() saves a new MockDocument to the database
        """
        docs = testing.mock.utils.create_mock_data()
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
        """APICollectionViews.create() returns 201 CREATED if successful
        """
        docs = testing.mock.utils.create_mock_data()
        view = self.get_view()
        for doc in docs:
            data = {
                'name': doc.name,
                'number': doc.number,
                'fact': doc.fact}
            view.request.json_body = data
            view.create()
            result = view.request.response.status_code
            self.assertEqual(result, 201)

    def test_create_existing_raises_400_BAD_REQUEST(self):
        """APICollectionViews.create() raises 409 CONFLICT if the document exists
        """
        view = self.get_view()
        # Create an existing person:
        existing_doc = testing.mock.MockDocument()
        existing_doc.name = 'Mock Document'
        existing_doc.save()
        # Create the same person:
        duplicate_doc = {'name': 'Mock Document'}
        view.request.json_body = duplicate_doc
        from stackcite.api.exceptions import APIConflict
        with self.assertRaises(APIConflict):
            view.create()

    def test_create_invalid_data_raises_400_BAD_REQUEST(self):
        """APICollectionViews.create() raises 400 BAD REQUEST if data fails validation
        """
        view = self.get_view()
        invalid_data = {
            'name': 123,
            'number': 'cats',
            'fact': 'dogs'}
        view.request.json_body = invalid_data
        from stackcite.api.exceptions import APIBadRequest
        with self.assertRaises(APIBadRequest):
            view.create()


class APICollectionViewsRetrieveTestCase(APICollectionViewsIntegrationTestCase):

    def test_retrieve_gets_all_documents(self):
        """APICollectionViews.retrieve() returns all expected results
        """
        docs = testing.mock.utils.create_mock_data(save=True)
        view = self.get_view()
        view.request.params = {}
        results = view.retrieve()['items']
        results = [d['name'] for d in results]
        expected = [d.name for d in docs]
        for doc in results:
            self.assertIn(doc, expected)

    def test_retrieve_includes_properly_serialized_id(self):
        """APICollectionViews.retrieve() returned an id for each result
        """
        testing.mock.utils.create_mock_data(save=True)
        view = self.get_view()
        view.request.params = {}
        results = view.retrieve()['items']
        from bson import ObjectId
        for doc in results:
            try:
                ObjectId(doc['id'])
            except TypeError:
                self.fail('APICollectionViews.retrieve() return a invalid id')
            except KeyError:
                self.fail('APICollectionViews.retrieve() did not return an id')

    def test_retrieve_includes_intended_fields(self):
        """ APICollectionViews.retrieve() properly serializes each object
        """
        docs = testing.mock.utils.create_mock_data(save=True)
        view = self.get_view()
        view.request.params = {}
        results = view.retrieve()['items']
        for idx, result in enumerate(results):
            expected = docs[idx].serialize()
            expected['id'] = result['id']
            self.assertEqual(expected, result)

    def test_retrieve_returns_200_OK(self):
        """APICollectionViews.retrieve() returns 200 OK if documents exist
        """
        testing.mock.utils.create_mock_data(save=True)
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
        result = view.retrieve()['items']
        self.assertEqual(expected, result)

    def test_retrieve_schema_invalidation_raises_400_BAD_REQUEST(self):
        """APICollectionViews.retrieve() raises 400 BAD REQUEST if data fails schema validation
        """
        view = self.get_view()
        invalid_query = {
            'name': 'Document',
            'number': 'some_string',
            'fact': True}
        view.request.params = invalid_query
        from stackcite.api.exceptions import APIBadRequest
        with self.assertRaises(APIBadRequest):
            view.retrieve()


class APIDocumentViewsIntegrationTestCase(
        APIViewsIntegrationTestCase,
        testing.views.DocumentViewTestCase):
    """
    A test case for :class:`.APIDocumentViews`.
    """

    # Define resource and view class under test
    from ..api import APIDocumentViews
    VIEW_CLASS = APIDocumentViews

    def setUp(self):
        testing.mock.MockDocument.drop_collection()
        super().setUp()

    def get_view(self, object_id=None, name='documents'):
        return super().get_view(object_id, name)


class APIDocumentViewsRetrieveTestCase(APIDocumentViewsIntegrationTestCase):

    def test_retrieve_returns_correct_person(self):
        """APIDocumentViews.retrieve() returns correct Person data
        """
        documents = testing.mock.utils.create_mock_data(save=True)
        for doc in documents:
            view = self.get_view(doc.id)
            # Work around missing default schema:
            view.request.params = {}
            result = view.retrieve()
            self.assertEqual(doc.serialize(), result)

    def test_retrieve_filters_fields(self):
        """APIDocumentViews.retrieve() filters explicitly named fields
        """
        documents = testing.mock.utils.create_mock_data(save=True)
        for document in documents:
            view = self.get_view(document.id)
            view.request.params = {'fields': 'id,number'}
            result = view.retrieve()
            self.assertEqual(str(document.id), result['id'])
            self.assertNotIn('name', result.keys())
            self.assertEqual(document.number, result['number'])

    def test_existing_person_returns_200_OK(self):
        """APIDocumentViews.retrieve() returns 200 OK if found
        """
        documents = testing.mock.utils.create_mock_data(save=True)
        ids = [doc.id for doc in documents]
        for pid in ids:
            view = self.get_view(pid)
            # Work around missing default schema:
            view.request.params = {}
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
        view.request.params = {}
        from stackcite.api.exceptions import APINotFound
        with self.assertRaises(APINotFound):
            view.retrieve()


class APIDocumentViewsUpdateTestCase(APIDocumentViewsIntegrationTestCase):

    def test_update_returns_changes(self):
        """APIDocumentViews.update() returns updated Person data
        """
        # Build data:
        documents = testing.mock.utils.create_mock_data(save=True)
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
        documents = testing.mock.utils.create_mock_data(save=True)
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
        documents = testing.mock.utils.create_mock_data(save=True)
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
        documents = testing.mock.utils.create_mock_data(save=True)
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
        from stackcite.api.exceptions import APINotFound
        with self.assertRaises(APINotFound):
            view.update()

    def test_update_invalid_data_raises_400_BAD_REQUEST(self):
        """APIDocumentViews.update() raises 400 BAD REQUEST if data fails validation
        """
        doc = testing.mock.utils.create_mock_data(1, save=True)[0]
        view = self.get_view(doc.id)
        view.request.json_body = {'number': 'cats'}
        from stackcite.api.exceptions import APIBadRequest
        with self.assertRaises(APIBadRequest):
            view.update()


class APIDocumentViewsDeleteTestCase(APIDocumentViewsIntegrationTestCase):

    def test_delete_deletes_correct_person(self):
        """APIDocumentViews.delete() deletes the correct document in MongoDB
        """
        # Build data:
        documents = testing.mock.utils.create_mock_data(save=True)
        # Delete a random person:
        from random import randint
        target = documents.pop(randint(0, len(documents) - 1))
        view = self.get_view(target.id)
        from stackcite.api.exceptions import APINoContent
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
        documents = testing.mock.utils.create_mock_data(save=True)
        # Delete a random person:
        from random import randint
        target = documents.pop(randint(0, len(documents) - 1))
        view = self.get_view(target.id)
        from stackcite.api.exceptions import APINoContent
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
        documents = testing.mock.utils.create_mock_data(save=True)
        # Delete a random document:
        from random import randint
        target = documents.pop(randint(0, len(documents) - 1))
        view = self.get_view(target.id)
        from stackcite.api.exceptions import APINoContent
        with self.assertRaises(APINoContent):
            view.delete()

    def test_delete_missing_person_returns_404_NotFound(self):
        """APIDocumentViews.delete() returns 404 NOT FOUND if person does not exist
        """
        # Build data:
        testing.mock.utils.create_mock_data(save=True)
        from bson import ObjectId
        pid = ObjectId()
        view = self.get_view(pid)
        from stackcite.api.exceptions import APINotFound
        with self.assertRaises(APINotFound):
            view.delete()
