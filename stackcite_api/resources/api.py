import bson

from pyramid import security as psec

from stackcite_api import views, schema

from . import index, mongo


class EndpointResource(object):
    """
    An abstract class providing API endpoint resources with self-contained
    view configuration methods.
    """

    _VIEW_CLASS = NotImplemented
    _OFFSPRING = NotImplemented

    @classmethod
    def add_views(cls, config):
        """
        Recursively adds the ``_VIEW_CLASS`` associated with this class and any
        traversal routes defined in ``_OFFSPRING``.

        :param config: A Pyramid WSGI configuration object
        """
        cls._add_cls_view(config)
        for offspring in cls._OFFSPRING.values():
            offspring.add_views(config)

    @classmethod
    def _add_cls_view(cls, config):
        """
        Adds this class' ``_VIEW_CLASS`` to a Pyramid WSGI configuration object.

        :param config: A Pyramid WSGI configuration object
        """
        for method, attr in cls._VIEW_CLASS.METHODS:
            config.add_view(
                cls._VIEW_CLASS,
                context=cls,
                request_method=method,
                attr=attr,
                permission=attr)


class ValidatedResource(object):
    """
    An abstract class providing a basic schema loading and validation
    :class:`Resource`.
    """

    _DEFAULT_SCHEMA = NotImplemented
    _SCHEMA = {}

    def validate(self, method, data, strict=True):
        """
        If the `method` provided has an associated data validation schema
        defined in `_schema`, this method will instantiate the associated
        schema and validate the provided data. Otherwise, it will return the
        original data without performing any data validation.

        :param method: An HTTP request method name (e.g. `GET`)
        :param data: A nested dictionary of request data
        :param strict: If true, raises exception for validation errors
        :return: A tuple in the form of (``data``, ``errors``)
        """
        errors = None
        schema = self._SCHEMA.get(method) or self._DEFAULT_SCHEMA.get(method)
        if schema:
            schema = schema(strict=strict)
            data, errors = schema.load(data)
        return data, errors


class APIIndexResource(index.IndexResource, EndpointResource):
    """
    A base traversal resource used to define API indexes for Pyramid's
    traversal system.
    """


class APIDocument(
        mongo.DocumentResource, ValidatedResource, EndpointResource):
    """
    The API-level traversal resource.
    """

    _VIEW_CLASS = views.APIDocumentViews

    __acl__ = [
        (psec.Allow, psec.Authenticated, ('update', 'delete')),
        (psec.Allow, psec.Everyone, 'retrieve'),
        psec.DENY_ALL
    ]

    _DEFAULT_SCHEMA = {
        'GET': schema.forms.RetrieveDocument
    }

    def retrieve(self, query=None):
        query = query or {}
        query, errors = self.validate('GET', query)
        fields = query.get('fields')
        result = super().retrieve(fields)
        return result.serialize(fields)

    def update(self, data):
        data = data or {}
        data, errors = self.validate('PUT', data)
        result = super().update(data)
        return result.serialize()

    def delete(self):
        result = super().delete()
        return bool(result)


class APICollection(
        mongo.CollectionResource, ValidatedResource, EndpointResource):
    """
    The API-level traversal resource.
    """

    _VIEW_CLASS = views.APICollectionViews

    __acl__ = [
        (psec.Allow, psec.Authenticated, 'create'),
        (psec.Allow, psec.Everyone, 'retrieve'),
        psec.DENY_ALL
    ]

    _DEFAULT_SCHEMA = {
        'GET': schema.forms.RetrieveCollection
    }

    def create(self, data):
        data = data or {}
        data, errors = self.validate('POST', data)
        result = super().create(data)
        return result.serialize()

    def retrieve(self, query=None):
        query = query or {}
        query, errors = self.validate('GET', query)
        fields, limit, skip = self.get_commons(query)
        raw_query = self._raw_query(query)
        results = super().retrieve(raw_query, fields, limit, skip)

        return {
            'count': results.count(),
            'limit': limit,
            'skip': skip,
            'items': [doc.serialize(fields) for doc in results]
        }

    @staticmethod
    def get_commons(query):
        """
        A helper method used to extract and prepare the common ``fields``,
        ``limit`` and ``skip`` values used by-default in collection-level
        queries.

        :param query: A nested dictionary of values
        :return: fields, limit, skip
        """
        fields, limit, skip = (), 100, 0

        if 'fields' in query.keys():
            fields = query.pop('fields')
        if 'limit' in query.keys():
            limit = query.pop('limit')
        if 'skip' in query.keys():
            skip = query.pop('skip')

        return fields, limit, skip

    @staticmethod
    def _raw_query(query=None):
        """
        A hook to build a raw pymongo query.

        :param query: The output of `self._retrieve_schema`.
        :return: A raw pymongo query
        """
        raw_query = query or {}
        ids = query.pop('ids', None)
        if ids:
            ids = [bson.ObjectId(id) for id in ids]
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
