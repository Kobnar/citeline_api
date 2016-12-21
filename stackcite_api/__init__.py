import mongoengine

from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.renderers import JSON
from pyramid.httpexceptions import HTTPFound

from . import (
    api,
    auth,
    resources,
    views
)


def root_traversal_factory(request):
    root = resources.IndexResource(None, '')
    root[api.VERSION] = api.resources.APIIndex
    return root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    mongoengine.connect(
        host=settings['mongo.host'],
        db=settings['mongo.db']
    )
    config = Configurator(
        settings=settings,
        root_factory=root_traversal_factory)

    # Custom request attributes
    config.add_request_method(auth.get_token, 'token', reify=True)
    config.add_request_method(auth.get_user, 'user', reify=True)

    # Authentication and authorization policies
    authentication_policy = auth.AuthTokenAuthenticationPolicy(debug=True)
    authorization_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)

    # JSON response rendering
    config.add_renderer('json', JSON())

    # API views configuration
    api.resources.APIIndex.add_views(config)

    # Root index redirect to API index view
    config.add_view(
        lambda c, r: HTTPFound('/{}/'.format(api.VERSION)),
        context=resources.IndexResource)

    config.scan()
    return config.make_wsgi_app()
