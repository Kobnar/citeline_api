import os
import mongoengine

from pyramid.config import Configurator
from pyramid.renderers import JSON

from citeline_api import api


def root_traversal_factory(request):
    return api.traversal_factory(None, '')


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
    config = Configurator(
        settings=settings,
        root_factory=root_traversal_factory)
    config.add_renderer('json', JSON())
    config.scan()
    return config.make_wsgi_app()
