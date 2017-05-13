import bson

from pyramid import security as psec

from stackcite.api import views, schema

from . import index, mongo


class EndpointResource(object):
    """
    An abstract class providing API endpoint resources with self-contained
    view configuration methods.
    """

    _VIEW_CLASS = NotImplemented

    @classmethod
    def add_views(cls, config):
        """
        Recursively adds the ``_VIEW_CLASS`` associated with this class and any
        traversal routes defined in ``_OFFSPRING``.

        :param config: A Pyramid WSGI configuration object
        """
        for method, attr in cls._VIEW_CLASS.METHODS.items():
            config.add_view(
                cls._VIEW_CLASS,
                context=cls,
                request_method=method,
                attr=attr,
                permission=attr)


class SerializableResource(object):
    """
    An abstract class providing a basic schema loading and validation
    :class:`Resource`.
    """

    _SCHEMA = NotImplemented

    @property
    def schema(self):
        return self._SCHEMA

    def load(self, data, only=(), method=None, many=False, strict=True,
             json=False):
        """
        Loads (and validates) serialized data into a Python-compatible data
        structure.

        If the `method` provided has an associated data validation schema
        defined in `_schema`, this method will instantiate the associated
        schema and validate the provided data. Otherwise, it will return the
        original data without performing any data validation.

        :param data: A nested dictionary of request
        :param only: A list of fields to include (e.g. `('birth', 'name.first')`)
        :param method: An HTTP request method name (e.g. `GET`)
        :param many: Whether to deserialize data as a collection
        :param strict: Whether to raise an exception for validation errors
        :param json: Whether the input data is a JSON encoded string
        :return: A tuple in the form of (``data``, ``errors``)
        """
        if self._SCHEMA:
            scheme = self._SCHEMA(
                method=method, only=only, many=many, strict=strict)
            if json:
                return scheme.loads(data)
            return scheme.load(data)
        return data, {}

    def dump(self, data, only=(), method=None, many=False, json=False):
        """
        Dumps (i.e. serializes) Python objects into a serialized data structure.

        (See docstring for `load()` above.)

        :param data: A nested dictionary of request data
        :param only: A list of fields to include (e.g. `('birth', 'name.first')`)
        :param method: An HTTP request method name (e.g. `GET`)
        :param many: Whether to deserialize data as a collection
        :param json: Whether the output data should be a JSON encoded string
        :return: A tuple in the form of (``data``, ``errors``)
        """
        if self._SCHEMA:
            scheme = self._SCHEMA(method=method, only=only, many=many)
            if json:
                return scheme.dumps(data)
            return scheme.dump(data)
        return data, {}

    def loads(self, data, only=(), method=None, many=False, strict=True):
        return self.load(data, only, method, many, strict, json=True)

    def dumps(self, data, only=(), method=None, many=False):
        return self.dump(data, only, method, many, json=True)


class APIIndexResource(index.IndexResource, EndpointResource):
    """
    A base traversal resource used to define API indexes for Pyramid's
    traversal system.
    """


def _get_params(query, params):
    """
    Extracts a dictionary of special query parameters to update a dictionary
    of known defaults.

    NOTE: This function creates copies of the original dicts instead of
        modifying the existing data structures

    :param query: A dictionary of document-level query parameters
    :param params: A dictionary of collection-level query parameters
    :return: A two-tuple in the form of (``query``, ``params``)
    """
    query = query.copy()
    params = params.copy()
    params.update({k: query.pop(k) for k in params.keys()
                   if k in query.keys()})
    return query, params


class APIDocumentResource(
        mongo.DocumentResource, SerializableResource, EndpointResource):
    """
    The API-level traversal resource.
    """

    _VIEW_CLASS = views.APIDocumentViews

    __acl__ = [
        (psec.Allow, psec.Authenticated, ('update', 'delete')),
        (psec.Allow, psec.Everyone, 'retrieve'),
        psec.DENY_ALL
    ]

    @property
    def schema(self):
        if self._SCHEMA is NotImplemented:
            return self.__parent__.schema
        else:
            return self._SCHEMA

    @staticmethod
    def get_params(query):
        """
        A helper method used to extract collection-level query parameters,
        including:

            * ``fields``

        :param query: A dictionary of document-level query parameters
        :return: A two-tuple in the form of (``query``, ``params``)
        """
        params = {
            'fields': ()
        }
        return _get_params(query, params)


class APICollectionResource(
        mongo.CollectionResource, SerializableResource, EndpointResource):
    """
    The API-level traversal resource.
    """

    _VIEW_CLASS = views.APICollectionViews

    __acl__ = [
        (psec.Allow, psec.Authenticated, 'create'),
        (psec.Allow, psec.Everyone, 'retrieve'),
        psec.DENY_ALL
    ]

    _DOCUMENT_RESOURCE = APIDocumentResource
    _SCHEMA = schema.APICollectionSchema

    # TODO: Find a better pattern to inject custom raw queries
    def retrieve(self, query=None, fields=None, limit=100, skip=0):
        raw_query = self._raw_query(query)
        self._retrieve(query)
        return super().retrieve(raw_query, fields, limit, skip)

    def _retrieve(self, query):
        pass

    @staticmethod
    def get_params(query):
        """
        A helper method used to extract collection-level query parameters,
        including:

            * ``fields``
            * ``limit``
            * ``skip``

        :param query: A dictionary of document-level query parameters
        :return: A two-tuple in the form of (``query``, ``params``)
        """
        params = {
            'fields': (),
            'limit': 100,
            'skip': 0
        }
        return _get_params(query, params)

    @staticmethod
    def _raw_query(query):
        """
        A hook to build a raw pymongo query.

        :param query: The output of `self._retrieve_schema`.
        :return: A raw pymongo query
        """
        raw_query = query or {}
        ids = query.pop('ids', None) if query else []
        if ids:
            ids = [bson.ObjectId(oid) for oid in ids]
            raw_query.update({'_id': {'$in': ids}})
        return raw_query

    @classmethod
    def add_views(cls, config):
        """
        A wrapper for ``add_views()`` in :class:`~EndpointResource` that adds
        the views associated with ``_DOCUMENT_RESOURCE``, which is not located
        in the traversal tree.

        :param config: A Pyramid WSGI configuration object
        """
        super().add_views(config)
        cls._DOCUMENT_RESOURCE.add_views(config)
