from stackcite.api import testing


class CitationCollectionViewsIntegrationTestCase(
        testing.views.CollectionViewTestCase):

    layer = testing.layers.MongoTestLayer

    # Define resource and view classes
    from ..resources import CitationCollection
    from stackcite.api.views import APICollectionViews
    RESOURCE_CLASS = CitationCollection
    VIEW_CLASS = APICollectionViews

    def make_view(self, name='citation'):
        return super().make_view(name)

    def setUp(self):
        from stackcite import data
        data.Source.drop_collection()
        data.Citation.drop_collection()

    def test_create_citation_source_with_source_id_string_reference(self):
        """CitationCollectionViews.create() accepts a string-formatted ObjectId as a source
        """
        from stackcite import data
        from stackcite.api.exceptions import APIBadRequest

        source = data.Source(title='Test Source')
        source.save()

        data = {
            'source': str(source.id),
            'note': 'A test source.'}

        view = self.make_view()
        view.request.json_body = data
        try:
            view.create()
        except APIBadRequest as err:
            self.fail(err)


class CitationDocumentViewsIntegrationTestCase(
        testing.views.DocumentViewTestCase):

    layer = testing.layers.MongoTestLayer

    # Define resource and view classes
    from ..resources import CitationCollection
    from stackcite.api.views import APIDocumentViews
    RESOURCE_CLASS = CitationCollection
    VIEW_CLASS = APIDocumentViews

    def setUp(self):
        from stackcite import data
        data.Source.drop_collection()
        data.Citation.drop_collection()

    def make_view(self, object_id=None, name='citation'):
        return super().make_view(object_id, name)
