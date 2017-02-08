import unittest

from stackcite.api import testing


class MockDocumentIntegrationTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from ..models import MockDocument
        MockDocument.drop_collection()

    def test_name_is_unique(self):
        """MockDocument.name is a unique field
        """
        from ..models import MockDocument
        doc_0 = MockDocument(name='Document')
        doc_0.save()
        doc_1 = MockDocument(name='Document')
        from mongoengine import NotUniqueError
        with self.assertRaises(NotUniqueError):
            doc_1.save()

    def test_serialize_returns_proper_dict(self):
        """MockDocument.serialize() returns a proper dict
        """
        from ..models import MockDocument
        doc = MockDocument(name='Document', number=42, fact=True)
        doc.save()
        expected = {
            'id': str(doc.id),
            'name': 'Document',
            'number': 42,
            'fact': True}
        result = doc.serialize()
        self.assertEqual(expected, result)

    def test_deserialize_sets_all_values(self):
        """MockDocument.deserialize() sets all values in dict
        """
        data = {
            'name': 'Document',
            'number': 42,
            'fact': True}
        from ..models import MockDocument
        doc = MockDocument()
        doc.deserialize(data)
        for k, expected in data.items():
            result = getattr(doc, k)
            self.assertEqual(expected, result)

    def test_allow_inheritance(self):
        """MockDocument allows inheritance
        """
        try:
            from ..models import MockDocument
            class SubDocument(MockDocument):
                pass
        except ValueError as err:
            msg = 'Unexpected ValueError: {}'.format(err)
            self.fail(msg)

    def test_search_text_returns_matching_documents(self):
        """A search_text() query returns matching MockDocument instances
        """
        names = [
            'Some Important Document',
            'Some Other Document',
            'Another Important Document']
        from ..models import MockDocument
        for name in names:
            MockDocument(name=name).save()
        docs = MockDocument.objects.search_text('important').all()
        expected = {
            'Some Important Document',
            'Another Important Document'}
        results = {d.name for d in docs}
        self.assertEqual(expected, results)

    def test_raw_text_search_returns_matching_documents(self):
        """A raw text search query returns matching MockDocument instances
        """
        names = [
            'Some Important Document',
            'Some Other Document',
            'Another Important Document']
        from ..models import MockDocument
        for name in names:
            MockDocument(name=name).save()
        raw_query = {'$text': {'$search': 'important'}}
        docs = MockDocument.objects(__raw__=raw_query).all()
        expected = {
            'Some Important Document',
            'Another Important Document'}
        results = {d.name for d in docs}
        self.assertEqual(expected, results)
