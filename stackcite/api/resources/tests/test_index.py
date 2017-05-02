import unittest

from stackcite.api import testing


class IndexResourceTestCase(unittest.TestCase):
    """
    Unit tests for :class:`resources.IndexResource`.
    """

    layer = testing.layers.UnitTestLayer

    def make_root(self):
        from ..index import IndexResource
        self.root = IndexResource(None, 'root')

    def test_init_sets_parent(self):
        """IndexResource.__init__() sets the correct parent
        """
        self.make_root()
        from ..index import IndexResource
        child = IndexResource(self.root, 'child')
        self.assertEqual(child.__parent__, self.root)

    def test_init_parent_accepts_none(self):
        """IndexResource.__init__() accepts 'None' as 'parent'
        """
        from ..index import IndexResource
        try:
            IndexResource(None, 'root')
        except TypeError as err:
            self.fail(err)

    def test_init_parent_accepts_index_resource(self):
        """IndexResource.__init__() accepts an IndexResource as 'parent'
        """
        self.make_root()
        from ..index import IndexResource
        try:
            IndexResource(self.root, 'ux')
        except TypeError as err:
            self.fail(err)

    def test_init_parent_raises_exception_if_parent_is_bad_type(self):
        """IndexResource.__init__() raises an exception if 'parent' is not an IndexResource or 'None'
        """
        from bson import ObjectId
        non_strings = [
            False,
            True,
            1,
            1.1,
            'string',
            ObjectId()]
        from ..index import IndexResource
        for x in non_strings:
            with self.assertRaises(TypeError):
                IndexResource(x, 'ux')

    def test_init_name_accepts_string(self):
        """IndexResource.__init__() accepts a string as 'name'
        """
        from ..index import IndexResource
        try:
            IndexResource(None, 'ux')
        except TypeError as err:
            self.fail(err)

    def test_init_sets_name(self):
        """IndexResource.__init__() sets the correct name
        """
        self.make_root()
        from ..index import IndexResource
        child = IndexResource(self.root, 'child')
        self.assertEqual(child.__name__, 'child')

    def test_init_name_raises_exception_for_non_strings(self):
        """IndexResource.__init__() raises an exception if 'name' is not a string
        """
        from bson import ObjectId
        from ..index import IndexResource
        non_strings = [
            None,
            False,
            True,
            1, 1.1,
            ObjectId(),
            IndexResource(None, 'ux')]
        for x in non_strings:
            with self.assertRaises(TypeError):
                IndexResource(None, x)

    def test_setitem_sets_names_for_cls(self):
        """IndexResource.__setitem__() sets the correct name for class
        """
        self.make_root()
        from ..index import IndexResource
        self.root['1'] = IndexResource
        self.root['1']['1.1'] = IndexResource
        self.root['2'] = IndexResource
        self.root['2']['2.1'] = IndexResource
        self.root['2']['2.1']['2.1.1'] = IndexResource
        self.root['2']['2.2'] = IndexResource
        self.assertEqual(
            self.root['1'].__name__,
            '1')
        self.assertEqual(
            self.root['1']['1.1'].__name__,
            '1.1')
        self.assertEqual(
            self.root['2'].__name__,
            '2')
        self.assertEqual(
            self.root['2']['2.1'].__name__,
            '2.1')
        self.assertEqual(
            self.root['2']['2.1']['2.1.1'].__name__,
            '2.1.1')
        self.assertEqual(
            self.root['2']['2.2'].__name__,
            '2.2')

    def test_setitem_sets_parents_for_cls(self):
        """IndexResource.__setitem__() sets the correct parent for class
        """
        self.make_root()
        from ..index import IndexResource
        self.root['1'] = IndexResource
        self.root['1']['1.1'] = IndexResource
        self.root['2'] = IndexResource
        self.root['2']['2.1'] = IndexResource
        self.root['2']['2.1']['2.1.1'] = IndexResource
        self.root['2']['2.2'] = IndexResource
        self.assertEqual(
            self.root['1'].__parent__,
            self.root)
        self.assertEqual(
            self.root['1']['1.1'].__parent__,
            self.root['1'])
        self.assertEqual(
            self.root['2'].__parent__,
            self.root)
        self.assertEqual(
            self.root['2']['2.1'].__parent__,
            self.root['2'])
        self.assertEqual(
            self.root['2']['2.1']['2.1.1'].__parent__,
            self.root['2']['2.1'])
        self.assertEqual(
            self.root['2']['2.2'].__parent__,
            self.root['2'])

    def test_setitem_raises_exception_if_item_is_not_an_indexresource(self):
        """IndexResource.__setitem__() raises an exception if the item is not a type of IndexResource
        """
        self.make_root()
        from datetime import datetime
        with self.assertRaises(TypeError):
            self.root['mock'] = datetime.now()

    def test_setitem_accepts_resource_instance(self):
        """IndexResource.__setitem__() accepts an instance of IndexResource without raising an exception
        """
        self.make_root()
        from ..index import IndexResource
        child_resource = IndexResource(self.root, 'child_resource')
        try:
            self.root['child_resource'] = child_resource
        except TypeError:
            self.fail("Failed to set an instantiated instance of IndexResource")

    def test_name_returns_name(self):
        """IndexResource.name returns the correct __name__ string
        """
        self.make_root()
        expected = 'root'
        result = self.root.name
        self.assertEqual(result, expected)

    def test_linage_returns_linage(self):
        """IndexResource.name returns the correct lineage for the resource
        """
        self.make_root()
        from ..index import IndexResource
        level_0 = IndexResource(self.root, 'level_0')
        level_1 = IndexResource(level_0, 'level_1')
        level_0['level_1'] = level_1
        self.root['level_0'] = level_0
        result = level_1.lineage
        expected = ['level_1', 'level_0', 'root']
        self.assertEqual(result, expected)

    def test_setitem_sets_parent_with_traversal_factory_pattern(self):
        """IndexResource.__setitem__() sets parent with traversal_factory pattern
        """
        self.make_root()
        from ..index import IndexResource

        def mock_traversal_factory(parent, name):
            return IndexResource(parent, name)

        self.root['child'] = mock_traversal_factory
        self.assertEqual(self.root['child'].__parent__, self.root)

    def test_setitem_sets_name_with_traversal_factory_pattern(self):
        """IndexResource.__setitem__() sets name with traversal_factory pattern
        """
        self.make_root()
        from ..index import IndexResource

        def mock_traversal_factory(parent, name):
            return IndexResource(parent, name)

        self.root['child'] = mock_traversal_factory
        self.assertEqual(self.root['child'].__name__, 'child')

    def test_setitem_raises_exception_for_bad_traversal_signature(self):
        """IndexResource.__setitem__() raises exception for bad traversal signature
        """
        self.make_root()
        from ..index import IndexResource

        def mock_traversal_factory(parent):
            return IndexResource(parent, 'some_child')

        with self.assertRaises(TypeError):
            self.root['child'] = mock_traversal_factory

    def test_iter_through_children(self):
        """IndexResource.__iter__() iterates through children
        """
        self.make_root()
        from ..index import IndexResource
        names = ('child_0', 'child_1', 'child_2')
        for child in names:
            self.root[child] = IndexResource
        for name in self.root:
            item = self.root[name]
            self.assertIn(item.name, names)
