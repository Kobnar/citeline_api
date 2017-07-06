import unittest

from stackcite.api import testing


class BaseViewTests(unittest.TestCase):
    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from pyramid import testing
        self.context = {'name': 'test_context'}
        self.request = testing.DummyRequest({'data': 'test_request'})
        from ..base import BaseView
        self.view = BaseView(self.context, self.request)

    def test_context_set(self):
        """BaseView.__init__() sets a given context object
        """
        try:
            context = self.view.context
            self.assertEqual(context['name'], 'test_context')
        except AttributeError:
            self.fail('BaseView.context not set.')

    def test_request_set(self):
        """BaseView.__init__() sets a given request object
        """
        try:
            request = self.view.request
            self.assertEqual(request.params['data'], 'test_request')
        except AttributeError:
            self.fail('BaseView.request not set.')