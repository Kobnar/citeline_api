import bson
from citeline_api import resources

from . import schemas


class APIIndex(resources.IndexResource):
    """
    The root index resource.
    """


class APIDocument(resources.DocumentResource):
    """
    The API-level traversal resource.
    """

    _retrieve_schema = schemas.forms.RetrieveDocument
    _update_schema = NotImplemented

    def retrieve(self, query=None):
        query = query or {}
        schema = self._retrieve_schema(strict=True)
        query = schema.load(query).data
        fields = query.get('fields')
        result = super().retrieve(fields)
        return result.serialize(fields)

    def update(self, data):
        data = data or {}
        if self._update_schema is not NotImplemented:
            schema = self._update_schema(strict=True)
            data = schema.load(data).data
        result = super().update(data)
        return result.serialize()

    def delete(self):
        result = super().delete()
        return bool(result)


class APICollection(resources.CollectionResource):
    """
    The API-level traversal resource.
    """

    _retrieve_schema = schemas.forms.RetrieveCollection
    _create_schema = NotImplemented

    def create(self, data):
        data = data or {}
        if self._create_schema is not NotImplemented:
            schema = self._create_schema(strict=True)
            data = schema.load(data).data
        result = super().create(data)
        return result.serialize()

    def retrieve(self, query=None):
        query = query or {}
        schema = self._retrieve_schema(strict=True)
        query = schema.load(query).data
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
    def _raw_query(query):
        """
        A hook to build a raw pymongo query.
        :param query: The output of `self._retrieve_schema`.
        :return: A raw pymongo query
        """
        raw_query = {}
        ids = query.get('ids')
        if ids:
            ids = [bson.ObjectId(id) for id in ids]
            raw_query.update({'_id': {'$in': ids}})
        return raw_query
