from bson import ObjectId
from bson.errors import InvalidId

from . import index


class DocumentResource(index.IndexResource):
    """
    A modified version of :class:`.IndexResource` providing generalized
    RETRIEVE, UPDATE and DELETE operations for individual documents in MongoDB.

    This class is designed to operate as an abstract class and should not
    be instantiated by itself. In order to perform CRUD operations on a
    document, a child of :class:`~DocumentResource` should be defined as
    the class variable `_document_resource` in a corresponding child of
    :class:`~CollectionResource` set up to access a specific collection.

    :class:`~DocumentResource` is essentially a wrapper for interacting with
    a `mongoengine` back-end. As such, it does not attempt to serialize or
    prepare any data for back-end work. It will, however, aggressively
    instantiate results into :class:`~Document` objects.

    As a final note, this class is designed to accept raw ``pymongo`` queries.
    Future versions are planned to accept higher level ``mongoengine`` options
    as well.

    WARNING: The methods in this class implicitly trust whatever data you throw
    at them. They were created with the assumption that user data will have
    already been parsed and sanitized at the view-level before it is passed
    back to lower-level systems. Do not shove untrusted queries into these
    methods.
    """

    @property
    def id(self):
        """
        The requested document ID.
        """
        return self.__name__

    @property
    def collection(self):
        """
        The MongoDB collection in which this document resides.
        """
        return self.__parent__.collection

    def retrieve(self, fields=None):
        """
        Retrieves the target :class:`mongoengine.Document` from the collection.
        If ``fields`` is set, will only load data for those fields. Raises
        :class:`mongoengine.DoesNotExist` exception if nothing is found.

        :param fields: A list or tuple of explicitly desired field names
        :return: A :class:`mongoengine.Document`
        """
        fields = fields or ()

        assert not isinstance(fields, str)

        results = self.collection.objects
        if fields:
            results = results.only(*fields)
        return results.get(id=self.id)

    def update(self, data):
        """
        Updates the target :class:`mongoengine.Document` according to a nested
        dictionary of data and returns the newly updated document. Raises
        corresponding :class:`mongoengine.DoesNotExist` and
        :class:`mongoengine.ValidationError` exceptions if the document cannot
        be found or if the provided data fails back-end validation.

        :param data: A nested dictionary of data
        :return: An updated :class:`mongoengine.Document`
        """
        assert isinstance(data, dict)

        document = DocumentResource.retrieve(self)
        document.deserialize(data)
        document.save(cascade=True)
        return document

    def delete(self):
        """
        Deletes the target :class:`mongoengine.Document`. Returns an integer
        representing the number of documents deleted (should always be "1").
        Raises :class:`mongoengine.DoesNotExist` exception if the document
        cannot be found.
        """
        return self.collection.objects(id=self.id).delete()


class CollectionResource(index.IndexResource):
    """
    A modified version of :class:`.IndexResource` that provides CREATE and
    RETRIEVE operations for collections of documents in MongoDB.

    This class is designed to operate as an abstract class and should not
    be instantiated by itself. In order to perform CRUD operations on a
    collection, a child of :class:`~CollectionResource` should be defined
    with an explicit ``_COLLECTION`` set.

    :class:`~CollectionResource` is essentially a wrapper for interacting with
    a `mongoengine` back-end. As such, it does not attempt to serialize or
    prepare any data for back-end work. It will, however, aggressively
    instantiate results into :class:`~Document` objects.

    As a final note, this class is designed to accept raw `pymongo` queries.
    Future versions are planned to accept higher level `mongoengine` options
    as well.

    WARNING: The methods in this class implicitly trust whatever data you throw
    at them. They were created with the assumption that user data will have
    already been parsed and sanitized at the view-level before it is passed
    back to lower-level systems. Do not shove untrusted queries into these
    methods.
    """

    # This resource's designated MongoDB collection:
    _COLLECTION = NotImplemented

    # The designated child resource:
    _DOCUMENT_RESOURCE = DocumentResource

    def __getitem__(self, key):
        """
        Attempts to cast ``name`` into a :class:`bson.ObjectId` so it can be
        used to query a specific document. If that fails, method calls
        ``__getitem__()`` of :class:`.IndexResource` to resolve any children
        indexes.
        """
        try:
            key = ObjectId(key)
        except InvalidId:
            return super(CollectionResource, self).__getitem__(key)

        return self._DOCUMENT_RESOURCE(self, str(key))

    @property
    def collection(self):
        """
        A read-only reference to this resource's MongoDB collection.
        """
        return self._COLLECTION

    def create(self, data):
        """
        Creates a new :class:`mongoengine.Document` in the target collection
        based on a nested dictionary of data. Raises
        :class:`mongoengine.ValidationError` if the data provided fails back-end
        validation.

        :param data: A dictionary of new object data
        :return: A newly created MongoEngine document object
        """
        assert isinstance(data, dict)

        document = self.collection()
        document.deserialize(data)
        document.save(cascade=True)
        return document

    def retrieve(self, query=None, fields=None, limit=100, skip=0):
        """
        Retrieves a list of documents from the requested collection. Accepts a
        dictionary-styled ``pymongo`` query, a list of explicitly desired
        ``fields``, a ``limit`` of the maximum number of documents to return
        (default 100) and a number of documents to ``skip`` (default 0).

        :param query: A raw dictionary-styled ``pymongo`` query
        :param fields: A list or tuple of explicitly desired fields
        :param limit: The maximum number of documents to return
        :param skip: The number of documents to skip
        :return: A MongoEngine query object
        """
        query = query or {}
        fields = fields or ()

        assert isinstance(query, dict)
        assert not isinstance(fields, str)
        assert isinstance(limit, int)
        assert isinstance(skip, int)

        # Process query:
        limit += skip
        results = self.collection.objects(__raw__=query)[skip:limit]
        # Filter fields:
        if fields:
            results = results.only(*fields)
        # Return results:
        return results.all()
