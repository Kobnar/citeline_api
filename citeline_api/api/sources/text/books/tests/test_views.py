from citeline_api import testing


class BookSourceCollectionViewsIntegrationTestCase(
        testing.views.CollectionViewTestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    # Define resource and view classes
    from ..resources import BookSourceCollection
    from ..views import BookSourceCollectionViews
    RESOURCE_CLASS = BookSourceCollection
    VIEW_CLASS = BookSourceCollectionViews

    def get_view(self, name='book'):
        return super().get_view(name)

    def setUp(self):
        from citeline.data import Person
        from citeline.data import BookSource
        Person.drop_collection()
        BookSource.drop_collection()

    def test_create_book_source_with_author_id_string_reference(self):
        """BookSourceCollectionViews.create() accepts a string-formatted ObjectId as an author reference
        """
        from citeline.data import Person
        from citeline_api.api.exceptions import APIBadRequest
        author = Person()
        author.name.full = 'John Nobody Doe'
        author.save()
        data = {
            'title': 'Test BookSource',
            'authors': [str(author.id)]}
        view = self.get_view()
        view.request.json_body = data
        try:
            view.create()
        except APIBadRequest as err:
            self.fail(err)

    def test_create_raises_exception_for_invalid_ISBN13(self):
        """CitationCollectionViews.create() raises APIBadRequest exception with an invalid ISBN-13
        """
        from citeline.data import Person
        from citeline_api.api.exceptions import APIBadRequest
        author = Person()
        author.name.full = 'John Nobody Doe'
        author.save()
        data = {
            'title': 'Test Citation',
            'authors': [str(author.id)],
            'isbn13': 'badISBN'}
        view = self.get_view()
        view.request.json_body = data
        with self.assertRaises(APIBadRequest):
            view.create()

    def test_create_raises_exception_for_invalid_ISBN10(self):
        """CitationCollectionViews.create() raises APIBadRequest exception with an invalid ISBN-10
        """
        from citeline.data import Person
        from citeline_api.api.exceptions import APIBadRequest
        author = Person()
        author.name.full = 'John Nobody Doe'
        author.save()
        data = {
            'title': 'Test Citation',
            'authors': [str(author.id)],
            'isbn10': 'badISBN'}
        view = self.get_view()
        view.request.json_body = data
        with self.assertRaises(APIBadRequest):
            view.create()


class BookSourceDocumentViewsIntegrationTestCase(
        testing.views.DocumentViewTestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    # Define resource and view classes
    from ..resources import BookSourceCollection
    from ..views import BookSourceDocumentViews
    RESOURCE_CLASS = BookSourceCollection
    VIEW_CLASS = BookSourceDocumentViews

    def setUp(self):
        from citeline.data import BookSource
        BookSource.drop_collection()

    def make_book(self, save=False):
        from citeline.data import Person
        from citeline.testing.data import book_sources as bks
        from random import randint
        from .test_resources import make_book as mk_prs
        author = Person(name__full='John Nobody Doe')
        if save:
            author.save()
        books = bks()
        rand_idx = randint(0, len(books) - 1)
        book = mk_prs(books[rand_idx], [author], save)
        return book

    def get_view(self, object_id=None, name='book'):
        return super().get_view(object_id, name)
