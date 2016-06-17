from citeline_api import testing


class TextSourceCollectionViewsIntegrationTestCase(
        testing.views.CollectionViewTestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    # Define resource and view classes
    from ..resources import TextSourceCollection
    from ..views import TextSourceCollectionViews
    RESOURCE_CLASS = TextSourceCollection
    VIEW_CLASS = TextSourceCollectionViews

    def get_view(self, name='text'):
        return super().get_view(name)

    def setUp(self):
        from citeline.data import Person
        from citeline.data import TextSource
        Person.drop_collection()
        TextSource.drop_collection()

    def test_create_text_source_with_author_id_string_reference(self):
        """TextSourceCollectionViews.create() accepts a string-formatted ObjectId as an author reference
        """
        from citeline.data import Person
        from citeline_api.api.exceptions import APIBadRequest
        author = Person()
        author.name.full = 'John Nobody Doe'
        author.save()
        data = {
            'title': 'Test TextSource',
            'authors': [str(author.id)]}
        view = self.get_view()
        view.request.json_body = data
        try:
            view.create()
        except APIBadRequest as err:
            self.fail(err)


class TextSourceDocumentViewsIntegrationTestCase(
        testing.views.DocumentViewTestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    # Define resource and view classes
    from ..resources import TextSourceCollection
    from ..views import TextSourceDocumentViews
    RESOURCE_CLASS = TextSourceCollection
    VIEW_CLASS = TextSourceDocumentViews

    def setUp(self):
        from citeline.data import TextSource
        TextSource.drop_collection()

    def make_text(self, save=False):
        from citeline.data import Person
        from citeline.testing.data import text_sources as txts
        from random import randint
        from .test_resources import make_text as mk_prs
        author = Person(name__full='John Nobody Doe')
        if save:
            author.save()
        texts = txts()
        rand_idx = randint(0, len(texts) - 1)
        text = mk_prs(texts[rand_idx], [author], save)
        return text

    def get_view(self, object_id=None, name='text'):
        return super().get_view(object_id, name)
