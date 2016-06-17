import unittest

from pyramid import testing


class ViewTestCase(unittest.TestCase):
    """
    A :class:`BaseTestCase` designed for testing view objects with traversal
    contexts. Provides a view with a `DummyRequest` and traversal resource as
    a context.
    """

    def get_view(self, resource_class, view_class,
                 name='test_context'):
        """Returns a qualified view object for testing.

        :param resource_class: The resource class associated with the view under test
        :param view_class: The view class under test (e.g. `BaseView`)
        :return: A qualified view object
        """
        context = resource_class(None, name)
        request = testing.DummyRequest()
        view = view_class(context, request)
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

    def get_view(self, collection_class, view_class,
                 object_id=None, parent_name='parent_context'):
        """
        Assembles a new view object with a designated :class:`.DocumentResource`
        context. If no `ObjectId` is provided, this method generates a new
        `ObjectId` for testing.

        :param object_id: The target `ObjectId` for the :class:`.DocumentResource`
        :return: A :class:`.DocumentResource` view object
        """
        # Generate a new ObjectId if one was not provided:
        if not object_id:
            from bson import ObjectId
            object_id = ObjectId()
        # Assemble and return the view:
        parent = collection_class(None, parent_name)
        context = parent[object_id]
        request = testing.DummyRequest()
        view = view_class(context, request)
        return view
