from stackcite.api import testing


class APIIndexViewsTests(testing.views.BaseViewTestCase):

    layer = testing.layers.BaseTestLayer

    # Define resource and view class under test
    from ..resources import APIIndex
    from ..views import APIIndexViews
    RESOURCE_CLASS = APIIndex
    VIEW_CLASS = APIIndexViews

    def make_view(self, name='api_v1'):
        return super().make_view(name)

    def test_returns_dict(self):
        """APIIndexViews.retrieve() returns a dictionary
        """
        view = self.make_view()
        result = view.retrieve()
        self.assertIsInstance(result, dict)
