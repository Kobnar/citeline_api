import unittest

from pyramid import testing


class ViewTestCase(unittest.TestCase):
    """
    A :class:`BaseTestCase` designed for testing view objects with traversal
    contexts. Provides a view with a `DummyRequest` and traversal resource as
    a context.
    """

    RESOURCE_CLASS = NotImplemented
    REQUEST_CLASS = testing.DummyRequest
    VIEW_CLASS = NotImplemented

    def get_view(self, name='test_context'):
        """Returns a qualified view object for testing.

        :return: A qualified view object
        """
        context = self.RESOURCE_CLASS(None, name)
        request = self.REQUEST_CLASS()
        view = self.VIEW_CLASS(context, request)
        return view


class CollectionViewTestCase(ViewTestCase):
    """
    An alias for :class:`.ViewTestCase` that communicates when the developer is
    specifically testing a MongoDB collection of documents.
    """


class DocumentViewTestCase(ViewTestCase):
    """
    A :class:`.ViewTestCase` that has been modified to create a specialized
    MongoDB document view.

    NOTE: This test case's `get_view()` function requires an ObjectId or it
    will randomly generate a new one.
    """

    def get_view(self, object_id=None, parent_name='parent_context'):
        """
        Assembles a new view object with a designated :class:`.DocumentResource`
        context. If no `ObjectId` is provided, this method generates a new
        `ObjectId` for testing.

        :param object_id: The target `ObjectId` for the :class:`.DocumentResource`
        :param parent_name: The parent resource name
        :return: A :class:`.DocumentResource` view object
        """
        # Generate a new ObjectId if one was not provided:
        if not object_id:
            from bson import ObjectId
            object_id = ObjectId()
        # Assemble and return the view:
        parent = self.RESOURCE_CLASS(None, parent_name)
        context = parent[object_id]
        request = testing.DummyRequest()
        view = self.VIEW_CLASS(context, request)
        return view
