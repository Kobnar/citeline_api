import unittest

from citeline_api import testing


class ObjectIdFieldTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..fields import ObjectIdField
        self.field = ObjectIdField()

    def test_deserialize_accepts_valid_string(self):
        """ObjectIdField accepts a valid ObjectId string
        """
        from bson import ObjectId
        object_id = str(ObjectId())
        result = self.field.deserialize(object_id)
        self.assertEqual(object_id, result)

    def test_deserialize_raises_exception_for_invalid_string(self):
        """ObjectIdField raises exception for an invalid string
        """
        bad_id = 'bad_id'
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.field.deserialize(bad_id)


class ListFieldTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..fields import ListField
        self.field = ListField()

    def test_deserialize_list_items(self):
        """ListSchema.deserialize() parses a list string into a python list
        """
        data = '12,cat,Michael Bolton'
        result = self.field.deserialize(data)
        expected = ['12', 'cat', 'Michael Bolton']
        self.assertEqual(expected, result)

    def test_deserialize_single_list_item(self):
        """ListSchema.deserialize() parses a single string into a list w/ one item
        """
        data = 'Michael Bolton'
        result = self.field.deserialize(data)
        expected = ['Michael Bolton']
        self.assertEqual(expected, result)

    def test_deserialize_empty_string(self):
        """ListSchema.deserialize() parses an empty string into an empty list
        """
        data = ''
        result = self.field.deserialize(data)
        expected = []
        self.assertEqual(expected, result)

    def test_deserialize_none(self):
        """ListSchema.deserialize() raises exception for None
        """
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.field.deserialize(None)


class FieldsFieldTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..fields import FieldsField
        self.fields = FieldsField()

    def test_deserialize_list_items(self):
        """FieldsSchema.deserialize() parses a list string into a python list
        """
        data = '12,cat,Michael Bolton'
        result = self.fields.deserialize(data)
        expected = ['12', 'cat', 'Michael Bolton']
        self.assertEqual(expected, result)

    def test_deserialize_single_list_item(self):
        """FieldsSchema.deserialize() parses a single string into a list w/ one item
        """
        data = 'Michael Bolton'
        result = self.fields.deserialize(data)
        expected = ['Michael Bolton']
        self.assertEqual(expected, result)

    def test_deserialize_empty_string(self):
        """FieldsSchema.deserialize() parses an empty string into an empty list
        """
        data = ''
        result = self.fields.deserialize(data)
        expected = []
        self.assertEqual(expected, result)

    def test_deserialize_none(self):
        """ListSchema.deserialize() raises exception for None
        """
        from marshmallow import ValidationError
        with self.assertRaises(ValidationError):
            self.fields.deserialize(None)

    def test_deserialize_converts_subfield_notation(self):
        """FieldsSchema.deserialize() converts underscores to dots for subfields
        """
        data = 'id,name__full,birth,pets__dogs__indoor'
        expected = ['id', 'name.full', 'birth', 'pets.dogs.indoor']
        result = self.fields.deserialize(data)
        self.assertEqual(expected, result)