"""
Because of the complicated and highly integrated relationship between views,
resources, and requests when resolving an action, the Stackcite API relies on
special test cases to create standard, predictable test conditions.
"""

import unittest

from pyramid import testing

from stackcite.api import resources


class BaseViewTestCase(unittest.TestCase):
    """
    A base test case designed to coordinate the instantiation of an explicitly
    defined ``VIEW_CLASS`` with a default :class:`~IndexResource` and
    :class:`~DummyRequest`.
    """

    #: The view class under test (should be defined in unit test case).
    VIEW_CLASS = NotImplemented

    #: A resource class associated with the view class under test.
    RESOURCE_CLASS = resources.IndexResource

    #: A dummy request class.
    REQUEST_CLASS = testing.DummyRequest

    def make_view(self, name=None):
        """
        Creates an instance of the view class under test along with associated
        context and request objects.

        :return: An instance of ``VIEW_CLASS``
        """
        name = name or str(self.RESOURCE_CLASS)
        context = self.RESOURCE_CLASS(None, name)
        request = self.REQUEST_CLASS()
        view = self.VIEW_CLASS(context, request)
        return view


class APIViewTestCase(BaseViewTestCase):
    """
    An alternate version of :class:`~BaseViewTestCase` for testing API view
    classes.
    """

    RESOURCE_CLASS = resources.APIIndexResource


class ExceptionViewTestCase(BaseViewTestCase):
    """
    An alias of :class:`~BaseViewTestCase` used specifically to test exception
    contexts (e.g. :class:`APIValidationError`).
    """


class CollectionViewTestCase(BaseViewTestCase):
    """
    An alias for :class:`.BaseViewTestCase` used specifically to test
    collection endpoint view classes.
    """


class DocumentViewTestCase(BaseViewTestCase):
    """
    A modified version of :class:`~CollectionViewTestCase` used specifically
    to test view classes associated with specific documents in a collection.
    """

    def make_view(self, object_id=None, parent_name=None):
        """
        Creates an instance of the view class under test along with associated
        context and request objects. Specifically, this method will use the
        resource defined by ``RESOURCE_CLASS`` as a parent, and mock a
        traversal resolution for a :class:`bson.ObjectId`.

        Note: This method will randomly generate a :class:`bson.ObjectId`
        to fill in ``object_id`` if nothing is provided.

        :param object_id: A target :class:`bson.ObjectId` string
        :param parent_name: The parent resource name
        :return: An instance of ``VIEW_CLASS``
        """
        parent_name = parent_name or str(self.RESOURCE_CLASS)
        # Generate a new ObjectId if one was not provided:
        if not object_id:
            from bson import ObjectId
            object_id = str(ObjectId())
        # Assemble and return the view:
        parent = self.RESOURCE_CLASS(None, parent_name)
        context = parent[object_id]
        request = testing.DummyRequest()
        view = self.VIEW_CLASS(context, request)
        return view
