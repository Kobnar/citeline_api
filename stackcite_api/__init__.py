import mongoengine

from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.renderers import JSON

from stackcite_api import api, auth

from . import resources, views, api


def root_traversal_factory(request):
    root = resources.IndexResource(None, '')
    api.traversal_factory(root, api.VERSIONS[0])
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

    # Authentication
    authentication_policy = auth.TokenAuthenticationPolicy(debug=True)
    authorization_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)

    # Views
    config.add_renderer('json', JSON())
    config.add_view(api.root_redirect, context=resources.IndexResource)
    api.view_factory(config)

    config.scan()
    return config.make_wsgi_app()
