import os
import mongoengine

from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.renderers import JSON
from pyramid.httpexceptions import HTTPFound

from citeline_api import api, auth

from . import resources, views


def index(context, request):
    return HTTPFound('/{}/'.format(api.VERSIONS[0]))


def root_traversal_factory(request):
    root = resources.IndexResource(None, '')
    api.traversal_factory(root, api.VERSIONS[0])
    return root


def connect():
    # TODO: Get key names from settings
    host = os.environ.get('CITELINE_MONGO_HOST', 'mongodb://127.0.0.1/')
    db = os.environ.get('CITELINE_MONGO_DB', 'citeline_dev')
    username = os.environ.get('CITELINE_MONGO_USER', 'citeline_dev')
    password = os.environ.get('CITELINE_MONGO_PASSWORD', 'citeline_dev')
    mongoengine.connect(host=host, db=db, username=username, password=password)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    connect()
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
    config.add_view(index, name='', context=resources.IndexResource)
    config.add_renderer('json', JSON())

    config.scan()
    return config.make_wsgi_app()
