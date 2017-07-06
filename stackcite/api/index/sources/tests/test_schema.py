import unittest

from stackcite.api import testing


class UpdateSourceTests(unittest.TestCase):

    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from ..schema import UpdateSource
        self.schema = UpdateSource()

    def test_source_type_loads_from_type(self):
        """UpdateSource.source_type loads from 'type' field
        """
        data = {'type': 'BOOK'}
        result, errors = self.schema.load(data)
        result = result.get('source_type')
        self.assertEqual(result, 'BOOK')

    def test_description_accepts_none_value(self):
        """UpdateSource.description accepts None value
        """
        data = {'description': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('description', result)

    def test_authors_accepts_empty_list(self):
        """UpdateSource.authors accepts an empty list
        """
        data = {'authors': []}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('published', result)

    def test_editors_accepts_none_value(self):
        """UpdateSource.editors accepts an empty list
        """
        data = {'editors': []}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('editors', result)

    def test_edition_accepts_none_value(self):
        """UpdateSource.edition accepts None value
        """
        data = {'edition': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('edition', result)

    def test_publisher_accepts_none_value(self):
        """UpdateSource.publisher accepts None value
        """
        data = {'publisher': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('publisher', result)

    def test_published_accepts_none_value(self):
        """UpdateSource.published accepts None value
        """
        data = {'published': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('published', result)

    def test_location_accepts_none_value(self):
        """UpdateSource.location accepts None value
        """
        data = {'location': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('location', result)

    def test_isbn10_accepts_none_value(self):
        """UpdateSource.isbn10 accepts None value
        """
        data = {'isbn10': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('isbn10', result)

    def test_isbn13_accepts_none_value(self):
        """UpdateSource.isbn13 accepts None value
        """
        data = {'isbn13': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('isbn13', result)


class CreateSourceTests(unittest.TestCase):

    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from ..schema import CreateSource
        self.schema = CreateSource()

    def test_source_type_default_is_source(self):
        """CreateSource.source_type default value is SOURCE
        """
        data = {'title': 'Test Source'}
        expected = 'SOURCE'
        result, errors = self.schema.load(data)
        result = result.get('source_type')
        self.assertEqual(expected, result)

    def test_title_is_required(self):
        """CreateSource.title is a required field
        """
        result = self.schema.load({}).errors.keys()
        self.assertIn('title', result)

    def test_text_requires_authors(self):
        """CreateSource.authors is required if type is TEXT
        """
        data = {
            'type': 'TEXT',
            'title': 'Test Source'}
        result = self.schema.load(data).errors.keys()
        self.assertIn('authors', result)

    def test_book_requires_authors(self):
        """CreateSource.authors is required if type is BOOK
        """
        data = {
            'type': 'BOOK',
            'title': 'Test Source'}
        result = self.schema.load(data).errors.keys()
        self.assertIn('authors', result)


class RetrieveSourcesTests(unittest.TestCase):

    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from ..schema import RetrieveSources
        self.schema = RetrieveSources()

    def test_accepts_q_field(self):
        """RetrieveSources accepts "q" field
        """
        data = {'q': 'Some query string.'}
        result, errors = self.schema.load(data)
        self.assertIn('q', result)
