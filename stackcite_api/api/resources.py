import bson

from pyramid import security as sec

from stackcite_api import resources

from . import (
    schema as api_schema,
    views as api_views
)


class APIIndex(resources.IndexResource):
    """
    The root index resource.
    """

    VIEW_CLASS = api_views.APIIndexViews

    __acl__ = [
        (sec.Allow, sec.Everyone, 'retrieve'),
        sec.DENY_ALL
    ]


class ValidatedResource(object):
    """
    An abstract class providing a basic schema loading and validation
    :class:`Resource`.
    """

    _schema = NotImplemented

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
        schema = self._schema.get(method)
        if schema:
            schema = schema(strict=strict)
            data, errors = schema.load(data)
        return data, errors


class APIDocument(resources.DocumentResource, ValidatedResource):
    """
    The API-level traversal resource.
    """

    VIEW_CLASS = api_views.APIDocumentViews

    __acl__ = [
        (sec.Allow, sec.Authenticated, ('update', 'delete')),
        (sec.Allow, sec.Everyone, 'retrieve'),
        sec.DENY_ALL
    ]

    _schema = {
        'GET': api_schema.forms.RetrieveDocument
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


class APICollection(resources.CollectionResource, ValidatedResource):
    """
    The API-level traversal resource.
    """

    VIEW_CLASS = api_views.APICollectionViews

    __acl__ = [
        (sec.Allow, sec.Authenticated, 'create'),
        (sec.Allow, sec.Everyone, 'retrieve'),
        sec.DENY_ALL
    ]

    _schema = {
        'GET': api_schema.forms.RetrieveCollection
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

        if results:
            return [doc.serialize(fields) for doc in results]
        else:
            return []

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
