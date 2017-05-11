from marshmallow import Schema as _Schema, fields as _fields

from stackcite.api import resources as _resources
from stackcite.api import testing as _testing


class MockEndpointResource(_resources.EndpointResource):
    """
    A "mock" :class:`~EndpointResource` used specifically to test dynamic
    view configuration methods using ``_OFFSPRING`` and ``add_views()`` method.
    """

    class MockViewClass(object):
        METHODS = {'GET': 'mock_schema'}

    class MockOffspring(object):
        @classmethod
        def add_views(cls, config):
            config.add_view('TEST', context='MockOffspring')

    class MockConfig(object):
        def __init__(self):
            self.views = []

        def add_view(self, view_class, context, **kwargs):
            self.views.append({
                'view_class': view_class,
                'context': context})

    _VIEW_CLASS = MockViewClass


class MockValidatedResource(_resources.SerializableResource):
    """
    A "mock" :class:~`SerializableResource` used specifically to test shema
    validation.
    """

    _SCHEMA = _testing.mock.MockDocumentSchema
