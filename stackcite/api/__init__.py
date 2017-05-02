import mongoengine

from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.renderers import JSON
from pyramid.httpexceptions import HTTPFound

from . import (
    index,
    auth,
    resources,
    views
)


def root_factory(request=None):
    root = resources.IndexResource()
    # Defers naming the API's version to the package-level definition
    root[index.VERSION] = index.traversal_factory(root)
    return root


def configure_views(config):
    # TODO: find a better reference to the traversal tree
    root_resource = root_factory()
    api_resource = root_resource[index.VERSION]

    # Add a root-level redirect to the most recent API endpoint
    config.add_view(
        lambda c, r: HTTPFound('/{}/'.format(index.VERSION)),
        context=resources.IndexResource)

    # Recursively add views associated with traversal tree resources
    def connect(rsrc):
        for name in rsrc:
            child = rsrc[name]
            connect(child)
        rsrc.add_views(config)

    connect(api_resource)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    mongoengine.connect(
        host=settings['mongo.host'],
        db=settings['mongo.db']
    )
    config = Configurator(
        settings=settings,
        root_factory=root_factory)

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

    # Configure views
    configure_views(config)

    config.scan()
    return config.make_wsgi_app()
