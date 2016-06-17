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

    def retrieve(self, fields=None):
        fields = fields or ()

        assert isinstance(fields, typing.Sequence)

        result = super().retrieve(fields)
        return result.serialize(fields)

    def update(self, data):
        assert isinstance(data, typing.Container)

        result = super().update(data)
        return result.serialize()

    def delete(self):
        result = super().delete()
        return bool(result)


class APICollection(resources.CollectionResource):
    """
    The API-level traversal resource.
    """

    def create(self, data):
        assert isinstance(data, typing.Container)

        result = super().create(data)
        return result.serialize()

    def retrieve(self, query=None, fields=None, limit=100, skip=0):
        query = query or {}
        fields = fields or ()

        assert isinstance(query, typing.Container)
        assert isinstance(limit, int)
        assert isinstance(skip, int)

        results = super().retrieve(query, fields, limit, skip)

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
