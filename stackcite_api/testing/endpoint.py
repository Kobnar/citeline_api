import unittest

from . import layers


class APIEndpointTestCase(unittest.TestCase):

    layer = layers.WSGIIntegrationTestLayer

    def setUp(self):
        self.test_app = self.make_app()

    @staticmethod
    def make_app():
        from pyramid import paster
        import stackcite_api
        import webtest
        settings = paster.get_appsettings('development.ini')
        app = stackcite_api.main(global_config=None, **settings)
        return webtest.TestApp(app)
