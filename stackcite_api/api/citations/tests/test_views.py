from stackcite_api import testing


class CitationCollectionViewsIntegrationTestCase(
        testing.views.CollectionViewTestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    # Define resource and view classes
    from ..resources import CitationCollection
    from stackcite_api.api.views import APICollectionViews
    RESOURCE_CLASS = CitationCollection
    VIEW_CLASS = APICollectionViews

    def get_view(self, name='citation'):
        return super().get_view(name)

    def setUp(self):
        from stackcite import data
        data.Source.drop_collection()
        data.Citation.drop_collection()

    def test_create_citation_source_with_source_id_string_reference(self):
        """CitationCollectionViews.create() accepts a string-formatted ObjectId as a source
        """
        from stackcite import data
        from stackcite_api.api.exceptions import APIBadRequest

        source = data.Source(title='Test Source')
        source.save()

        data = {
            'source': str(source.id),
            'note': 'A test source.'}

        view = self.get_view()
        view.request.json_body = data
        try:
            view.create()
        except APIBadRequest as err:
            self.fail(err)


class CitationDocumentViewsIntegrationTestCase(
        testing.views.DocumentViewTestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    # Define resource and view classes
    from ..resources import CitationCollection
    from stackcite_api.api.views import APIDocumentViews
    RESOURCE_CLASS = CitationCollection
    VIEW_CLASS = APIDocumentViews

    def setUp(self):
        from stackcite import data
        data.Source.drop_collection()
        data.Citation.drop_collection()

    def make_citation(self, save=False):
        from stackcite import data
        from .test_resources import make_citation
        source = data.Source(title='Test Source')
        source.save()
        return make_citation({}, source, save=True)

    def get_view(self, object_id=None, name='citation'):
        return super().get_view(object_id, name)
