import typing
from citeline_api import resources


class APIIndex(resources.IndexResource):
    """
    The root index resource.
    """


class APIDocument(resources.DocumentResource):
    """
    The API-level traversal resource.
    """

    _retrieve_schema = NotImplemented
    _update_schema = NotImplemented

    def retrieve(self, query=None):
        query = query or {}
        if self._retrieve_schema is not NotImplemented:
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

    _create_schema = NotImplemented
    _retrieve_schema = NotImplemented

    def create(self, data):
        data = data or {}
        if self._create_schema is not NotImplemented:
            schema = self._create_schema(strict=True)
            data = schema.load(data).data
        result = super().create(data)
        return result.serialize()

    def retrieve(self, query=None):
        query = query or {}
        if self._retrieve_schema is not NotImplemented:
            schema = self._retrieve_schema(strict=True)
            query = schema.load(query).data
        fields, limit, skip = self.get_commons(query)
        # TODO: Create hook to build a raw query in children of APICollection
        raw_query = {}
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
