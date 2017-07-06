import unittest

from stackcite.api import testing


class MockAPIMongoResourceTestCase(unittest.TestCase):

    layer = testing.layers.MongoTestLayer

    def setUp(self):
        from ..models import MockDocument
        MockDocument.drop_collection()
        from ..resources import MockAPICollectionResource
        self.test_col = MockAPICollectionResource(None, 'test_collection')


class MockAPICollectionResourceTestCase(MockAPIMongoResourceTestCase):

    def test_create_fails_validation_with_invalid_data(self):
        """MockAPICollectionResource.create() fails validation with invalid data
        """
        data = {'fact': 42}
        from mongoengine import ValidationError
        with self.assertRaises(ValidationError):
            self.test_col.create(data)

    def test_load_fails_validation_with_invalid_data(self):
        """MockAPICollectionResource.load() fails validation with invalid data
        """
        data = {'fact': 42}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.test_col.load(data)

    def test_getitem_returns_mock_api_document_resource(self):
        """MockAPICollectionResource.__getitem__() returns an instance of MockAPIDocumentResource
        """
        from ..utils import create_mock_data
        docs = create_mock_data(count=1, save=True)
        doc_id = docs[0].id
        doc_resource = self.test_col[doc_id]
        from ..resources import MockAPIDocumentResource
        self.assertIsInstance(doc_resource, MockAPIDocumentResource)


class MockAPIDocumentResourceTestCase(MockAPIMongoResourceTestCase):

    def setUp(self):
        super().setUp()
        from ..utils import create_mock_data
        docs = create_mock_data(count=1, save=True)
        doc_id = docs[0].id
        self.test_doc = self.test_col[doc_id]

    def test_update_fails_validation_with_invalid_data(self):
        """MockAPIDocumentResource.update() fails validation with invalid data
        """
        data = {'fact': 42}
        from mongoengine import ValidationError
        with self.assertRaises(ValidationError):
            self.test_doc.update(data)

    def test_load_fails_validation_with_invalid_data(self):
        """MockAPICollectionResource.load() fails validation with invalid data
        """
        data = {'fact': 42}
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.test_col.load(data)
