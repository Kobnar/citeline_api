"""
Test layers provide a way to collect tests into groups with common setup and
teardown procedures (e.g. establishing a live connection to a persistent test
database).
"""

import os
import mongoengine


class BaseTestLayer(object):
    """
    A base test layer for the Stackcite API. Works well with any unit tests that
    do not require any special setup or teardown prociedures.
    """


class MongoTestLayer(BaseTestLayer):
    """
    An integration test layer for working with a live MongoDB test database.
    Any tests performed within this layer will be able to connect with and
    manipulate persistent data in MongoDB.
    """

    _IP = os.environ.get('MONGO_TEST_IP', 'http://127.0.0.1/')
    _DB = os.environ.get('MONGO_TEST_DB', 'test')
    _USER = os.environ.get('MONGO_TEST_USER', 'test')
    _PASSWORD = os.environ.get('MONGO_TEST_PASSWORD', 'test')

    @classmethod
    def setUp(cls):
        db = mongoengine.connect(cls._DB)
        db.drop_database(cls._DB)


class WSGITestLayer(MongoTestLayer):
    """
    An integration test layer for working with a complete WSGI application.
    In addition to having a persistent connection to MongoDB, this layer can
    be used to isolate endpoint tests into their own boxes.
    """
