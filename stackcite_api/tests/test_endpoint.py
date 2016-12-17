from stackcite_api import testing


class IndexAPIEndpointTests(testing.endpoint.APIEndpointTestCase):

    def test_index_returns_302_FOUND(self):
        response = self.test_app.get('/')
        self.assertEqual(302, response.status_code)
