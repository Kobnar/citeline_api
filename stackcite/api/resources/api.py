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
        mongo.DocumentResource, EndpointResource):
    """
    The API-level traversal resource.
    """

    __acl__ = [
        (psec.Allow, psec.Authenticated, ('update', 'delete')),
        (psec.Allow, psec.Everyone, 'retrieve'),
        psec.DENY_ALL
    ]

    _VIEW_CLASS = views.APIDocumentViews
    _SCHEMA = schema.APIDocumentSchema

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
        mongo.CollectionResource, EndpointResource):
    """
    The API-level traversal resource.
    """

    __acl__ = [
        (psec.Allow, psec.Authenticated, 'create'),
        (psec.Allow, psec.Everyone, 'retrieve'),
        psec.DENY_ALL
    ]

    _VIEW_CLASS = views.APICollectionViews
    _SCHEMA = schema.APICollectionSchema

    _DOCUMENT_RESOURCE = APIDocumentResource
    _DOCUMENT_SCHEMA = schema.APIDocumentSchema

    # TODO: Find a better pattern to inject custom raw queries
    def retrieve(self, query=None, fields=None, limit=100, skip=0):
        raw_query = self._raw_query(query)
        self._retrieve(query)
        return super().retrieve(raw_query, fields, limit, skip)

    def _retrieve(self, query):
        pass

    def schema(self, method=None, only=(), exclude=(), strict=None):
        schm = self._SCHEMA(only=only, exclude=exclude, strict=strict)
        schm.document_schema = self._DOCUMENT_SCHEMA
        schm.method = method
        return schm

    def load(self, query, method=None, **kwargs):
        schm = self.schema(method=method)
        return schm.load(query, **kwargs)

    def dump(self, data, method=None, **kwargs):
        schm = self.schema(method=method)
        return schm.dump(data, **kwargs)

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
