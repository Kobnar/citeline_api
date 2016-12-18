from stackcite_api import testing


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
        result = view.index()
        self.assertIsInstance(result, dict)
