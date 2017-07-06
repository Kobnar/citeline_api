"""
Endpoint tests are the most expensive tests to perform, as they instantiate an
entire WSGI application to mock full-stack functionality. They are necessary,
however, if you need to capture specific behavior that propagates all the way
up the application (e.g. capturing JSON errors in a request).
"""

import unittest

from . import layers


class APIEndpointTestCase(unittest.TestCase):
    """
    A test case that instantiates the entire WSGI application to enable
    functional testing of various application endpoints.
    """

    layer = layers.WSGITestLayer

    def setUp(self):
        self.test_app = self.make_app()

    @staticmethod
    def make_app():
        """
        Instantiates a WSGI application object.
        """
        from pyramid import paster
        import stackcite.api
        import webtest
        settings = paster.get_appsettings('development.ini')
        app = stackcite.api.main(global_config=None, **settings)
        return webtest.TestApp(app)
