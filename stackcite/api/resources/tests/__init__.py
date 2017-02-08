from marshmallow import Schema as _Schema, fields as _fields

from stackcite.api import resources as _resources


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
    _OFFSPRING = {
        'route_0': MockOffspring,
        'route_1': MockOffspring}


class MockValidatedResource(_resources.ValidatedResource):
    """
    A "mock" :class:~`ValidatedResource` used specifically to test shema
    validation.
    """

    class MockSchema(_Schema):
        required = _fields.Bool()

    _DEFAULT_SCHEMA = {'GET': MockSchema}


class MockValidatedChildResource(MockValidatedResource):
    """
    A "mock" :class:~`ValidatedResource` used specifically to test overridden
    and child schema validation.
    """

    class MockSchema(_Schema):
        name = _fields.String(required=True)

    _DEFAULT_SCHEMA = {'GET': MockSchema}
